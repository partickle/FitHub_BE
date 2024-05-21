from rest_framework import serializers
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
