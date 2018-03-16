from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.context import RequestContext
from online_status.utils import OnlineStatusJSONEncoder
from online_status.conf import online_status_settings as config


def users(request):
    """
    Json of online users, useful f.ex. for refreshing a online users list via
    an ajax call or something
    """
    online_users = cache.get(config.CACHE_USERS)
    return JsonResponse(
        online_users, encoder=OnlineStatusJSONEncoder, safe=False
    )


def example(request):
    """Example view where you can see templatetags in action"""
    User = get_user_model()
    user, created = User.objects.get_or_create(username='example')
    return render(
        request, 'online_status/example.html', context={'example_user': user})


def test(request):
    """Dummy view for test purpose"""
    return HttpResponse('test')
