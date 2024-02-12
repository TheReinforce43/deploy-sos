from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,CourseCategory, Course, CourseDetails, StudentModel, EnrollmentModel,Teacher

class CustomUserAdmin(UserAdmin):
    list_display = ('id','mobile_number', 'name', 'role', 'is_active', 'is_admin', 'created_at', 'updated_at')
    search_fields = ('mobile_number', 'name')
    list_filter = ('role', 'is_active', 'is_admin', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('Personal Info', {'fields': ('name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'name', 'email', 'role', 'password1', 'password2', 'is_active', 'is_admin')}
        ),
    )
    ordering = ('-created_at',)
    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(CourseDetails)
admin.site.register(Teacher)
admin.site.register(StudentModel)
admin.site.register(EnrollmentModel)
