from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.timezone import now, timedelta


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('driver', 'Driver'),
        ('manager', 'Manager'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True)
    cnic = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    id_card = models.ImageField(upload_to='id_cards/', null=True, blank=True)  # ✅ ID Card Upload

    # ✅ Auto-disable unpaid students
    is_active = models.BooleanField(default=True)  # ❌ Set to False if unpaid for 30+ days

    # Add related_name arguments to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Custom related name for groups
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Custom related name for permissions
        blank=True,
    )

    def disable_unpaid_students(self):
        """Disable student accounts if they have not paid in the last 30 days."""
        from payments.models import Payment  # Avoid circular import

        overdue_payments = Payment.objects.filter(
            student=self,
            status="pending",
            due_date__lte=now().date() - timedelta(days=30)
        )

        if overdue_payments.exists():
            self.is_active = False  # ❌ Disable the account
            self.save()

    def __str__(self):
        return f"{self.username} - {self.role} - {'Active' if self.is_active else 'Disabled'}"
