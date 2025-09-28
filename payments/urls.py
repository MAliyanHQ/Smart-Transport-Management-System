from django.urls import path
from .views import student_payments, confirm_payment, manager_payments, toggle_payment_status

urlpatterns = [
    path('student/', student_payments, name='student_payments'),  # ✅ Student Payments Page
    path('confirm-payment/<int:payment_id>/', confirm_payment, name='confirm_payment'),  # ✅ Student Marks Paid
    path('manager/', manager_payments, name='manager_payments'),  # ✅ Manager Payments Page
    path('toggle-payment/<int:payment_id>/', toggle_payment_status, name='toggle_payment_status'),  # ✅ Manager Toggles Status
]
