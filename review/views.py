from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Review
from .serializers import ReviewSerializer


class ReviewLikeDislikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({"message": "Review does not exist."}, status=404)

        action = request.data.get('action')

        if action == 'like':
            review.likes += 1
        elif action == 'dislike':
            review.dislikes += 1
        else:
            return Response({"message": "Invalid action."}, status=400)

        if request.user != review.user:  # Sprawdź, czy użytkownik jest autorem recenzji
            raise PermissionDenied("You are not allowed to like/dislike this review.")

        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_reviews(request):
    # Użyj `request.user.review_set.all()` lub `Review.objects.filter(user=request.user)`
    # w zależności od tego, jak zdefiniowano relację w modelu Review
    reviews = Review.objects.filter(user=request.user)  # Zakładam, że istnieje pole 'user' w modelu Review
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addReview(request):
    serializer = ReviewSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateReview(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review.user != request.user:
        return Response({"detail": "You do not have permission to update this review."},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = ReviewSerializer(review, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteReview(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review.user != request.user:
        return Response({"detail": "You do not have permission to delete this review."},
                        status=status.HTTP_403_FORBIDDEN)

    review.delete()
    return Response({"message": "Review deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
