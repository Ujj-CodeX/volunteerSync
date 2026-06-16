from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [('admin', 'Admin'), ('volunteer', 'Volunteer')]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='volunteer')
    region = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)

class VolunteerRequest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    region = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    deadline = models.DateField()
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    created_at = models.DateTimeField(auto_now_add=True)

class RequestResponse(models.Model):
    STATUS_CHOICES = [('accepted', 'Accepted'), ('rejected', 'Rejected')]
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(VolunteerRequest, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    responded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('volunteer', 'request')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)