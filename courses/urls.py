from django.urls import path

from .views import CourseCreateView, CourseListView, CourseDetailView

urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('create-course/', CourseCreateView.as_view(), name='create-course'),
]
