
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib.auth.models import User
from .custom import user_in_group, user_can, in_group_decorator, user_can_decorator, args_builder
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, request
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from os.path import join, abspath
from django.shortcuts import redirect, render, render_to_response
from datetime import date
from os import mkdir
from operator import __and__
from functools import reduce
from .forms import *
from .models import *


TESTIMONIALS_ON_PAGE = 8
TESTIMONIALS_ON_ADMIN_PAGE = 8
USERS_ON_PAGE = 25


# @method_decorator(user_can_decorator(['custom_permission_1']), name='dispatch')  # Decorator use example
class MainPage(TemplateView):
    template_name = 'base.html'


class LoginPage(TemplateView):
    template_name = 'app/login_page.html'


class AccessRequired(TemplateView):
    template_name = 'app/access_required_page.html'


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
    template_name = "app/testimonials.html"
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


@method_decorator(user_can_decorator(['testimonials_admin']), name='dispatch')
class TestimonialsAdmin(ListView):
    model = Testimonial
    template_name = "app/testimonials_admin.html"
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
    if request.user.is_staff():
        q.is_moderated = True
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
    if request.user.is_staff():
        q.is_moderated = True
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


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


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


class SiteAdmin(TemplateView):
    template_name = 'app/site_admin.html'


@method_decorator(user_can_decorator(['admin_users']), name='dispatch')
class AdminUsers(ListView):
    model = User
    template_name = "app/admin_users.html"
    context_object_name = "users"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_used = False

    def get_queryset(self):
        return User.objects.filter(useryoga__is_admin=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_used'] = self.login_used
        self.login_used = False
        return context

    def post(self, request):
        if 'save' in request.POST:
            new_user = request.POST['username']
            if len(User.objects.filter(username=new_user)) > 0:  # Check if username is already used
                self.login_used = True
                return self.get(self, request)
            new_user = User(username=new_user)
            new_user.set_password(request.POST['password'])
            new_user.save()
            useryoga = UserYoga.objects.get(user=new_user)
            useryoga.is_admin = True
            useryoga.auth_by_sn = False
            useryoga.save()
            return HttpResponseRedirect(reverse('app:edit_admin_user', args=(new_user.id,)))
        return self.get(self, request)


@method_decorator(user_can_decorator(['admin_users']), name='dispatch')
class EditAdminUser(TemplateView):
    model = User
    template_name = "app/edit_admin_user.html"
    context_object_name = "user_obj"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_used = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user_obj = User.objects.get(pk=self.kwargs['user_id'])
            context['user_obj'] = user_obj
            context['blog_admin'] = user_obj.has_perm('app.blog_admin')
            context['portfolio_admin'] = user_obj.has_perm('app.portfolio_admin')
            context['testimonials_admin'] = user_obj.has_perm('app.testimonials_admin')
            context['projects_admin'] = user_obj.has_perm('app.projects_admin')
            context['user_messages'] = user_obj.has_perm('app.user_messages')
            context['admin_users'] = user_obj.has_perm('app.admin_users')
            context['general_users'] = user_obj.has_perm('app.general_users')
            context['user_exist'] = True
            context['login_used'] = self.login_used
            self.login_used = False
        except User.DoesNotExist:
            context['user_exist'] = False
        return context

    def post(self, request, user_id=None):
        try:
            user_obj = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('app:admin_users'))

        if 'change_pass' in request.POST:
            new_pass = request.POST['password']
            user_obj.set_password(new_pass)
            return HttpResponseRedirect(reverse('app:admin_users'))

        elif 'delete' in request.POST:
            user_obj.delete()
            return HttpResponseRedirect(reverse('app:admin_users'))

        elif 'save' in request.POST:
            new_username = request.POST['username']
            if len(User.objects.filter(~Q(pk=user_id), Q(username=new_username))) > 0:  # Check if login is already used
                self.login_used = True
                return self.get(request)
            user_obj.username = request.POST['username']
            user_obj.first_name = request.POST['first_name']
            user_obj.last_name = request.POST['last_name']
            user_obj.email = request.POST['email']
            perm_list = []
            for perm in ['blog_admin', 'portfolio_admin', 'testimonials_admin', 'projects_admin',
                         'user_messages', 'admin_users', 'general_users']:
                if perm in request.POST:
                    perm_list.append(Permission.objects.get(codename=perm))
            user_obj.user_permissions.set(perm_list)
            user_obj.save()
            return HttpResponseRedirect(reverse('app:admin_users'))
        else:
            return HttpResponseRedirect(reverse('app:admin_users'))


@method_decorator(user_can_decorator(['general_users']), name='dispatch')
class GeneralUsers(ListView):  # View and fast create general user
    model = User
    template_name = "app/general_users.html"
    context_object_name = "users"
    paginate_by = USERS_ON_PAGE

    def __init__(self):
        super().__init__()
        self.login_used = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_used'] = self.login_used
        if len(context['users']) <= 0:
            context['no_found'] = True
        self.login_used = False
        return context

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'username')
        order_desc = self.request.GET.get('order_desc', 'false')
        auth_by_sn = self.request.GET.get('auth_by_sn', 'any')
        search_q = self.request.GET.get('search', None)
        is_active = self.request.GET.get('is_active', 'true')
        q_builder = [Q(useryoga__is_admin=False)]
        if order_by == 'first_name':
            order_by = '{0}first_name'.format('-' if order_desc == 'true' else '')
        elif order_by == 'last_name':
            order_by = '{0}last_name'.format('-' if order_desc == 'true' else '')
        else:
            order_by = '{0}username'.format('-' if order_desc == 'true' else '')

        if search_q:
            try:
                search_q = int(search_q)
                q_builder.append(Q(pk=search_q))
            except ValueError:
                q_builder.append((Q(username=search_q) | Q(first_name=search_q) | Q(last_name=search_q)))

        if auth_by_sn == 'true':
            q_builder.append(Q(useryoga__auth_by_sn=True))
        elif auth_by_sn == 'false':
            q_builder.append(Q(useryoga__auth_by_sn=False))

        if is_active == 'false':
            q_builder.append(Q(is_active=False))
        elif is_active == 'true':
            q_builder.append(Q(is_active=True))

        return User.objects.filter(reduce(__and__, q_builder)).order_by(order_by)

    def post(self, request):  # Create new general user
        if 'save' in request.POST:
            new_user = request.POST['username']
            print(User.objects.filter(username=new_user))
            if len(User.objects.filter(username=new_user)) > 0:  # Check if username is already used
                self.login_used = True
                return self.get(self, request)
            new_user = User(username=new_user)
            new_user.set_password(request.POST['password'])
            new_user.save()
            useryoga = UserYoga.objects.get(user=new_user)
            useryoga.is_admin = False
            useryoga.auth_by_sn = False
            useryoga.save()
            return HttpResponseRedirect(reverse('app:edit_general_user', args=(new_user.id,)))
        elif 'search' in request.POST:
            search_q = request.POST['search_q']
            return HttpResponseRedirect(reverse('app:general_users')+args_builder(request, ['order_by', 'order_desc'])
                                        + '&search={0}'.format(search_q))
        elif 'reset' in request.POST:
            return HttpResponseRedirect(reverse('app:general_users') + args_builder(request, ['order_by', 'order_desc']))
        return HttpResponseRedirect(reverse('app:general_users'))


@method_decorator(user_can_decorator(['general_users']), name='dispatch')
class EditGeneralUser(TemplateView):  # Edit general user
    model = User
    template_name = "app/edit_general_user.html"
    context_object_name = "user_obj"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_used = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user_obj = User.objects.get(pk=self.kwargs['user_id'])
            context['user_obj'] = user_obj
            context['user_exist'] = True
            context['login_used'] = self.login_used
            self.login_used = False
        except User.DoesNotExist:
            context['user_exist'] = False
        return context

    def post(self, request, user_id=None):
        try:
            user_obj = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('app:general_users'))

        if 'change_pass' in request.POST:
            new_pass = request.POST['password']
            user_obj.set_password(new_pass)
            return HttpResponseRedirect(reverse('app:general_users'))

        elif 'save' in request.POST:
            new_username = request.POST['username']
            if len(User.objects.filter(~Q(pk=user_id), Q(username=new_username))) > 0:  # Check if login is already used
                self.login_used = True
                return self.get(request)
            user_obj.username = request.POST['username']
            user_obj.first_name = request.POST['first_name']
            user_obj.last_name = request.POST['last_name']
            user_obj.email = request.POST['email']
            if "is_active" in request.POST:
                user_obj.is_active = True
            else:
                user_obj.is_active = False
            user_obj.save()
            return HttpResponseRedirect(reverse('app:general_users'))
        else:
            return HttpResponseRedirect(reverse('app:general_users'))


class PortfolioListView(ListView):
    """02.03.2017 Taras  this list returns all Portfolio projects of our agency """
    template_name = 'app/portfolio.html'
    # paginate_by = 4

    def get_queryset(self):
        return PortfolioContent.objects.all()


class PortfolioDetailView(DetailView):
    """02.03.2017 Taras this is detail portfolio view of concrete project"""
    model = PortfolioContent
    template_name = 'app/portfolio_detail.html'


def register(request): # 06.03.2017 Taras need to edit later
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        yoga_form = YogaUserForm(data=request.POST)

        if user_form.is_valid() and yoga_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = yoga_form.save(commit=False)
            profile.user = user
            registered = True
        else:
            print(user_form.errors, yoga_form.errors)
    else:
        user_form = UserForm()
        yoga_form = YogaUserForm()
    return render(request, 'registration/registration_form.html',
                              {'user_form': user_form, 'profile_form': yoga_form, 'registered': registered}, context)
