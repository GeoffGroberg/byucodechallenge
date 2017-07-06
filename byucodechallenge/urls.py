from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.chess_board, name='chess_board'),
]