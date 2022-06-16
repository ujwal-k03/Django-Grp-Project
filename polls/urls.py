from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('',views.home,name='polls-home'),
    path('about/',views.about,name='polls-home'),
    path('<int:poll_id>',views.detail,name='detail'),
    path('<int:poll_id>/results',views.results,name='results'),
    path('<int:poll_id>/vote',views.vote,name='vote'),
]