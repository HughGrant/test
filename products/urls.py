from django.conf.urls import patterns, url
from products import views

urlpatterns = patterns(
    '',
    url(r'^keyword', views.KeywordView.as_view(), name='keyword'),
    url(r'^capture', views.CaptureView.as_view(), name='capture')
)
