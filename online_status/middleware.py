from django.core.cache import cache
from online_status.status import refresh_user, refresh_users_list
from status import OnlineStatus, CACHE_PREFIX_USER


class OnlineStatusMiddleware(object):
    """Cache OnlineStatus instance for an authenticated User"""
    
    def process_request(self, request):
        if not request.user.is_authenticated():
            return
        onlinestatus = cache.get(CACHE_PREFIX_USER % request.user.pk)
        if not onlinestatus:
            onlinestatus = OnlineStatus(request)
        refresh_user(request)
        refresh_users_list(updated=onlinestatus)
        return
        
