from django.conf.urls import patterns, url
from products import views

urlpatterns = patterns(
    '',
    url(r'^keyword', views.KeywordView.as_view(), name='keyword'),
    url(r'^titlekey', views.TitleKeyView.as_view(), name='titlekey'),
    url(r'^capture', views.CaptureView.as_view(), name='capture'),
    url(r'^tracking', views.TrackingListView.as_view(), name='tracking'),
    url(r'^update_by_model', views.UpdateByModel.as_view(), name='updating')
)
