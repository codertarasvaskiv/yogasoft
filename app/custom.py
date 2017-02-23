from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

LOGIN_PAGE = 'app:login_page'
ACCESS_REQUIRED_PAGE = 'app:access_required_page'
APP_NAME = "app"


def user_in_group(user, group_list):    # Returns true if user is one of specified groups
    if user.is_authenticated():
        user_groups = user.groups.values_list('name', flat=True)
        for group in group_list:
            if group in user_groups:
                return True
        return False
    return False


def user_can(user, permission_list):   # Returns true if user has one of specified permissions
    if user.is_authenticated():
        user_permissions = user.user_permissions.values_list('codename', flat=True)
        for permission in permission_list:
            if permission in user_permissions:
                return True
    return False


def user_groups(user):
    return user.groups.values_list('name', flat=True)


def user_permissions(user):
    return user.user_permissions.values_list('codename', flat=True)


def in_group_decorator(group_list,  optional_redirect=None):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if request.user.is_authenticated():
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


def user_can_decorator(permission_list,  optional_redirect=None):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if request.user.is_authenticated():
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
