from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView

from projects.models import *
from django.template import loader


# Create your views here.

def find_non_financial_projects_search_results(request):
    if request.user.is_authenticated:
        pass
    if request.user.is_charity:
        pass
    all_ability_types = [ability_type.name for ability_type in AbilityType.objects.all()]
    all_ability_tags = [ability_tag.name for ability_tag in AbilityTag.objects.all()]

    if request.method == 'GET':
        return render(request, 'url', {
            'ability_types': all_ability_types,
            'ability_tags': all_ability_tags,
            'result_non_financial_projects': []
        })

    project_name = request.POST.get('search_non_financial_project_name')
    charity_name = request.POST.get('search_non_financial_charity_name')
    benefactor_name = request.POST.get('search_non_financial_benefactor_name')
    project_state = request.POST.get('search_non_financial_project_state')
    ability_name = request.POST.get('search_non_financial_ability_name')
    tags = request.POST.get('search_non_financial_tags')
    start_date = request.POST.get('search_non_financial_start_date')
    end_date = request.POST.get('search_non_financial_end_date')
    weekly_schedule = create_query_schedule(request.POST.get('search_non_financial_schedule'))
    schedule = [start_date, end_date, weekly_schedule]
    min_required_hours = request.POST.get('searchnon_financial_min_required_hours')
    min_date_overlap = request.POST.get('search_non_financial_min_date_overlap')
    min_time_overlap = request.POST.get('search_non_financial_min_time_overlap')
    age = request.POST.get('search_non_financial_age')
    gender = request.POST.get('search_non_financial_gender')
    country = request.POST.get('search_non_financial_country')
    province = request.POST.get('search_non_financial_province')
    city = request.POST.get('search_non_financial_city')
    project_queryset = search_non_financial_project(project_name, charity_name, benefactor_name, project_state,
                                                    ability_name, tags, schedule, min_required_hours, min_date_overlap,
                                                    min_time_overlap, age, gender, country, province, city)
    return render(request, 'url', {
        'result_non_financial_projects': list(project_queryset),
        'ability_types': all_ability_types,
        'ability_tags': all_ability_tags
    })


def find_financial_project_search_results(request):
    if request.user.is_authenticated:
        pass
    if request.user.is_charity:
        pass
    project_name = request.POST.get('search_financial_project_name')
    charity_name = request.POST.get('search_financial_charity_name')
    benefactor_name = request.POST.get('search_financial_benefactor_name')
    project_state = request.POST.get('search_financial_project_state')
    min_progress = request.POST.get('search_financial_min_progress')
    max_progress = request.POST.get('search_financial_max_progress')
    min_deadline_date = request.POST.get('search_financial_min_deadline_date')
    max_deadline_date = request.POST.get('search_financial_max_deadline_date')
    project_queryset = search_financial_project(project_name, charity_name, benefactor_name, project_state,
                                                min_progress, max_progress, min_deadline_date, max_deadline_date)
    return render(request, 'url', {'result_financial_projects': list(project_queryset)})


def find_charity_search_results(request):
    if request.user.is_authenticated:
        pass
    if request.user.is_charity:
        pass
    charity_name = request.POST.get('search_charity_name')
    min_score = request.POST.get('search_charity_min_score')
    max_score = request.POST.get('search_charity_max_score')
    min_related_projects = request.POST.get('search_charity_min_related_projects')
    max_related_projects = request.POST.get('search_charity_max_related_projects')
    min_finished_projects = request.POST.get('search_charity_min_finished_projects')
    max_finished_projects = request.POST.get('search_charity_max_finished_projects')
    benefactor_name = request.POST.get('search_charity_benefactor_name')
    country = request.POST.get('search_charity_country')
    province = request.POST.get('search_charity_province')
    city = request.POST.get('search_charity_city')
    charity_queryset = search_charity(charity_name, min_score, max_score, min_related_projects, max_related_projects,
                                      min_finished_projects, max_finished_projects, benefactor_name, country, province,
                                      city)
    return render(request, 'url', {'result_charities': list(charity_queryset)})


# TODO handle security and stuff like that
def find_benefactor_search_results(request):
    if request.user.is_authenticated:
        pass
    if request.user.is_benefactor:
        pass
    start_date = request.POST.get('search_benefactor_start_date')
    end_date = request.POST.get('search_benefactor_end_date')
    weekly_schedule = create_query_schedule(request.POST.get('search_benefactor_schedule'))
    schedule = [start_date, end_date, weekly_schedule]
    min_required_hours = request.POST.get('search_benefactor_min_required_hours')
    min_date_overlap = request.POST.get('search_benefactors_min_date_overlap')
    min_time_overlap = request.POST.get('search_benefactors_min_time_overlap')
    tags = request.POST.get('search_benefactor_tags')
    ability_name = request.POST.get('search_benefactor_ability_name')
    ability_min_score = request.POST.get('search_benefactor_ability_min_score')
    ability_max_score = request.POST.get('search_benefactor_ability_max_score')
    country = request.POST.get('search_benefactor_country')
    province = request.POST.get('search_benefactor_province')
    city = request.POST.get('search_benefactor_city')
    user_min_score = request.POST.get('search_benefactor_user_min_score')
    user_max_score = request.POST.get('search_benefactor_user_max_score')
    gender = request.POST.get('search_benefactor_gender')
    first_name = request.POST.get('search_benefactor_first_name')
    last_name = request.POST.get('search_benefactor_last_name')
    result_benefactor_data = search_benefactor(schedule, min_required_hours, min_date_overlap, min_time_overlap, tags,
                                            ability_name, ability_min_score, ability_max_score, country, province,
                                            city, user_min_score, user_max_score, gender, first_name, last_name)
    # benefactor_list = list(benefactor_queryset)
    # result_benefactor_data = []
    # for benefactor, overlap_data in zip(benefactor_list, search_overlap_data):
    #     result_benefactor_data.append([benefactor, overlap_data[0], overlap_data[1]])

    return render(request, 'wtf?', {'result_benefactors': result_benefactor_data})


def create_new_project(request):

    if request.user.is_authenticated:
        project = Project.objects.create()
        project.project_name = request.POST.get('project_name')
        project.charity = request.user
        project.description = request.POST.get('description')
        project.state = 'open'
        project.save()
        if request.POST.get('type') is 'financial':
            project.type = 'financial'
            financial_project = FinancialProject.objects.create()
            if request.POST.get('start_date') is not None:
                financial_project.start_date = datetime.datetime.strptime(request.POST.get('start_date'), '%y-%m-%d')
            else:
                financial_project.start_date = datetime.date.today()
            # FIXME only date not datetime?
            financial_project.end_date = datetime.datetime.strptime(request.POST.get('end_date'), '%y-%m-%d')
            financial_project.project = project
            financial_project.target_money = int(request.POST.get('target_money'))
            if request.POST.get('current_money') is not None:
                financial_project.current_money = request.POST.get('current_money')
            else:
                financial_project.current_money = 0
            financial_project.save()
        else:
            project.type = 'non-financial'
            non_financial_project = NonFinancialProject.objects.create()
            non_financial_project.project = project
            if request.POST.get("ability_type") is not None:
                non_financial_project.ability_type = request.POST.get("ability_type")
            if request.POST.get("min_age") is not None:
                non_financial_project.min_age = request.POST.get("min_age")
            if request.POST.get("max_age") is not None:
                non_financial_project.max_age = request.POST.get("max_age")
            non_financial_project.required_gender = request.POST.get("required_gender")
            non_financial_project. country = request.POST.get("country")
            non_financial_project.province = request.POST.get("province")
            non_financial_project.city = request.POST.get("city")
            date_interval = DateInterval.objects.create()
            date_interval.begin_date = request.POST.get('start_date')
            date_interval.end_date = request.POST.get('end_date')
            date_interval.non_financial_project = non_financial_project
            # FIXME check if the input is JSON or not
            date_interval.week_schedule = request.POST.get('week_schedule')
            non_financial_project.save()
        # TODO Fix redirect path
        return HttpResponseRedirect('path')
    else:
        # TODO Fix content
        return HttpResponse(content=[])


def edit_project(request, pk):
    # TODO fix path
    template = loader.get_template('path-to-template')
    if not request.user.is_authenticated():
        return HttpResponse(template.render({'pk': pk, 'error_message': 'Authentication Error!'}, request))
    if request.method is not 'POST':
        return HttpResponse(template.render({'pk': pk, 'error_message': 'Method is not POST!'}, request))
    project = Project.objects.get(pk=pk)
    try:
        dic = request.POST
        project.project_name = dic['project_name']
        project.project_state = dic['project_state']
        project.description = dic['description']
        if project.type is 'financial':
            fin_project = FinancialProject.objects.get(project=project)
            fin_project.target_money = dic['target_money']
            fin_project.start_date = dic['start_date']
            fin_project.end_date = dic['end_date']
            # FIXME should the current_money be editable or not?
            fin_project.current_money = dic['current_money']
            fin_project.save()
        else:
            nf_project = NonFinancialProject.objects.get(project=project)
            nf_project.ability_type = dic['ability_type']
            nf_project.city = dic['city']
            nf_project.country = dic['country']
            nf_project.max_age = dic['max_age']
            nf_project.min_age = dic['min_age']
            nf_project.project = dic['province']
            nf_project.required_gender = dic['required_gender']
            date_interval = nf_project.dateinterval
            if dic.get('start_date') is not None:
                date_interval.begin_date = dic['start_date']
            date_interval.end_date = dic['end_date']
            if dic.get('week_schedule') is not None:
                date_interval.week_schedule = dic['week_schedule']
            nf_project.save()
            date_interval.save()
        project.save()
    except:
        context = {
            'pk': pk,
            'error_message': 'Error in finding the Project!'
        }
        return HttpResponse(template.render(context, request))
    # FIXME maybe all responses should be Redirects / parameters need fixing
    return HttpResponseRedirect([])


def show_project_data(request, pk):
    project = Project.objects.get(pk=pk)
    # TODO fix template path
    template = loader.get_template('projects/get_project_data_for_edit.html')
    try:
        context = {
            'pk': pk,
            'project_name': project.project_name,
            'description': project.description,
            'project_state': project.project_state,
            'type': project.type,
        }
        if project.type is 'financial':
            fin_project =  FinancialProject.objects.get(project=project)
            context.update({
                'start_date': fin_project.start_date,
                'end_date': fin_project.end_date,
                'target_money': fin_project.target_money,
                'current_money': fin_project.current_money
            })
        else:
            nf_project = NonFinancialProject.objects.get(project=project)
            context.update({
                'ability_type':nf_project.ability_type,
                'min_age':nf_project.min_age,
                'max_age':nf_project.max_age,
                'required_gender':nf_project.required_gender,
                'country':nf_project.country,
                'province':nf_project.province,
                'city':nf_project.city,
            })
    except:
        context = {
            'pk': pk,
            'error_message': 'Error in finding the Project!'
        }
    return HttpResponse(template.render(context, request))


class CreateProjectForm(TemplateView):
    template_name = "create_project_form.html"


def contribute_to_project(request, project_id):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        return HttpResponse([])
    if request.user.is_charity:
        # TODO Raise Account Type Error
        return HttpResponse([])
    project = Project.objects.get(id=project_id)
    if project.type is not 'financial':
        # TODO Raise Project Type Error
        return HttpResponse([])
    fin_project = FinancialProject.objects.get(project=project)
    try:
        if project.project_state is 'completed':
            # TODO Raise Project Closed Error
            return HttpResponse([])
        amount = float(request.POST.get('money'))
        benefactor = Benefactor.objects.get(user=request.user)
        if benefactor.credit < amount:
            # TODO Raise Not Enough Money Error
            return HttpResponse([])
        contribution = FinancialContribution.objects.get(benefactor=benefactor, financial_project=fin_project)
        if contribution is not None:
            contribution.money += amount
            contribution.save()
        else:
            FinancialContribution.objects.create(benefactor=benefactor, financial_project=fin_project, money=amount)
        benefactor.credit -= amount
        fin_project.add_contribution(amount)
        benefactor.save()
        # TODO Redirect
        return HttpResponseRedirect([])
    except:
        # TODO Raise Unexpected Error
        return HttpResponse([])