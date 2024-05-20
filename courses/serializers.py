from rest_framework import serializers
from .models import Course, Exercise, Workout, Tag


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'category', 'image', 'is_pro']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class WorkoutToCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'name']


class CourseDetailSerializer(serializers.ModelSerializer):
    workouts = WorkoutToCourseSerializer(many=True, read_only=False, required=False)
    tags = TagSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Course
        fields = "__all__"

    def create(self, validated_data):
        workouts_data = validated_data.pop('workouts', [])
        tags_data = validated_data.pop('tags', [])
        course = Course.objects.create(**validated_data)
        for workout_data in workouts_data:
            workout, _ = Workout.objects.get_or_create(**workout_data)
            course.workouts.add(workout)
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            course.tags.add(tag)
        return course

    def update(self, instance, validated_data):
        instance.workouts.clear()
        instance.tags.clear()
        workouts_data = validated_data.pop('workouts', [])
        tags_data = validated_data.pop('tags', [])
        for workout_data in workouts_data:
            workout, _ = Workout.objects.get_or_create(**workout_data)
            instance.workouts.add(workout)
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            instance.tags.add(tag)
        return super().update(instance, validated_data)


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'name', 'category', 'image']


class WorkoutDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = "__all__"


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'category', 'image', 'video']


class ExerciseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"
