from django.views.generic import TemplateView, ListView, DetailView, FormView
from .custom import user_in_group, user_can, in_group_decorator, user_can_decorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from os.path import join, abspath
from datetime import date
from os import mkdir
from django.conf import settings
from .forms import *


#@method_decorator(user_can_decorator(['custom_permission_1']), name='dispatch')  # Decorator use example


class MainPage(TemplateView):
    template_name = 'index.html'


class MainPage2(TemplateView):
    template_name = 'app/index.html'



class LoginPage(TemplateView):
    template_name = 'login_page.html'


class AccessRequired(TemplateView):
    template_name = 'access_required_page.html'


class StartProjectView(FormView):
    template_name = "base.html"
    form_class = StartProjectForm
    success_url = "/app/"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')

        if form.is_valid():
            print('form.is_valid')
            data = form.cleaned_data
            # в мене цей рядок не працює маю переписати щоб запрацював
            #pth = join('stor', str(date.today()) + '-' + data['first_name'] + '-' + data['last_name'])
            pth = settings.MEDIA_ROOT
            print(pth)
            print(request.FILES)
            form.cleaned_data['file'] = abspath(pth)
            for f in files:
                with open(join(pth, str(f)), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            return self.form_valid(form, request.FILES['file'])
        else:
            return self.form_invalid(form)

    def form_valid(self, form, fil):
        print('form_valid')

        a = form.save(commit=False)
        a.file = fil
        a.save()

        return super(StartProjectView, self).form_valid(form)

