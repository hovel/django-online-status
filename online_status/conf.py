from django.conf import settings


class OnlineStatusSettings(object):
    @property
    def TIME_IDLE(self):
        return getattr(settings, 'USERS_ONLINE__TIME_IDLE', 60 * 5)

    @property
    def TIME_OFFLINE(self):
        return getattr(settings, 'USERS_ONLINE__TIME_OFFLINE', 60 * 10)

    @property
    def CACHE_USERS(self):
        return getattr(settings, 'USERS_ONLINE__CACHE_USERS', 'online_users')

    @property
    def CACHE_PREFIX_USER(self):
        return getattr(settings, 'USERS_ONLINE__CACHE_PREFIX_USER',
                       'online_user') + '_%d'

    @property
    def CACHE_PREFIX_ANONYM_USER(self):
        return getattr(settings, 'USERS_ONLINE__CACHE_PREFIX_ANONYM_USER',
                       'online_anonym_user') + '_%s'

    @property
    def ONLY_LOGGED_USERS(self):
        return getattr(settings, 'USERS_ONLINE__ONLY_LOGGED_USERS', False)


online_status_settings = OnlineStatusSettings()
