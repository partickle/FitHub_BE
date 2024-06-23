from django.urls import path
from .views import CommentListView, CommentDetailView, ComplaintListView, ComplaintDetailView, CourseDetailView, RateCourseView, UserCoursesView

urlpatterns = [
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('complaints/', ComplaintListView.as_view(), name='complaint-list'),
    path('complaints/<int:pk>/', ComplaintDetailView.as_view(), name='complaint-detail'),
    path('user-courses/', UserCoursesView.as_view(), name='user-courses'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:pk>/rate', RateCourseView.as_view(), name='rate-course'),

]
