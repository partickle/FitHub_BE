from django.contrib import admin

from community.models import Comment, Complaint

admin.site.register(Comment)
admin.site.register(Complaint)
