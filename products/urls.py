from django.conf.urls import url
from products import views

urlpatterns = [
    url(r'^keyword', views.TitleKeywordView.as_view(), name='titlekeyword'),
    url(r'^capture', views.CaptureView.as_view(), name='capture'),
    url(r'^update_by_model', views.UpdateByModel.as_view(), name='updating'),
]
