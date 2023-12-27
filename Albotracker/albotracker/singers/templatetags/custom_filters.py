from django import template

register = template.Library()


@register.filter(name='group_exists')
def group_exists(user, group_name):
    return user.groups.filter(name=group_name).exists()