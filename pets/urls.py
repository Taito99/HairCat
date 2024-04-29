from django.urls import path
from .views import get_pet, pet_detail, create_pet, update_pet, delete_pet

urlpatterns = [
    path('pets/getpet/<int:pk>/', get_pet, name='get-pet'),
    path('pets/<int:pk>/', pet_detail, name='pet-detail'),
    path('pets/create/', create_pet, name='pet-create'),
    path('pets/<int:pk>/update/', update_pet, name='pet-update'),
    path('pets/<int:pk>/delete/', delete_pet, name='pet-delete'),
]
