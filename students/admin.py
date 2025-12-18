from django.contrib import admin
from .models import Student, Course,Teacher,Subject,StudentAuditLog,Activelog
@admin.register(Subject)
class SubjectAmin(admin.ModelAdmin):
    list_display=['name']
    search_fields=['name']
@admin.register(Teacher)
class Teacheradmin(admin.ModelAdmin):
    list_display=['name']
    filter_horizontal=['subjects']
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'age', 'course', 'is_active']
    list_filter = ['course', 'is_active']
    filter_horizontal = ['teachers']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_active=True)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=['name','duration','fee']
    list_filter = ['duration']
    serch_fields = ['name']
    from django.contrib import admin
from .models import Student, StudentAuditLog


@admin.register(StudentAuditLog)
class StudentAuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'student_name',
        'action',
        'performed_by',
        'timestamp',
    )

    list_filter = (
        'action',
        'performed_by',
        'timestamp',
    )

    search_fields = (
        'student_name',
        'performed_by__username',
    )

    ordering = ('-timestamp',)

    readonly_fields = (
        'student',
        'student_name',
        'action',
        'performed_by',
        'timestamp',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False




@admin.register(Activelog)
class ActivelogAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'action',
        'model_name',
        'object_id',
        'ip_address',
        'created_at'
    )
    list_filter = ('action', 'model_name', 'created_at')
    search_fields = ('user__username', 'action', 'model_name', 'message')