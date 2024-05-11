from django.contrib import admin

from courses.models import Course, Tag, Workout, Exercise


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('workouts', 'tags')


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('exercises',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Tag)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Exercise)
