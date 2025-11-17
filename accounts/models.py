from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('admin', 'Менеджер'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    isu = models.CharField(
        max_length=6,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Номер ИСУ'
    )

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"