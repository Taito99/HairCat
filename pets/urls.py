from django.urls import path
from .views import get_pet_list, pet_detail, create_pet_list, update_pet, delete_pet

urlpatterns = [
    path('pets/', get_pet_list, name='pet-list'),
    path('pets/<int:pk>/', pet_detail, name='pet-detail'),
    path('pets/create/', create_pet_list, name='pet-create'),
    path('pets/<int:pk>/update/', update_pet, name='pet-update'),
    path('pets/<int:pk>/delete/', delete_pet, name='pet-delete'),
]
