from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.conf import settings

class Activelog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    action=models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.model_name}"
    
class Subject(models.Model):
    name= models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name 
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject,blank=True)
    def __str__(self):
        return self.name 
class Course(models.Model):
    name= models.CharField(max_length=100)
    duration= models.CharField(max_length=20)
    fee = models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return f"{self.name} ({self.duration})"
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class Student(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{10}$', 'Invalid phone number.')],
        blank=True,
        null=True
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    teachers = models.ManyToManyField(Teacher, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students_created"
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students_updated"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        permissions = [
            ("can_update_student", "Can update student"),
        ]

    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    def restore(self):
        self.is_active = True
        self.save(update_fields=["is_active"])

    def __str__(self):
        return self.name

class StudentAuditLog(models.Model):
    ACTIONS = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    student_name = models.CharField(max_length=200)
    action = models.CharField(max_length=10, choices=ACTIONS)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.action}"
