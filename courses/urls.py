
from django.urls import path

from .views import CourseListView, CourseDetailView, WorkoutListView, WorkoutDetailView, ExerciseListView, \
    ExerciseDetailView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/detail/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('workouts/', WorkoutListView.as_view(), name='workout-list'),
    path('workouts/<int:pk>/', WorkoutDetailView.as_view(), name='workout-detail'),
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
    path('exercises/<int:pk>/', ExerciseDetailView.as_view(), name='exercise-detail'),
]
