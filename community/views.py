from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from courses.models import Course, CourseRating
from .models import Comment, Complaint
from .serializers import CommentSerializer, ComplaintSerializer, CourseDetailSerializer, CourseListSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CommentListView(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        course_id = request.data.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
            if course.owner != request.user:
                return Response({"message": "You can only comment on your own courses."},
                                status=status.HTTP_403_FORBIDDEN)
        except Course.DoesNotExist:
            return Response({"message": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def get(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)


class ComplaintListView(APIView):
    def get(self, request):
        complaints = Complaint.objects.all()
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComplaintDetailView(APIView):
    def get(self, request, pk):
        try:
            complaint = Complaint.objects.get(id=pk)
            serializer = ComplaintSerializer(complaint)
            return Response(serializer.data)
        except Complaint.DoesNotExist:
            return Response({"message": "Complaint not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            complaint = Complaint.objects.get(pk=pk)
            complaint.delete()
            return Response({"message": "Complaint deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Complaint.DoesNotExist:
            return Response({"message": "Complaint not found"}, status=status.HTTP_404_NOT_FOUND)


class UserCoursesView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of courses with optional filters. Example usage:\n"
                              "`?filter=recent&search=Pushups&username=John&coursetag=Hands`",
        manual_parameters=[
            openapi.Parameter('filter', openapi.IN_QUERY, description="Filter type: recent, critical, favourable", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by course name", type=openapi.TYPE_STRING),
            openapi.Parameter('username', openapi.IN_QUERY, description="Search by username of the course creator", type=openapi.TYPE_STRING),
            openapi.Parameter('coursetag', openapi.IN_QUERY, description="Filter by course tag", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        filter_param = request.query_params.get('filter', 'recent')
        search_param = request.query_params.get('search', None)
        username = request.query_params.get('username', None)
        course_tag = request.query_params.get('coursetag', None)
        
        if filter_param == 'recent':
            courses = Course.objects.recent().filter(owner__isnull=False)
        elif filter_param == 'critical':
            courses = Course.objects.critical().filter(owner__isnull=False)
        elif filter_param == 'favourable':
            courses = Course.objects.favourable().filter(owner__isnull=False)
        else:
            courses = Course.objects.filter(owner__isnull=False)
        
        if search_param:
            courses = courses.filter(name__icontains=search_param)
        
        if username:
            courses = courses.filter(owner__username__icontains=username)
        
        if course_tag:
            courses = courses.filter(tags__name__icontains=course_tag)
        
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseDetailView(APIView):
    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        serializer = CourseDetailSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RateCourseView(APIView):
    def post(self, request, pk):
        user = request.user
        course = get_object_or_404(Course, id=pk)
        rating_value = request.data.get('rating')
        
        rating, created = CourseRating.objects.update_or_create(
            user=user, course=course,
            defaults={'rating': rating_value}
        )
        
        return Response({'status': 'rating set', 'rating': rating_value}, status=status.HTTP_201_CREATED)
