from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from .custom import user_can_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.utils.decorators import method_decorator
from django.http import StreamingHttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from shutil import rmtree
from django.db.models import Q
from mimetypes import MimeTypes
from os.path import join, abspath, getsize, exists
from django.shortcuts import redirect, render
from datetime import date
from os import mkdir, listdir, chdir, getcwd
from .forms import *
from .models import *

import PIL.Image
from wsgiref.util import FileWrapper
from itertools import chain
import zipfile

TESTIMONIALS_ON_PAGE = 8
TESTIMONIALS_ON_ADMIN_PAGE = 8


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
    """ View that is responsible for main page """
    template_name = 'app/index.html'
    form_class = StartProjectForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        """ Post method that handles files, when user starts new project """
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
                if str(f).endswith('.exe'):
                    continue
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
    """ View that is responsible for testimonials page """
    model = Testimonial
    template_name = "app/testimonials.html"
    paginate_by = TESTIMONIALS_ON_PAGE
    context_object_name = "testimonials"

    def get_queryset(self):
        return Testimonial.objects.filter(is_moderated=True).order_by('-date')

    @staticmethod
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

    @staticmethod
    def post(self, request, testimonial_id=None):
        view_moderated = request.GET.get('mod', 'all')
        page = request.GET.get('page', 1)

        if 'moderated' in request.POST:
            try:
                testimonial = Testimonial.objects.get(pk=testimonial_id)
                testimonial.is_moderated = True
                testimonial.save()
            except Testimonial.DoesNotExist:
                return HttpResponseRedirect(reverse('app:testimonials_admin') + '?mod={0}&page={1}'
                                            .format(view_moderated, page))
            return HttpResponseRedirect(reverse('app:testimonials_admin') + '?mod={0}&page={1}'
                                        .format(view_moderated, page))

        elif 'delete' in request.POST:
            try:
                testimonial = Testimonial.objects.get(pk=testimonial_id)
                testimonial.delete()
            except Testimonial.DoesNotExist:
                return HttpResponseRedirect(reverse('app:testimonials_admin') + '?mod={0}&page={1}'
                                            .format(view_moderated, page))
            return HttpResponseRedirect(reverse('app:testimonials_admin') + '?mod={0}&page={1}'
                                        .format(view_moderated, page))

        elif 'save' in request.POST:
            author_name = request.POST['author_name']
            author_email = request.POST['author_email']
            message = request.POST['message']
            new_tstm = Testimonial(author_name=author_name, author_email=author_email, message=message)
            new_tstm.save()
            return HttpResponseRedirect(reverse('app:testimonials_admin') + '?mod={0}&page={1}'
                                        .format(view_moderated, page))
        else:
            return HttpResponseRedirect(reverse('app:testimonials_admin') + '?mod={0}&page={1}'
                                        .format(view_moderated, page))


class BlogDetailView(DetailView):
    """ View that is responsible for blog page """
    model = BlogPost
    template_name = 'app/blog.html'

    def get_context_data(self, **kwargs):
        """ Method that collects all comments for current blog """
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        blog_post = context['object']
        context['tags'] = blog_post.tags.all()
        comments = blog_post.comment_set.all()
        context['comments'] = {}
        for i in comments:
            if i.is_moderated:
                context['comments'][i] = list(CommentSecondLevel.objects.filter(father_comment=i))
                print(CommentSecondLevel.objects.filter(id=1))
                print('*'*50)
                for j in context['comments'][i]:
                    if not j.is_moderated:
                        context['comments'][i].pop(context['comments'][i].index(j))
        context['form'] = CommentForm()
        context.pop('blogpost')
        return context


def add_comment(request, pk):
    """ Function that handles comment adding """
    data = request.POST
    if request.user.is_authenticated():
        q = Comment(author_email=request.user.email, author_name=request.user)
    else:
        q = Comment(author_email=data['author_email'], author_name=data['author_name'])
    q.message = data['message']
    q.blog = BlogPost.objects.get(pk=pk)
    if request.user.is_staff:  # if admin, no need for other admin to moderate
        q.is_moderated = True
    q.save(q)
    return redirect('app:blog_detail_view', pk)


def add_second_comment(request, pk, comm_pk):
    """ Function that handles second level comment adding """
    data = request.POST
    print(request.user)
    if request.user.is_authenticated():
        q = CommentSecondLevel(author_email=request.user.email, author_name=request.user)
    else:
        q = CommentSecondLevel(author_email=data['author_email'], author_name=data['author_name'])
    q.message = data['message']
    q.father_comment = Comment.objects.get(pk=comm_pk)
    if request.user.is_staff:  # if admin, no need for other admin to moderate
        q.is_moderated = True
    q.save(q)
    return redirect('app:blog_detail_view', pk)


class BlogListView(ListView):
    """ View that is responsible for blog list page """
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
    """ View that is responsible for feedback page """
    template_name = 'app/contact_us.html'
    form_class = ContactUsForm
    success_url = "/"

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
                return render(request, '/', {}, context)
            else:
                return render(request, '/', {}, context)
        else:
            print("Invalid login details: {}, {}".format(username, password))
            return render(request, '/', {})
    else:
        return render(request, '/', {}, context)


class SiteAdmin(TemplateView):
    template_name = 'app/site_admin.html'

    def get_context_data(self, **kwargs):
        context = dict()
        context['new_comments'] = len(Comment.objects.filter(is_moderated=False)) + \
                                  len(CommentSecondLevel.objects.filter(is_moderated=False))
        context['new_testimonials'] = len(Testimonial.objects.filter(is_moderated=False))
        context['opened_projects'] = len(Project.objects.filter(is_opened=True))
        context['new_feedback'] = len(ContactUsModel.objects.filter(is_new=True))
        return context


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
class GeneralUsers(ListView):
    model = User
    template_name = "app/general_users.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.filter(useryoga__is_admin=False)

    @staticmethod
    def post(self, request):
        if 'save' in request.POST:
            new_user = request.POST['username']
            if len(User.objects.filter(username=new_user)) > 0:  # Check if username is already used
                return HttpResponseRedirect(reverse('app:admin_users'))
            new_user = User(username=new_user)
            new_user.set_password(request.POST['password'])
            new_user.save()
            useryoga = UserYoga.objects.get(user=new_user)
            useryoga.is_admin = True
            useryoga.auth_by_sn = False
            useryoga.save()
            return HttpResponseRedirect(reverse('app:edit_admin_user', args=(new_user.id,)))
        return HttpResponseRedirect(reverse('app:admin_users'))


class PortfolioListView(ListView):
    """02.03.2017 Taras  this list returns all Portfolio projects of our agency """
    template_name = 'app/portfolio.html'

    # paginate_by = 4

    def get_queryset(self):
        return PortfolioContent.objects.all()

    def get_context_data(self, **kwargs):
        q = super().get_context_data()
        _list = list(q['object_list'])
        new_list = list(zip(_list[::2], _list[1::2]))
        if len(_list) % 2:
            new_list.append((_list[-1], None))
        q['object_list'] = new_list
        return q


class PortfolioDetailView(DetailView):
    """02.03.2017 Taras this is detail portfolio view of concrete project"""
    model = PortfolioContent
    template_name = 'app/portfolio_detail.html'


def register(request):  # 06.03.2017 Taras need to edit later
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
    return render(request, 'registration/registration_form.html', {'user_form': user_form, 'profile_form': yoga_form,
                                                                   'registered': registered}, context)


class AdminBlogList(ListView):
    model = BlogPost
    template_name = 'app/admin_blog_list.html'


class CreateBlogPost(CreateView):
    model = BlogPost
    form_class = CreateBlogForm
    template_name = "app/create_blog_post.html"

    def post(self, request, *args, **kwargs):
        data = request.POST
        q = BlogPost(name=data['name'], text=data['text'], nameUA=data['nameUA'], textUA=data['textUA'],
                     author=User.objects.get(username=request.user))
        q.save()
        q.tags = []
        for i in request.POST.getlist('tags'):
            q.tags.add(Tag.objects.get(id=i))
        q.save()
        for i in request.FILES.getlist('file'):
            img = BlogPostImage(image=i, content=q)
            img.save()
        return redirect("/")


class ChangeBlogPost(UpdateView):
    model = BlogPost
    fields = ['text', 'textUA', 'tags']
    template_name = "app/blog_update.html"
    success_url = "/"


class BlogPostDelete(DeleteView):
    model = BlogPost
    success_url = "/"
    template_name = 'app/confirm_delete.html'


class ProjectsListView(ListView):
    model = Project
    template_name = "app/projects_list.html"


class ProjectDetailView(DetailView):
    model = Project
    template_name = "app/project_view.html"

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
            try:
                context['files'] = [join(str(i)) for i in listdir(self.object.file)]
            except FileNotFoundError:
                context['files'] = ['There is no files']
        context.update(kwargs)
        return super(ProjectDetailView, self).get_context_data(**context)


def project_file_download(request, pk, file):
    pth = Project.objects.get(id=pk).file
    back = getcwd()
    chdir(pth)
    mime = MimeTypes()
    resp = StreamingHttpResponse(FileWrapper(open(file, 'rb'), 8192), content_type=mime.guess_type(url=file))
    resp['Content-Length'] = getsize(file)
    resp["Content-Disposition"] = "attachment; filename=" + file
    chdir(back)
    return resp


def project_all_files_download(request, pk):
    pth = Project.objects.get(id=pk).file
    back = getcwd()
    chdir(pth)
    files = listdir(pth)
    zip_filename = "".join(("project", str(pk), ".zip"))
    if not exists(zip_filename):
        with zipfile.ZipFile(zip_filename, "w") as zf:
            for i in files:
                zf.write(str(i))

    resp = StreamingHttpResponse(FileWrapper(open(zip_filename, 'rb'), 8192), content_type="application/zip-file")
    resp['Content-Length'] = getsize(zip_filename)
    resp["Content-Disposition"] = "attachment; filename=" + zip_filename
    chdir(back)
    return resp


class ProjectDelete(DeleteView):
    model = Project
    success_url = '/'
    template_name = "app/confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            rmtree(self.object.file)
        except FileNotFoundError:
            pass
        self.object.delete()
        return HttpResponseRedirect(success_url)


def close_project(request, pk):
    z = Project.objects.get(id=pk)
    z.is_opened = False
    z.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class SearchListAsView(ListView):
    """ this class is responsible for search

    It searchs blog posts on info that user inputs, It uses Ajax queries
    """
    template_name = 'app/ajax_list_view.html'
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super(SearchListAsView, self).get_context_data(**kwargs)
        # here we can add some additional context
        context.update({
            'tag_list': None,
        })
        return context

    def get_queryset(self):
        return BlogPost.objects.filter(Q(name__contains=self.kwargs['info']) | Q(text__contains=self.kwargs['info']))


class CreatePortfolio(CreateView):
    model = PortfolioContent
    form_class = CreatePortfolio
    template_name = "app/create_portfolio.html"

    def post(self, request, *args, **kwargs):

        data = request.POST
        q = PortfolioContent(name=data['name'], description=data['description'], nameUA=data['nameUA'],
                             descriptionUA=data['descriptionUA'], technologies=data['technologies'],
                             link=data['link'], client=data['client'])
        q.save()
        q.tags = []
        for i in request.POST.getlist('tags'):
            q.tags.add(Tag.objects.get(id=i))
        q.save()
        for i in request.FILES.getlist('file'):
            img = ImageContentClass(image=i, content=q)
            img.save()
        return redirect("/")


class PortfolioAdminList(ListView):
    model = PortfolioContent
    template_name = "app/portfolio_admin_list.html"


class PortfolioDelete(DeleteView):
    model = PortfolioContent
    success_url = '/'
    template_name = "app/confirm_delete.html"


class ChangePortfolio(UpdateView):
    UpdateView.model = PortfolioContent
    UpdateView.fields = ['name', 'nameUA', 'description', 'descriptionUA', 'tags', "technologies", 'link', 'client']
    UpdateView.template_name = "app/portfolio_update.html"
    success_url = "/"


class CommentsAdmin(ListView):
    model = Comment
    template_name = 'app/comments_admin.html'
    context_object_name = 'comments'
    paginate_by = 10

    def get_queryset(self):
        if 'mod' in self.request.GET:
            view_moderated = self.request.GET['mod']
            if view_moderated == 'true':
                return list(chain(Comment.objects.filter(is_moderated=True).order_by('-id'),
                                  CommentSecondLevel.objects.filter(is_moderated=True).order_by('-id')))
            elif view_moderated == 'false':
                return list(chain(Comment.objects.filter(is_moderated=False).order_by('-id'),
                                  CommentSecondLevel.objects.filter(is_moderated=False).order_by('-id')))
            else:
                return list(
                    chain(Comment.objects.all().order_by('-id'), CommentSecondLevel.objects.all().order_by('-id')))
        else:
            return list(chain(Comment.objects.all().order_by('-id'), CommentSecondLevel.objects.all().order_by('-id')))


def moderate_comment(request, pk):
    q = Comment.objects.get(id=pk)
    q.is_moderated = True
    q.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def moderate_sec_comment(request, pk):
    q = CommentSecondLevel.objects.get(id=pk)
    q.is_moderated = True
    q.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def delete_comment(request, pk):
    q = Comment.objects.get(id=pk)
    q.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def delete_sec_comment(request, pk):
    q = CommentSecondLevel.objects.get(id=pk)
    q.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
