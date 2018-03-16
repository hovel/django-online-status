# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.cache import cache

from online_status.conf import online_status_settings as config
from online_status.status import refresh_user, refresh_users_list, OnlineStatus


class OnlineStatusMiddleware(object):
    """Cache OnlineStatus instance for an authenticated User"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.set_status(request)

        response = self.get_response(request)

        return response

    def set_status(self, request):
        if request.user.is_authenticated:
            onlinestatus = cache.get(
                config.CACHE_PREFIX_USER % request.user.pk)
        elif not config.ONLY_LOGGED_USERS:
            onlinestatus = cache.get(
                config.CACHE_PREFIX_ANONYM_USER % request.session.session_key)
        else:
            return

        if not onlinestatus:
            onlinestatus = OnlineStatus(request)

        refresh_user(request)
        refresh_users_list(request, updated=onlinestatus)
