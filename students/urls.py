from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from .api_views import ActivityLogViewSet
router = DefaultRouter()
router.register('activity-logs', ActivityLogViewSet, basename='activity-log')

urlpatterns = [
    path('',HomeView.as_view(),name="home"),

    path('student_list/',StudentListView.as_view(),name="student_list"),
    path('create/',StudentCreateView.as_view(),name="student_create"),
    path('login/',UserLoginView.as_view(),name="login"),
    path('logout/',UserLogoutView.as_view(),name="logout"),
    path('register/',UserRegisterView.as_view(),name="register"),
    path('change_password/',ChangePasswordView.as_view(),name="change_password"),
    path('profile/',ProfileView.as_view(),name="profile"),
    path('course/',CourseListView.as_view(),name="course_list"),
    path('courses/add/',CourseCreateView.as_view(),name="course_add"),
    path('teacher/',TeacherListView.as_view(),name="teacher_list"),
    path('teachers/add/',TeacherCreateView.as_view(),name="teacher_add"),
    path('update/<int:pk>',StudentUpdateView.as_view(),name="student_update"),
    path('delete/<int:pk>',StudentDeleteView.as_view(),name="student_delete"),
    path('teacher/<int:pk>/edit/',TeacherUpdateView.as_view(),name="teacher_edit"),
    path('course/<int:pk>/edit/',CourseUpdateView.as_view(),name="course_edit"),
     path('students/export/', StudentExportCSVView.as_view(), name='export_students_csv'),
    path('students/import/', StudentImportCSVView.as_view(), name='import_students_csv'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
urlpatterns += router.urls