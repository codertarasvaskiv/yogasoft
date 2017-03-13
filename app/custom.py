from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

LOGIN_PAGE = 'app:index_page'  # Where to redirect if user is not login
ACCESS_REQUIRED_PAGE = 'app:access_required_page'  # Where to redirect if user is not permitted to access this  page
APP_NAME = "app"  # Application name


def user_in_group(user, group_list):    # Returns true if user is in the one of specified groups (accepts list)
    if user.is_authenticated():
        user_groups = user.groups.values_list('name', flat=True)
        for group in group_list:
            if group in user_groups:
                return True
        return False
    return False


def user_can(user, permission_list):   # Returns true if user has one of specified permissions (accepts list)
    if user.is_authenticated():
        user_permissions = user.user_permissions.values_list('codename', flat=True)
        for permission in permission_list:
            if permission in user_permissions:
                return True
    return False


def user_groups(user):  # Returns user groups list
    return user.groups.values_list('name', flat=True)


def user_permissions(user):  # Returns user permissions list
    return user.user_permissions.values_list('codename', flat=True)


def in_group_decorator(group_list,  optional_redirect=None, superuser_allowed=True):  # Checks if user is logined and in specified group
    def decorator(func):                                                                # accepts list
        def inner(request, *args, **kwargs):
            if request.user.is_authenticated():
                if request.user.is_superuser and superuser_allowed:
                    return func(request, *args, **kwargs)
                user_groups = request.user.groups.values_list('name', flat=True)
                for group in group_list:
                    if group in user_groups:
                        return func(request, *args, **kwargs)
                else:
                    if optional_redirect is not None:
                        return HttpResponseRedirect(reverse(optional_redirect))
                    else:
                        return HttpResponseRedirect(reverse(ACCESS_REQUIRED_PAGE))
            else:
                return HttpResponseRedirect(reverse(LOGIN_PAGE))
        return inner
    return decorator


def user_can_decorator(permission_list,  optional_redirect=None, superuser_allowed=True):  # Checks if user is logined and has permissions
    def decorator(func):                                                                    # accepts list
        def inner(request, *args, **kwargs):
            if request.user.is_authenticated():
                if request.user.is_superuser and superuser_allowed:
                    return func(request, *args, **kwargs)
                user_permissions = request.user.user_permissions.values_list('codename', flat=True)
                for permission in permission_list:
                    if permission in user_permissions:
                        return func(request, *args, **kwargs)
                else:
                    if optional_redirect is not None:
                        return HttpResponseRedirect(reverse(optional_redirect))
                    else:
                        return HttpResponseRedirect(reverse(ACCESS_REQUIRED_PAGE))
            else:
                return HttpResponseRedirect(reverse(LOGIN_PAGE))
        return inner
    return decorator


def args_builder(reques, args_list):
    args_string = '?'
    for arg in args_list:
        arg_data = reques.GET.get(arg, False)
        if arg_data:
            args_string += '{0}={1}&'.format(arg, arg_data)
    return args_string
