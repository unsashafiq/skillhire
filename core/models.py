from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class ProblemReport(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class Worker(models.Model):
    name = models.CharField(max_length=100)
    id_card_number = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='worker_profiles/', blank=True, null=True)
    skill = models.CharField(max_length=100)
    experience = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.skill})"
# core/models.py


class EmployerManager(BaseUserManager):
    def create_user(self, email, name, id_card_number, password=None):
        if not email:
            raise ValueError("Employers must have an email")
        if not id_card_number:
            raise ValueError("ID Card number is required")
        email = self.normalize_email(email)
        employer = self.model(email=email, name=name, id_card_number=id_card_number)
        employer.set_password(password)
        employer.save(using=self._db)
        return employer

class Employer(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    id_card_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Required for admin
    is_active = models.BooleanField(default=True)  # Required for login
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'id_card_number']

    objects = EmployerManager()

    def __str__(self):
        return self.name


class JobPost(models.Model):
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    skill_required = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Bookmark(models.Model):
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employer', 'worker')

    def __str__(self):
        return f"{self.employer.username} bookmarked {self.worker.name}"
class Application(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    bookmarked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('job', 'worker')  # prevent duplicate applications

    def __str__(self):
        return f"{self.worker.name} applied to {self.job.title}"
class SupportMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"