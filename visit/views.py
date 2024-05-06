from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import VisitSerializer
from django.shortcuts import render
from .models import Visit
from django.utils import timezone
import datetime




def booking_view(request):
    date_today = timezone.now().date()
    start_time = datetime.datetime.combine(date_today, datetime.time(8, 0))
    end_time = datetime.datetime.combine(date_today, datetime.time(15, 0))
    available_slots = []

    while start_time < end_time:
        if not Visit.objects.filter(date=start_time).exists():
            available_slots.append(start_time.strftime('%H:%M'))
        start_time += datetime.timedelta(hours=1)

    if request.method == 'POST':
        selected_time = request.POST.get('time_slot')
        selected_datetime = datetime.datetime.strptime(f"{date_today} {selected_time}", '%Y-%m-%d %H:%M')
        Visit.objects.create(user=request.user, pet=request.user.pets.first(), date=selected_datetime, status='planned')
        return render(request, 'confirmation_page.html', {'selected_time': selected_time})

    return render(request, 'booking_page.html', {'slots': available_slots})

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
