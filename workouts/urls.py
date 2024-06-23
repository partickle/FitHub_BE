
from django.urls import path

from courses.views import WorkoutCreateView, WorkoutListView, WorkoutDetailView

urlpatterns = [
    path('', WorkoutListView.as_view(), name='workout-list'),
    path('<int:pk>/', WorkoutDetailView.as_view(), name='workout-detail'),
    path('create-workout/', WorkoutCreateView.as_view(), name='create-workout'),

]
