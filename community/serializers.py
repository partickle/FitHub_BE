from rest_framework import serializers

from courses.models import Course
from .models import Comment, Complaint


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_id', 'course_id', 'text', 'mark', 'date']
        read_only_fields = ['comment_id', 'user_id', 'date']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['user_id'] = request.user
        return super().create(validated_data)


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    owner_photo = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Course
        fields = ['name', 'category', 'image', 'owner_photo', 'average_rating', 'tags']

    def get_owner_photo(self, obj):
        if obj.owner and obj.owner.photo:
            return obj.owner.photo.url
        return None

    def get_average_rating(self, obj):
        return obj.average_rating()


class CourseDetailSerializer(serializers.ModelSerializer):
    owner_photo = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = '__all__'

    def get_owner_photo(self, obj):
        if obj.owner and obj.owner.photo:
            return obj.owner.photo.url
        return None

    def get_average_rating(self, obj):
        return obj.average_rating()