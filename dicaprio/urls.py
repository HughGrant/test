from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import View
# from django.utils.decorators import method_decorator


class ChromeLoginView(View):

    def get(self, request):
        return JsonResponse({'status': request.user.is_authenticated()})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'status': True})
        return JsonResponse({'status': False})


def user_logout(request):
    logout(request)
    return JsonResponse({'status': True})

urlpatterns = patterns(
    '',
    url(r'^products/', include('products.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chrome_login/',
        csrf_exempt(ChromeLoginView.as_view()), name='chrome_login'),
    url(r'^logout/', user_logout, name='user_logout'),
)
