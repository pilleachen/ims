from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from.models import *
# Register your models here.

def approve_users(modeladmin, request, queryset):
    queryset.update(is_active=True)
approve_users.short_description = "Approve selected users"

class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'is_active']
    actions = [approve_users]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Notice)
admin.site.register(StdProfile)
admin.site.register(Subject)
admin.site.register(Marks)
admin.site.register(UniversityMarks)
admin.site.register(Attendance)
admin.site.register(Course)
admin.site.register(Syllabus)
admin.site.register(ExamTimetable)
admin.site.register(ClassTimetable)