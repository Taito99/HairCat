from django.urls import path
from .views import VisitList, VisitDetail, booking_view

urlpatterns = [
    path('visits/', VisitList.as_view(), name='visit-list'),
    path('visits/<int:pk>/', VisitDetail.as_view(), name='visit-detail'),
    path('book-visit/', booking_view, name='book-visit'),
]
