from django.urls import path
from .views import ReviewCreateView, ReviewLikeDislikeView

urlpatterns = [
    path('reviews/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:review_id>/like_dislike/', ReviewLikeDislikeView.as_view(), name='review-like-dislike'),
]
