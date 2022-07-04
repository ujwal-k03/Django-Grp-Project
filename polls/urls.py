from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('',views.home,name='home'),
    path('polls/<int:poll_id>/',views.detail,name='detail'),
    path('polls/<int:poll_id>/results/',views.results,name='results'),
    path('polls/create/',views.create,name='create'),
    path('polls/search/',views.search,name='search'),
]