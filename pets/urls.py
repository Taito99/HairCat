from django.urls import path
from .views import pet_detail, create_pet, update_pet, delete_pet, list_pets

urlpatterns = [
    path('pets/', list_pets, name='pet-list'),
    path('pets/<int:pk>/', pet_detail, name='pet-detail'),
    path('pets/create/', create_pet, name='pet-create'),
    path('pets/<int:pk>/update/', update_pet, name='pet-update'),
    path('pets/<int:pk>/delete/', delete_pet, name='pet-delete'),
]
