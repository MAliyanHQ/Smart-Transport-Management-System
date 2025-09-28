from django.db import models
from django.conf import settings
from django.utils.timezone import now, timedelta

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=5000)  # Default fee
    due_date = models.DateField(default=now)  # Payment is due on the registration date
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def is_overdue(self):
        return self.status == 'pending' and self.due_date < now().date() - timedelta(days=30)

    def __str__(self):
        return f"{self.student.username} - {self.amount} PKR - {self.status}"
