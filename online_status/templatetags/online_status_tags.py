from datetime import timedelta
from django import template
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from django.contrib.sessions.models import Session
from online_status.status import status_for_user
from online_status.conf import online_status_settings as config

register = template.Library()


@register.inclusion_tag('online_status/online_users.html')
def online_users(limit=None):
    """Renders a list of OnlineStatus instances"""
    onlineusers = cache.get(config.CACHE_USERS)
    onlineanonymusers = None

    if not config.ONLY_LOGGED_USERS:
        now = timezone.now()

        expire_delta = timedelta(
            0, settings.SESSION_COOKIE_AGE - config.TIME_OFFLINE
        )
        sessions = Session.objects.filter(
            expire_date__gte=now + expire_delta
        ).values_list('session_key', flat=True)

        onlineanonymusers = filter(
            lambda x: x is not None,
            [cache.get(config.CACHE_PREFIX_ANONYM_USER % session_key, None)
             for session_key in sessions]
        )

        onlineusers = [item
                       for item in cache.get(config.CACHE_USERS, [])
                       if item.status in (0, 1) and item.session in sessions]

        if onlineanonymusers and limit:
            onlineanonymusers = onlineanonymusers[:limit]

    if onlineusers and limit:
        onlineusers = onlineusers[:limit]
    return {'onlineanonymusers': onlineanonymusers,
            'onlineusers': onlineusers, }


@register.inclusion_tag('online_status/user_status.html')
def user_status(user):
    """Renders an OnlineStatus instance for User"""
    status = status_for_user(user)
    return {'onlinestatus': status, }


@register.inclusion_tag('online_status/user_status_tag.html')
def user_status_tag(user):
    status = status_for_user(user)
    return {'onlinestatus': status, }
