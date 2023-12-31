import datetime

from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from habits.models import Habit
from habits.paginators import Paginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, HabitListSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        now = datetime.datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone()) + datetime.timedelta(hours=1)
        habit = Habit.objects.get(pk=serializer.data['id'])
        if habit.time.hour > now.time().hour:
            habit.date = datetime.datetime.now().date()
            habit.save()
        elif habit.time.hour <= now.time().hour:
            habit.date = datetime.datetime.now().date() + datetime.timedelta(days=1)
            habit.save()


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Paginator

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def partial_update(self, request, *args, **kwargs):
        return Response({"detail": "Метод PATCH запрещён, используйте метод PUT"})


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class AllHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitListSerializer
    permission_classes = [IsAuthenticated]
    queryset = Habit.objects.all().filter(is_public=True)
