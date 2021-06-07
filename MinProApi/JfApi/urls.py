from django.urls import path
from . import views

app_name='jfapi'
urlpatterns = [
    path('',views.mywork,name='mywork'),
    path('enterview/',views.enterview,name="enteriew"),
    path('jfview/',views.jfview,name="jfview"),
    path('mywork/',views.mywork,name='mywork'),
    path('index/',views.indexview,name='index')
]
