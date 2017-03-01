from django.views.generic import TemplateView, ListView, DetailView, FormView, View
from .custom import user_in_group, user_can, in_group_decorator, user_can_decorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from os.path import join, abspath
from django.shortcuts import render
from datetime import date

from os import mkdir
from .forms import *
from .models import Testimonial


TESTIMONIALS_ON_PAGE = 8
TESTIMONIALS_ON_ADMIN_PAGE = 8

#@method_decorator(user_can_decorator(['custom_permission_1']), name='dispatch')  # Decorator use example
class MainPage(TemplateView):
    template_name = 'base.html'


class LoginPage(TemplateView):
    template_name = 'login_page.html'


class AccessRequired(TemplateView):
    template_name = 'access_required_page.html'


class StartProjectView(FormView):
    template_name = "base.html"
    form_class = StartProjectForm
    success_url = "/app/"

    def post(self, request, *args, **kwargs):
        print("post inside project")
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')

        if form.is_valid():
            data = form.cleaned_data
            # в мене цей рядок не працює маю переписати щоб запрацював
            #pth = join('stor', str(date.today()) + '-' + data['first_name'] + '-' + data['last_name'])
            pth = r"C:\Users\Gus.Ol\projects"
            try:
                mkdir(pth)
            except FileExistsError:
                pass
            form.cleaned_data['file'] = abspath(pth)
            for f in files:
                with open(join(pth, str(f)), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            return self.form_valid(form, abspath(pth))
        else:
            return self.form_invalid(form)

    def form_valid(self, form, pth):
        print("form valid")

        a = form.save(commit=False)
        a.file = pth
        a.save()

        return super(StartProjectView, self).form_valid(form)


class Testimonials(ListView):
    model = Testimonial
    template_name = "testimonials.html"
    paginate_by = TESTIMONIALS_ON_PAGE
    context_object_name = "testimonials"

    def get_queryset(self):
        return Testimonial.objects.filter(is_moderated=True).order_by('-date')

    def post(self, request):
        if 'save' in request.POST:
            author_name = request.POST['author_name']
            author_email = request.POST['author_email']
            message = request.POST['message']
            new_tstm = Testimonial(author_name=author_name, author_email=author_email, message=message)
            new_tstm.save()
            return HttpResponseRedirect(reverse('app:testimonials'))
        return HttpResponseRedirect(reverse('app:testimonials'))


class TestimonialsAdmin(ListView):
    model = Testimonial
    template_name = "testimonials_admin.html"
    paginate_by = TESTIMONIALS_ON_ADMIN_PAGE
    context_object_name = "testimonials"

    def get_queryset(self):
        if 'mod' in self.request.GET:
            view_moderated = self.request.GET['mod']
            if view_moderated == 'true':
                return Testimonial.objects.filter(is_moderated=True).order_by('-date')
            elif view_moderated == 'false':
                return Testimonial.objects.filter(is_moderated=False).order_by('-date')
            else:
                return Testimonial.objects.order_by('date')  # If not specified get all.
        else:
            return Testimonial.objects.order_by('date')  # If not specified get all.

    def post(self, request, testimonial_id=None):
        view_moderated = request.GET.get('mod', 'all')
        page = request.GET.get('page', 1)

        if 'moderated' in request.POST:
            try:
                testimonial = Testimonial.objects.get(pk=testimonial_id)
                testimonial.is_moderated = True
                testimonial.save()
            except Testimonial.DoesNotExist:
                return HttpResponseRedirect(reverse('app:testimonials_admin')+'?mod={0}&page={1}'
                                            .format(view_moderated, page))
            return HttpResponseRedirect(reverse('app:testimonials_admin')+'?mod={0}&page={1}'
                                        .format(view_moderated, page))

        elif 'delete' in request.POST:
            try:
                testimonial = Testimonial.objects.get(pk=testimonial_id)
                testimonial.delete()
            except Testimonial.DoesNotExist:
                return HttpResponseRedirect(reverse('app:testimonials_admin')+'?mod={0}&page={1}'
                                            .format(view_moderated, page))
            return HttpResponseRedirect(reverse('app:testimonials_admin')+'?mod={0}&page={1}'
                                        .format(view_moderated, page))

        elif 'save' in request.POST:
            author_name = request.POST['author_name']
            author_email = request.POST['author_email']
            message = request.POST['message']
            new_tstm = Testimonial(author_name=author_name, author_email=author_email, message=message)
            new_tstm.save()
            return HttpResponseRedirect(reverse('app:testimonials_admin')+'?mod={0}&page={1}'
                                        .format(view_moderated, page))
        else:
            return HttpResponseRedirect(reverse('app:testimonials_admin')+'?mod={0}&page={1}'
                                        .format(view_moderated, page))
