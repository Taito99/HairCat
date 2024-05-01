from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .serializers import ReviewSerializer

class ReviewCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

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

        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
