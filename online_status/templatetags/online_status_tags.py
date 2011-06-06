from django import template
from django.core.cache import cache
from online_status.status import CACHE_USERS, status_for_user

register = template.Library()


@register.inclusion_tag('online_status/online_users.html')
def online_users(limit=None):
    """Renders a list of OnlineStatus instances"""
    onlineusers = cache.get(CACHE_USERS)
    if onlineusers and limit:
        onlineusers = onlineusers[:limit]
    return {'onlineusers': onlineusers,}


@register.inclusion_tag('online_status/user_status.html')
def user_status(user):
    """Renders an OnlineStatus instance for User"""
    status = status_for_user(user)
    return {'onlinestatus': status,}

@register.inclusion_tag('online_status/user_status_tag.html')
def user_status_tag(user):
    status = status_for_user(user)
    return {'onlinestatus': status,}