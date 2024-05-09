from django.urls import path
from .views import register, login, logout, CustomPasswordResetView, get_stuff_list
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('reset_password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('get-staff/', get_stuff_list, name='get-stuff'),
    # Dodaj inne adresy URL, które masz
]
