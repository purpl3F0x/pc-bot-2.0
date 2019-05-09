from django.conf.urls import include, url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pc/<int:id>/', views.pc, name='pc'),
    url(r'^markdownx/', include('markdownx.urls')),

]
