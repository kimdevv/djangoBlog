from django.urls import path
from .views import *
from . import views

app_name = 'blog'

urlpatterns = [
    path('', BlogList.as_view()),
    path('<int:pk>/', BlogDetail.as_view())
]
