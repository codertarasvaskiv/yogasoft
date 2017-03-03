from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, DetailView, FormView, View
from .custom import user_in_group, user_can, in_group_decorator, user_can_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from os.path import join, abspath
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.conf import settings
from datetime import date
from os import mkdir
from .forms import *
from .models import *


TESTIMONIALS_ON_PAGE = 8
TESTIMONIALS_ON_ADMIN_PAGE = 8


# @method_decorator(user_can_decorator(['custom_permission_1']), name='dispatch')  # Decorator use example
class MainPage(TemplateView):
    template_name = 'base.html'


class LoginPage(TemplateView):
    template_name = 'login_page.html'


class AccessRequired(TemplateView):
    template_name = 'access_required_page.html'


class StartProjectView(FormView):
    template_name = "base.html"


class IndexPage(FormView):
    template_name = 'app/index.html'
    form_class = StartProjectForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')

        if form.is_valid():
            data = form.cleaned_data
            pth = join('stor', str(date.today()) + '-' + data['first_name'] + '-' + data['last_name'])
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
        a = form.save(commit=False)
        a.file = pth
        a.save()
        return super(IndexPage, self).form_valid(form)


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


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'app/blog.html'

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        blog_post = context['object']
        context['tags'] = blog_post.tags.all()
        comments = blog_post.comment_set.all()
        context['comments'] = {}
        for i in comments:
            if i.is_moderated:
                context['comments'][i] = list(CommentSecondLevel.objects.filter(father_comment=i))
                for j in context['comments'][i]:
                    if not j.is_moderated:
                        context['comments'][i].pop(context['comments'][i].index(j))
        context['form'] = CommentForm()
        context.pop('blogpost')

        return context


def AddComment(request, pk):
    data = request.POST
    if request.user.is_authenticated():
        q = Comment(author_email=request.user.email, author_name=request.user)
    else:
        q = Comment(author_email=data['author_email'], author_name=data['author_name'])
    q.message = data['message']
    q.blog = BlogPost.objects.get(pk=pk)
    q.save(q)
    return redirect('app:blog_detail_view', pk)


def add_second_comment(request, pk, comm_pk):
    data = request.POST
    print(request.user)
    if request.user.is_authenticated():
        q = CommentSecondLevel(author_email=request.user.email, author_name=request.user)
    else:
        q = CommentSecondLevel(author_email=data['author_email'], author_name=data['author_name'])
    q.message = data['message']
    q.father_comment = Comment.objects.get(pk=comm_pk)
    q.save(q)
    return redirect('app:blog_detail_view', pk)


class BlogListView(ListView):
    model = BlogPost
    template_name = 'app/BlogList.html'

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        if 'tag' in self.kwargs:
            return Tag.objects.get(name__exact=self.kwargs['tag']).blogpost_set.all()
        else:
            return BlogPost.objects.all()


# just testing need to delete later Taras
class Test(TemplateView):
    template_name = 'app/test.html'


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('#')


class ContactUsView(FormView):
    template_name = 'app/contact_us.html'
    form_class = ContactUsForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        data = request.POST
        q = ContactUsModel()
        q.author_email = data['author_email']
        q.author_name = data['author_name']
        q.message = data['message']
        q.save(q)
        return redirect("app:index_page")


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, '#', {}, context)
            else:
                return render(request, '#', {}, context)
        else:
            print("Invalid login details: {}, {}".format(username, password))
            return render(request, '#', {})
    else:
        return render(request, '#', {}, context)
