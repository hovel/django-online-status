from datetime import datetime
from django.core.cache import cache
from django.conf import settings


TIME_IDLE = getattr(settings, 'USERS_ONLINE__TIME_IDLE', 60*5)
TIME_OFFLINE = getattr(settings, 'USERS_ONLINE__TIME_OFFLINE', 60*10)

CACHE_PREFIX_USER = getattr(settings, 'USERS_ONLINE__CACHE_PREFIX_USER', 'online_user') + '_%d'
CACHE_USERS = getattr(settings, 'USERS_ONLINE__CACHE_USERS', 'online_users')


class OnlineStatus(object):
    """Online status data which will be later cached"""
    
    def __init__(self, request):
        self.user = request.user
        # 0 - idle, 1 - active
        self.status = 1
        self.seen = datetime.now() 
        self.ip = request.META['REMOTE_ADDR']
        self.session = request.session.session_key

    def set_idle(self):
        self.status = 0        

    def set_active(self):
        self.status = 1
        self.seen = datetime.now() 
        


def refresh_user(request):
    """Sets or updates user's online status"""
    key = CACHE_PREFIX_USER % request.user.pk
    onlinestatus = cache.get(key)
    if not onlinestatus:
        onlinestatus = OnlineStatus(request)        
    else:
        onlinestatus.set_active()
    cache.set(key, onlinestatus, TIME_OFFLINE)
    return onlinestatus
    #self.refresh_users_list(user=self.user)
    
    
def refresh_users_list(**kwargs):
    """Updates online users list and their statuses"""
    updated = kwargs.pop('updated', None)
    online_users = cache.get(CACHE_USERS)        
    if not online_users:
        online_users = []
    updated_found = False
    for obj in online_users:
        seconds = (datetime.now() - obj.seen).seconds
        if seconds > TIME_OFFLINE:
            online_users.remove(obj)
            cache.delete(CACHE_PREFIX_USER % obj.user.pk)
        elif seconds > TIME_IDLE:
            obj.set_idle()
            user = cache.get(CACHE_PREFIX_USER % obj.user.pk)
            user.set_idle()
            cache.set(CACHE_PREFIX_USER % obj.user.pk, user, TIME_OFFLINE)
        if obj.user == updated.user:
            obj.set_active()
            obj.seen = datetime.now()    
            updated_found = True
    if not updated_found:
        online_users.append(updated)    
    cache.set(CACHE_USERS, online_users, TIME_OFFLINE)
    

def status_for_user(user):
    """Return status for user, duh?"""
    if user.is_authenticated():
        key = CACHE_PREFIX_USER % user.pk
        return cache.get(key)
    return None

