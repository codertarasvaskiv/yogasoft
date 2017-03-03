from django.template import Library

register = Library()


@register.inclusion_tag('base.html')
def popular_tags():
    tags = Tag.objects.all()[10]
    return {'tags': tags}
