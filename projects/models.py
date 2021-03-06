from django.db import models
from accounts.models import *

from django.db import models

from django.db import models
from django.utils import timezone
import datetime, math, json


# Create your models here.


class ProjectManager(models.Manager):
    def finished_charity_filter_count(self, charity):
        return super().all().filter(project_state__iexact='finished').filter(charity=charity).count()

    def related_charity_filter_count(self, charity):
        return super().all().filter(charity=charity).count()


class Ability(models.Model):
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, default='')
    ability_type = models.ForeignKey(AbilityType, on_delete=models.CASCADE, default='')
    score = models.IntegerField(default=-1)
    description = models.CharField(max_length=512, default='')


class Project(models.Model):
    project_name = models.CharField(max_length=256, default='')
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE, default='')
    benefactors = models.ManyToManyField(Benefactor)
    description = models.CharField(max_length=2048, default='')
    project_state = models.CharField(max_length=64, default='open')
    type = models.CharField(max_length=64, default='')
    objects = ProjectManager()

    def __str__(self):
        return self.project_name + "-" + self.type


class FinancialProject(models.Model):
    # TODO set min
    project = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True, default='')

    target_money = models.FloatField(default=0.0)
    current_money = models.FloatField(default=0.0)

    start_date = models.DateField(default=datetime.date(2018, 1, 1))
    end_date = models.DateField(default=datetime.date(2018, 1, 1))

    def add_contribution(self, amount):
        self.current_money += amount
        if self.current_money >= amount:
            self.project.project_state = 'completed'
        self.project.save()
        self.save()

    def progress_in_range(self, min_progress, max_progress):
        return min_progress < self.current_money / self.target_money < max_progress

    def __str__(self):
        return self.project.__str__()


class NonFinancialProject(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True, default='')

    ability_type = models.ForeignKey(AbilityType, on_delete=models.DO_NOTHING, default='')
    min_age = models.IntegerField(default=0)
    max_age = models.IntegerField(default=200)
    required_gender = models.CharField(max_length=128, null=True)

    country = models.CharField(max_length=32, null=True)
    province = models.CharField(max_length=32, null=True)
    city = models.CharField(max_length=32, null=True)

    request = models.OneToOneField(CooperationRequest, on_delete=models.DO_NOTHING, null=True)

    def search_filter(self, min_date_overlap, min_required_hours, min_time_overlap, schedule):
        return \
            has_matched_schedule(min_date_overlap, min_required_hours, min_time_overlap, schedule, self.dateinterval)[0]

    def __str__(self):
        return self.project.__str__()


class DateInterval(models.Model):
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, null=True)
    non_financial_project = models.OneToOneField(NonFinancialProject, on_delete=models.CASCADE, null=True)

    begin_date = models.DateField(default=datetime.date(2018, 1, 1))
    end_date = models.DateField(default=datetime.date(2018, 1, 1))
    week_schedule = models.CharField(max_length=512, default='')

    def to_json(self, schedule):
        self.week_schedule = json.dumps(schedule)

    def from_json(self):
        return json.loads(self.week_schedule)


class FinancialContribution(models.Model):
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, default='')
    financial_project = models.ForeignKey(FinancialProject, on_delete=models.CASCADE, default='')
    money = models.FloatField(default=0)


def search_benefactor(wanted_schedule=None, min_required_hours=0, min_date_overlap=30, min_time_overlap=50, tags=None,
                      ability_name=None, ability_min_score=0, ability_max_score=10, country=None, province=None,
                      city=None, user_min_score=0, user_max_score=10, gender=None, first_name=None, last_name=None):
    if tags is None:
        tags = []

    schedule_filtered = []

    result_benefactors = Benefactor.objects.all().filter(score__lte=user_max_score).filter(score__gte=user_min_score)
    if first_name is not None:
        result_benefactors = result_benefactors.filter(first_name__icontains=first_name)
    if last_name is not None:
        result_benefactors = result_benefactors.filter(last_name__icontains=last_name)
    if gender is not None:
        result_benefactors = result_benefactors.filter(gender__iexact=gender)
    if country is not None:
        result_benefactors = result_benefactors.filter(user__contactinfo__country__iexact=country)
    if province is not None:
        result_benefactors = result_benefactors.filter(user__contactinfo__province__iexact=province)
    if city is not None:
        result_benefactors = result_benefactors.filter(user__contactinfo__city__iexact=city)

    ability_type_ids = AbilityType.objects.find_ability_ids(ability_name, tags)
    result_ids = [benefactor.id for benefactor in result_benefactors if
                  benefactor.has_ability(ability_type_ids, ability_min_score, ability_max_score)]
    result_benefactors = result_benefactors.filter(id__in=result_ids)

    if wanted_schedule is not None:
        schedule_data = [benefactor.search_filter(min_date_overlap, min_required_hours, min_time_overlap,
                                                  wanted_schedule) for benefactor in result_benefactors]
        schedule_filtered = [(benefactor.id, data[1], data[2]) for
                             benefactor, data in zip(result_benefactors, schedule_data) if data[0]]
        result_benefactors = result_benefactors.filter(id__in=[data[0] for data in schedule_filtered])

    benefactor_list = list(result_benefactors)
    final_results = [(benefactor, data[1], data[2]) for benefactor, data in zip(benefactor_list, schedule_filtered)]

    return final_results


def search_charity(name=None, min_score=0, max_score=10, min_related_projects=0, max_related_projects=math.inf,
                   min_finished_projects=0, max_finished_projects=math.inf, benefactor_name=None, country=None
                   , province=None, city=None):
    result_charities = Charity.objects.all().filter(score__lte=min_score).filter(score__gte=max_score)
    filtered_ids = [charity.id for charity in result_charities if
                    max_related_projects >
                    Project.objects.related_charity_filter_count(charity) > min_related_projects and
                    max_finished_projects >
                    Project.objects.finished_charity_filter_count(charity) > min_finished_projects]
    result_charities = result_charities.filter(id__in=filtered_ids)
    if name is not None:
        result_charities = result_charities.filter(name__icontains=name)
    if country is not None:
        result_charities = result_charities.filter(user__contactinfo__country__iexact=country)
    if province is not None:
        result_charities = result_charities.filter(user__contactinfo__province__iexact=province)
    if city is not None:
        result_charities = result_charities.filter(user__contactinfo__city__iexact=city)
    if benefactor_name is not None:
        benefactors = Benefactor.objects.all().filter(first_name__icontains=benefactor_name) \
                      | Benefactor.objects.all().filter(last_name__icontains=benefactor_name)
        filtered_ids = []
        for benefactor in benefactors:
            filtered_ids.extend([charity.id for charity in result_charities if
                                 benefactor.charity_set.filter(pk=charity.pk).exists()])
        result_charities = result_charities.filter(id__in=filtered_ids)
    return result_charities


def filter_projects(current_projects, project_name, charity_name, benefactor_name, project_state):
    if project_name is not None:
        current_projects = current_projects.filter(project__project_name__iexact=project_name)
    if charity_name is not None:
        current_projects = current_projects.filter(project__charity__name=charity_name)
    if project_state is not None:
        current_projects = current_projects.filter(project__project_state__iexact=project_state)
    if benefactor_name is not None:
        benefactors = Benefactor.objects.all().filter(first_name__icontains=benefactor_name) \
                      | Benefactor.objects.all().filter(last_name__icontains=benefactor_name)
        filtered_ids = []
        for benefactor in benefactors:
            filtered_ids.extend([project.id for project in current_projects if
                                 benefactor.project_set.filter(pk=project.project.pk).exists()])
        current_projects = current_projects.filter(id__in=filtered_ids)
    return current_projects


def search_financial_project(project_name=None, charity_name=None, benefactor_name=None, project_state=None,
                             min_progress=0, max_progress=100, min_deadline_date=None, max_deadline_date=None):
    filtered_ids = [financial_project.id for financial_project in FinancialProject.objects.all() if
                    financial_project.progress_in_range(min_progress, max_progress)]
    result_financial_projects = FinancialProject.objects.all().filter(id__in=filtered_ids)
    result_financial_projects = result_financial_projects.filter(end_date__gte=min_deadline_date) \
        .filter(end_date__lte=max_deadline_date)
    return filter_projects(result_financial_projects, project_name, charity_name, benefactor_name, project_state)


def search_non_financial_project(project_name=None, charity_name=None, benefactor_name=None, project_state=None,
                                 ability_name=None, tags=None, wanted_schedule=None, min_required_hours=0,
                                 min_date_overlap=30, min_time_overlap=50, age=None, gender=None, country=None,
                                 province=None, city=None):
    result_projects = NonFinancialProject.objects.all()
    result_projects = filter_projects(result_projects, project_name, charity_name, benefactor_name, project_state)

    if age is not None:
        result_projects = result_projects.filter(min_age__lte=age).filter(max_age__gte=age)
    if gender is not None:
        result_projects = result_projects.filter(required_gender__iexact=gender)
    if country is not None:
        result_projects = result_projects.filter(country__iexact=country)
    if province is not None:
        result_projects = result_projects.filter(province__iexact=province)
    if city is not None:
        result_projects = result_projects.filter(city__iexact=city)
    if wanted_schedule is not None:
        filter_ids = [project.id for project in result_projects if
                      project.search_filter(min_date_overlap, min_required_hours, min_time_overlap, wanted_schedule)]
        result_projects = result_projects.filter(id__in=filter_ids)
    ability_type_ids = AbilityType.objects.find_ability_ids(ability_name, tags)
    filter_ids = [project.id for project in result_projects if project.ability_type.id in ability_type_ids]
    result_projects = result_projects.filter(id__in=filter_ids)
    return result_projects
