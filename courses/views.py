from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Workout, Exercise
from courses.serializers import CourseSerializer, CourseDetailSerializer, WorkoutDetailSerializer, ExerciseSerializer, \
    ExerciseDetailSerializer, WorkoutSerializer


class CourseListView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseDetailView(APIView):


    def get(self, request, pk):
        
        course = Course.objects.get(id=pk)
        serializer = CourseDetailSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new course."""
        serializer = CourseDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            serializer = CourseDetailSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            course.delete()
            return Response({"message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)


class WorkoutListView(APIView):
    def get(self, request):
        workouts = Workout.objects.all()
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)


class WorkoutDetailView(APIView):
    def get(self, request, pk):
        try:
            workout = Workout.objects.get(id=pk)
            serializer = WorkoutDetailSerializer(workout)
            return Response(serializer.data)
        except Workout.DoesNotExist:
            return Response({"message": "Workout not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = WorkoutDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            workout = Workout.objects.get(pk=pk)
            serializer = WorkoutDetailSerializer(workout, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Workout.DoesNotExist:
            return Response({"message": "Workout not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            workout = Workout.objects.get(pk=pk)
            workout.delete()
            return Response({"message": "Workout deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Workout.DoesNotExist:
            return Response({"message": "Workout not found"}, status=status.HTTP_404_NOT_FOUND)


class ExerciseListView(APIView):
    def get(self, request):
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)


class ExerciseDetailView(APIView):

    def get(self, request, pk):
        try:
            exercise = Exercise.objects.get(id=pk)
            serializer = ExerciseDetailSerializer(exercise)
            return Response(serializer.data)
        except Exercise.DoesNotExist:
            return Response({"message": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ExerciseDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            exercise = Exercise.objects.get(pk=pk)
            serializer = ExerciseDetailSerializer(exercise, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exercise.DoesNotExist:
            return Response({"message": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            exercise = Exercise.objects.get(pk=pk)
            exercise.delete()
            return Response({"message": "Exercise deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exercise.DoesNotExist:
            return Response({"message": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)
