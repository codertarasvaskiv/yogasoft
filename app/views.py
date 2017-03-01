from django.views.generic import TemplateView, ListView, DetailView, FormView
from .custom import user_in_group, user_can, in_group_decorator, user_can_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from os.path import join, abspath
from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
from datetime import date
from os import mkdir
from .forms import *
from .models import *


# @method_decorator(user_can_decorator(['custom_permission_1']), name='dispatch')  # Decorator use example
class MainPage(TemplateView):
    template_name = 'base.html'


class IndexPage(FormView):
    template_name = 'app/index.html'
    form_class = StartProjectForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        print("post inside project")
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


class LoginPage(TemplateView):
    template_name = 'login_page.html'


class AccessRequired(TemplateView):
    template_name = 'access_required_page.html'


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
        context['form'] = CommentForm()
        context.pop('blogpost')

        return context


def AddComment(request, pk):
    data = request.POST
    q = Comment()
    q.author_email = data['author_email']
    q.author_name = data['author_name']
    q.message = data['message']
    q.blog = BlogPost.objects.get(pk=pk)
    q.save(q)
    return redirect('app:blog_detail_view', pk)


def add_second_comment(request, pk, comm_pk):
    data = request.POST
    q = CommentSecondLevel()
    q.author_email = data['author_email']
    q.author_name = data['author_name']
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


def login(request):
    pass


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('#')
