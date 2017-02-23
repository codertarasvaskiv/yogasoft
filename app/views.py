from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic import View
from django.shortcuts import render
from .custom import user_in_group, user_can, in_group_decorator, user_can_decorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


#@method_decorator(login_required, name='dispatch')
#@method_decorator(in_group_decorator(['admin']), name='dispatch')
@method_decorator(user_can_decorator(['custom_permission_1']), name='dispatch')
class MainPage(TemplateView):
    template_name = 'base.html'


class LoginPage(TemplateView):
    template_name = 'login_page.html'


class AccessRequired(TemplateView):
    template_name = 'access_required_page.html'
