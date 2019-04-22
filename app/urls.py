from django.urls import path
from app import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',views.index,name='index'),
    path('results',views.results,name='results'),
]

urlpatterns += staticfiles_urlpatterns()

