from django.shortcuts import render,redirect,get_object_or_404
import csv
from django.http import HttpResponse
from django.views import View
from django.core.paginator import Paginator
import re
from django.views.generic import ListView,CreateView,UpdateView
from .models import Student, Course ,Teacher
from .forms import StudentForm, TeacherForm,CourseForm,StudentCSVImportForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Q,Count
from django.urls import reverse_lazy
import time
from django.utils import timezone
from .mixins import StaffRequiredMixin, AdminOnlyMixin, ReadOnlyMixin,ActivityLogMixin
from io import TextIOWrapper
from django.db import transaction


class CourseListView(StaffRequiredMixin,ListView):
    model=Course
    template_name= 'students/course_list.html'
    context_object_name='courses'
class CourseCreateView(StaffRequiredMixin,CreateView):
    model=Course
    form_class= CourseForm
    template_name= 'students/course_form.html'
    success_url='/course/'
    def form_valid(self, form):
        messages.success(self.request, "Course created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
class CourseUpdateView(StaffRequiredMixin,UpdateView
                       ):
    model=Course
    form_class= CourseForm
    template_name= 'students/course_form.html'
    success_url='/course/'
    def form_valid(self, form):
        messages.success(self.request, "Course updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
class UserRegisterView(View):
    def get(self, request):
        return render(request, 'students/register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')


        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('register')

        if not re.search(r"[A-Z]", password):
            messages.error(request, "Password must contain at least 1 uppercase letter.")
            return redirect('register')

        if not re.search(r"[0-9]", password):
            messages.error(request, "Password must contain at least 1 number.")
            return redirect('register')

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            messages.error(request, "Password must contain at least 1 special character.")
            return redirect('register')
 
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Congratulations, user has been created")
        return redirect('login')


class UserLoginView(View):
    def get(self,request):
        return render(request,'students/login.html')
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')

        if "attempts" not in request.session:
            request.session["attempts"] = 0

        if "lockout_until" not in request.session:
            request.session["lockout_until"] = None

        lockout_until = request.session.get("lockout_until")

        if lockout_until and time.time() < lockout_until:
            remaining = int(lockout_until - time.time())
            messages.error(request, f"Too many failed attempts. Try again in {remaining} seconds.")
            return render(request, 'students/login.html')

        user = authenticate(request, username=username, password=password)

        if user is None:
            request.session["attempts"] += 1

            if request.session["attempts"] >= 3:
                request.session["lockout_until"] = time.time() + 30 
                request.session["attempts"] = 0  
                messages.error(request, "Too many failed attempts. Login locked for 30 seconds.")
                return render(request, 'students/login.html')

            messages.error(request, "Invalid username or password.")
            return render(request, 'students/login.html')

        request.session["attempts"] = 0
        request.session["lockout_until"] = None

        login(request, user)
        return redirect('home')

class UserLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('login')

    

            

class StudentListView(LoginRequiredMixin, ReadOnlyMixin,View):
    login_url = 'login'

    def get(self, request):
        query = request.GET.get('q', '')
        sort_by = request.GET.get('sort_by', 'name')
        page_number = request.GET.get('page')

        students = Student.objects.filter(is_active=True)

    
        if query:
            students = students.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query)
            )

        
        if sort_by == 'age':
            students = students.order_by('age')
        else:
            students = students.order_by('name')

     
        paginator = Paginator(students, 5)  
        page_obj = paginator.get_page(page_number)

        context = {
            'students': page_obj,           
            'page_obj': page_obj,           
            'is_pagination': paginator.num_pages > 1,
            'query': query,
            'sort_by': sort_by,
        }

        return render(request, 'students/student_list.html', context)

class StudentCreateView(
    LoginRequiredMixin,
    ActivityLogMixin,   # ✅ BEFORE View
    View
):
    login_url = 'login'
    action = "Student Created"

    def get(self, request):
        form = StudentForm()
        return render(request, 'students/student_form.html', {'form': form})

    def post(self, request):
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save()

            # 🔥 REQUIRED LINE
            self.log_activity(
                request,
                obj=student,
                message="Student created successfully"
            )

            messages.success(request, "Student created successfully.")
            return redirect('student_list')

        messages.error(request, "Please correct the errors below.")
        return render(request, 'students/student_form.html', {'form': form})

    
class StudentUpdateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    PermissionRequiredMixin,
    ActivityLogMixin,   # ✅ BEFORE View
    View
):
    login_url = 'login'
    permission_required = 'students.can_update_student'
    action = "Student Updated"

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(instance=student)
        return render(request, 'students/student_form.html', {'form': form})

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            updated_student = form.save()

            # 🔥 THIS WAS MISSING
            self.log_activity(
                request,
                obj=updated_student,
                message="Student details updated"
            )

            messages.success(request, "Student updated successfully.")
            return redirect('student_list')

        messages.error(request, "Please correct the errors below.")
        return render(request, 'students/student_form.html', {'form': form})

    
class StudentDeleteView(
    LoginRequiredMixin,
    AdminOnlyMixin,
    ActivityLogMixin,   # ✅ BEFORE View
    View
):
    login_url = 'login'
    action = "Student Deleted"

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        return render(
            request,
            'students/student_confirm_delete.html',
            {'student': student}
        )

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk, is_active=True)

        student.soft_delete()

        # 🔥 REQUIRED
        self.log_activity(
            request,
            obj=student,
            message="Student soft deleted"
        )

        messages.success(request, "Student deleted successfully.")
        return redirect('student_list')


class ChangePasswordView(PasswordChangeView):
    template_name='students/password_change_form.html'
    success_url= reverse_lazy('home')

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {
            'user': user
        }
        return render(request, 'students/profile.html', context)

    
class HomeView(LoginRequiredMixin,View):
    login_url='/login/'
    redirect_field_name='next'

    def get(self , request):
        return render(request,'students/home.html')
    

class TeacherCreateView(StaffRequiredMixin,CreateView):
    model= Teacher
    form_class= TeacherForm
    template_name='students/teacher_form.html'
    success_url=reverse_lazy('teacher_list')
    def form_valid(self, form):
        messages.success(self.request, "Teacher added successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
class TeacherListView(StaffRequiredMixin,ListView):
    model= Teacher
    template_name= 'students/teacher_list.html'
    context_object_name='teachers'
    ordering=['name']

class TeacherUpdateView(StaffRequiredMixin,UpdateView):
    model=Teacher
    form_class= TeacherForm
    template_name='students/teacher_form.html'
    success_url=reverse_lazy('teacher_list')
    def form_valid(self, form):
        messages.success(self.request, "Teacher updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
    
class StudentExportCSVView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Name',
            'Email',
            'Age',
            'Phone Number',
            'Course'
        ])

        students = Student.objects.filter(is_active=True)

        for student in students:
            writer.writerow([
                student.name,
                student.email,
                student.age,
                student.phone_number,
                student.course.name if student.course else ''
            ])

        return response

class StudentImportCSVView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'students/student_import.html'

    def get(self, request):
        form = StudentCSVImportForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = StudentCSVImportForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        csv_file = form.cleaned_data['csv_file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please upload a valid CSV file.")
            return render(request, self.template_name, {'form': form})

        decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.DictReader(decoded_file)

        errors = []
        success_count = 0

        with transaction.atomic():
            for row_num, row in enumerate(reader, start=2):  # header = row 1
                try:
                    self.validate_and_create_student(row)
                    success_count += 1
                except Exception as e:
                    errors.append({
                        'row': row_num,
                        'error': str(e),
                        'data': row
                    })

        if errors:
            return render(request, self.template_name, {
                'form': form,
                'errors': errors,
                'success_count': success_count
            })

        messages.success(request, f"{success_count} students imported successfully.")
        return redirect('student_list')
    def validate_and_create_student(self, row):
        # normalize keys (lowercase + replace spaces)
        row = {k.strip().lower().replace(" ", "_"): v for k, v in row.items()}

        name = row.get('name', '').strip()
        email = row.get('email', '').strip()
        age = row.get('age', '').strip()
        phone = row.get('phone_number', '').strip()
        course_name = row.get('course', '').strip()

        if not name:
            raise ValueError("Name is required")

        if not email:
            raise ValueError("Email is required")

        if Student.objects.filter(email=email).exists():
            raise ValueError("Email already exists")

        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("Invalid age")

        if phone and (not phone.isdigit() or len(phone) != 10):
            raise ValueError("Phone number must be 10 digits")

        course = None
        if course_name:
            course = Course.objects.filter(name__iexact=course_name).first()
            if not course:
                raise ValueError(f"Course '{course_name}' does not exist")

        Student.objects.create(
            name=name,
            email=email,
            age=age,
            phone_number=phone,
            course=course,
            is_active=True
        )
class DashboardView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        # total active students
        total_students = Student.objects.filter(is_active=True).count()

        # students count per course (only active)
        students_per_course = (
            Course.objects.annotate(
                student_count=Count(
                    'student',
                    filter=Q(student__is_active=True)
                )
            )
        )

        context = {
            'total_students': total_students,
            'students_per_course': students_per_course,
        }
        return render(request, 'students/dashboard.html', context)
