from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Visit
from .serializers import VisitSerializer


class VisitList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        visits = Visit.objects.filter(user=request.user)
        serializer = VisitSerializer(visits, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VisitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class VisitDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        visit = Visit.objects.get(id=pk, user=request.user)
        serializer = VisitSerializer(visit)
        return Response(serializer.data)

    def put(self, request, pk):
        visit = Visit.objects.get(id=pk, user=request.user)
        serializer = VisitSerializer(visit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        visit = Visit.objects.get(id=pk, user=request.user)
        visit.delete()
        return Response(status=204)
