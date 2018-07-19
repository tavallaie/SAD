from django.db import models
from accounts.models import *

from django.db import models

from django.db import models
import json

import datetime, math
from django.utils import timezone


# Create your models here.


class ProjectManager(models.Manager):
    def finished_charity_filter_count(self, charity):
        return super().all().filter(project_state__iexact='finished').filter(charity=charity).count()

    def related_charity_filter_count(self, charity):
        return super().all().filter(charity=charity).count()


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE, primary_key=False)
    benefactors = models.ManyToManyField(Benefactor, primary_key=False)
    description = models.CharField(max_length=2000)
    project_state = models.CharField(max_length=50)
    objects = ProjectManager
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.project_name


class FinancialProject(models.Model):
    # TODO set min
    project = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)
    target_money = models.FloatField
    current_money = models.FloatField
    start_date = models.DateField()
    end_date = models.DateField()

    def progress_in_range(self, min_progress, max_progress):
        return min_progress < self.current_money / self.target_money < max_progress

    def __str__(self):
        super.__str__(self)


class NonFinancialProject(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        super.__str__(self)


class AbilityType(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

    def __str__(self):
        return self.name


class Ability(models.Model):
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE)
    ability_type = models.ForeignKey(AbilityType, on_delete=models.CASCADE)
    score = models.IntegerField
    description = models.CharField(max_length=300)


class Requirement(models.Model):
    project = models.ForeignKey(NonFinancialProject, on_delete=models.CASCADE, primary_key=False)
    ability_types = models.ManyToManyField(AbilityType, primary_key=False)
    min_age = models.IntegerField
    max_age = models.IntegerField
    gender = models.CharField(max_length=100)
    location = models.CharField(max_length=1000)
    require_quantity = models.IntegerField


class DateInterval(models.Model):
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, null=True)
    non_financial_project = models.ForeignKey(NonFinancialProject, on_delete=models.CASCADE, null=True)

    begin_date = models.DateField
    end_date = models.DateField
    week_schedule = models.CharField(max_length=200)

    def to_json(self, schedule):
        self.week_schedule = json.dumps(schedule)

    def from_json(self):
        return json.loads(self.week_schedule)


class Request(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, primary_key=False,
                               related_name='%(class)s_requests_sender')
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, primary_key=False,
                                 related_name='%(class)s_requests_receiver')
    description = models.CharField(max_length=2000)


# TODO add effect of province and city
def search_benefactor(wanted_schedule, min_required_hours, min_date_overlap=30, min_time_overlap=50,
                      ability_name=None, ability_min_score=0, ability_max_score=10, country=None, province=None,
                      city=None,
                      user_min_score=0, user_max_score=10, gender=None, first_name=None, last_name=None):
    result_benefactors = Benefactor.objects.all().filter(score__lte=user_max_score).filter(score__gte=user_min_score)
    if first_name is not None:
        result_benefactors = result_benefactors.filter(first_name__iexact=first_name)
    if last_name is not None:
        result_benefactors = result_benefactors.filter(last_name__iexact=last_name)
    if gender is not None:
        result_benefactors = result_benefactors.filter(gender__iexact=gender)

    schedule_filtered_ids = \
        [benefactor.id for benefactor in result_benefactors if
         benefactor.search_filter(min_date_overlap, min_required_hours, min_time_overlap, wanted_schedule)]
    result_benefactors = result_benefactors.filter(id__in=schedule_filtered_ids)

    if country is not None:
        result_benefactors = result_benefactors.filter(user__contactinfo__country__iexact=country)
    if province is not None:
        result_benefactors = result_benefactors.filter(user__contactinfo__province__iexact=province)
    if city is not None:
        result_benefactors = result_benefactors.filter(user__contactinfo__city__iexact=city)

    abilities = Ability.objects.all()
    if ability_name is not None:
        abilities = abilities.filter(ability_type__name__iexact=ability_name)
        pass


# TODO add effect of province and city
def search_charity(name=None, min_score=0, max_score=10, min_related_projects=0, max_related_projects=math.inf,
                   min_finished_projects=0, max_finished_projects=math.inf, related_benefactor=None, country=None
                   , province=None, city=None):
    result_charities = Charity.objects.all().filter(score__lte=min_score).filter(score__gte=max_score)
    filtered_ids = [charity.id for charity in result_charities if
                    max_related_projects >
                    Project.objects.related_charity_filter_count(charity) > min_related_projects and
                    max_finished_projects >
                    Project.objects.finished_charity_filter_count(charity) > min_finished_projects]
    result_charities = result_charities.filter(id__in=filtered_ids)
    if name is not None:
        result_charities = result_charities.filter(name__iexact=name)
    if related_benefactor is not None:
        filtered_ids = [charity.id for charity in result_charities if
                        related_benefactor.charity_set.filter(pk=charity.pk).exists()]
        result_charities = result_charities.filter(id__in=filtered_ids)


# TODO idk about ability
def search_financial_project(project_name=None, charity_name=None, benefactor=None, project_state=None,
                             min_progress=0, max_progress=100, start_date=None, end_date=None):
    filtered_ids = [financial_project.id for financial_project in FinancialProject.objects.all() if
                    financial_project.progress_in_range(min_progress, max_progress)]
    result_financial_projects = FinancialProject.objects.all().filter(id__in=filtered_ids)

    if project_name is not None:
        result_financial_projects = result_financial_projects.filter(project__project_name__iexact=project_name)
    if charity_name is not None:
        result_financial_projects = result_financial_projects.filter(project__charity__name=charity_name)
    if project_state is not None:
        result_financial_projects = result_financial_projects.filter(project__project_state__iexact=project_state)
    if benefactor is not None:
        filtered_ids = [financial_project.id for financial_project in result_financial_projects if
                        benefactor.project_set.filter(pk=financial_project.project.pk)]
        result_financial_projects = result_financial_projects.filter(id__in=filtered_ids)



    pass
