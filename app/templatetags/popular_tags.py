from django.template import Library
from app.models import Tag

register = Library()


@register.inclusion_tag('app/tagcloud.html')
def popular_tags():

    context = list(Tag.objects.all())

    return {'tags': context}


@register.simple_tag()
def q_transform(request, **kwargs):
    updated = request.GET.copy()
    for key, value in kwargs.items():
        updated[key] = value
    return '?' + updated.urlencode()