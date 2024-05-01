from django.urls import path
from .views import ReviewLikeDislikeView, get_all_reviews, addReview, updateReview, deleteReview

urlpatterns = [
    path('reviews/<int:review_id>/like_dislike/', ReviewLikeDislikeView.as_view(), name='review-like-dislike'),
    path('reviews/all/', get_all_reviews, name='get_reviews'),
    path('reviews/add/', addReview, name='add_review'),
    path('reviews/update/<int:pk>/', updateReview, name='update_review'),
    path('reviews/delete/<int:pk>/', deleteReview, name='delete_review'),
]
