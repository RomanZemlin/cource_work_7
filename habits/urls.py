from django.urls import path

from habits.views import HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView, AllHabitListAPIView

urlpatterns = [
    path('all_habits/', AllHabitListAPIView.as_view(), name='all_habits'),
    path('my_habits/create/', HabitCreateAPIView.as_view(), name='create_habit'),
    path('my_habits/', HabitListAPIView.as_view(), name='habits'),
    path('my_habits/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit'),
    path('my_habits/<int:pk>/update/', HabitUpdateAPIView.as_view(), name='update_habit'),
    path('my_habits/<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='delete_habit'),
]
