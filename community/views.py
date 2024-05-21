from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from courses.models import Course
from .models import Comment, Complaint
from .serializers import CommentSerializer, ComplaintSerializer


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

    def put(self, request, pk):
        try:
            complaint = Complaint.objects.get(pk=pk)
            serializer = ComplaintSerializer(complaint, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Complaint.DoesNotExist:
            return Response({"message": "Complaint not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            complaint = Complaint.objects.get(pk=pk)
            complaint.delete()
            return Response({"message": "Complaint deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Complaint.DoesNotExist:
            return Response({"message": "Complaint not found"}, status=status.HTTP_404_NOT_FOUND)
