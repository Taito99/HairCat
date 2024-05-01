from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from review.models import Review
from review.serializers import ReviewSerializer


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
