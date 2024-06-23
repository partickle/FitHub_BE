
from django.urls import path

from courses.views import ExerciseListView, ExerciseDetailView

urlpatterns = [
    path('', ExerciseListView.as_view(), name='exercise-list'),
    path('<int:pk>/', ExerciseDetailView.as_view(), name='exercise-detail'),
]
