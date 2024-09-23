from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.insert, name='insert'),
    path('<int:id>/', views.show, name='show'),
    path('<int:id>/update/', views.update, name='update'),
    path('<int:id>/delete/', views.destroy, name='destroy'),
    path('auth', views.auth, name='auth'),
]