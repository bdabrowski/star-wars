from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:collection_id>', views.collection, name='detail'),
    path('<int:collection_id>/counting', views.counting, name='counting'),
]
