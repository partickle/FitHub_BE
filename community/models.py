from django.db import models

from authorisation.models import CustomUser
from courses.models import Course


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mark = models.IntegerField(null=False)
    date = models.DateTimeField(null=False)

    def __str__(self):
        return f"Comment {self.comment_id} by User {self.user_id}"


class Complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Complaint {self.complaint_id} by User {self.user_id}"
