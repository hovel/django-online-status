from django.utils import timezone
from django.core.cache import cache
from online_status.conf import online_status_settings as config


class OnlineStatus(object):
    """Online status data which will be later cached"""

    def __init__(self, request):
        self.user = request.user
        # 0 - idle, 1 - active
        self.status = 1
        self.seen = timezone.now()
        self.ip = request.META['REMOTE_ADDR']
        self.session = request.session.session_key

    def set_idle(self):
        self.status = 0

    def set_active(self, request):
        self.status = 1
        self.seen = timezone.now()
        # Can change if operating from multiple browsers
        self.session = request.session.session_key
        # Can change if operating from multiple browsers
        self.ip = request.META['REMOTE_ADDR']


def refresh_user(request):
    """Sets or updates user's online status"""
    if request.user.is_authenticated():
        key = config.CACHE_PREFIX_USER % request.user.pk
    elif not config.ONLY_LOGGED_USERS:
        key = config.CACHE_PREFIX_ANONYM_USER % request.session.session_key
    else:
        return
    onlinestatus = cache.get(key)
    if not onlinestatus:
        onlinestatus = OnlineStatus(request)
    else:
        onlinestatus.set_active(request)
    cache.set(key, onlinestatus, config.TIME_OFFLINE)
    return onlinestatus
    # self.refresh_users_list(user=self.user)


def refresh_users_list(request, **kwargs):
    """Updates online users list and their statuses"""

    online_users = cache.get(config.CACHE_USERS) or []
    updated = kwargs.pop('updated', None)

    for online_status in online_users:
        seconds = (timezone.now() - online_status.seen).seconds

        if online_status.user == updated.user:
            online_users.remove(online_status)
            # don't delete user status from cache, because it's already updated
            continue

        if seconds > config.TIME_OFFLINE:
            online_users.remove(online_status)
            cache.delete(config.CACHE_PREFIX_USER % online_status.user.pk)
            continue

        if seconds > config.TIME_IDLE:
            user_status = cache.get(config.CACHE_PREFIX_USER %
                                    online_status.user.pk)
            if not user_status:
                online_users.remove(online_status)
                # user status already deleted from cache
                continue

            online_status.set_idle()
            user_status.set_idle()
            cache.set(config.CACHE_PREFIX_USER % online_status.user.pk,
                      user_status, config.TIME_OFFLINE)

    if updated.user.is_authenticated():
        online_users.append(updated)

    cache.set(config.CACHE_USERS, online_users, config.TIME_OFFLINE)


def status_for_user(user):
    """Return status for user, duh?"""
    if user.is_authenticated():
        key = config.CACHE_PREFIX_USER % user.pk
        return cache.get(key)
    return None
