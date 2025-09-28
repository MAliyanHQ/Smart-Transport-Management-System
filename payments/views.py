from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
from .models import Payment

# @login_required  # Restrict access to authenticated users
# def payment_history(request):
#     payments = Payment.objects.filter(student=request.user)
#     return render(request, 'payments/payment_history.html', {'payments': payments})

def payment_history(request):
    if not request.user.is_authenticated:
        return redirect('/users/login/')
    payments = Payment.objects.filter(student=request.user)
    return render(request, 'payments/payment_history.html', {'payments': payments})

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from payments.models import Payment

@login_required
def confirm_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, student=request.user)
    
    # Mark as paid
    payment.status = "paid"
    payment.save()
    
    return redirect('student_payments')

@login_required
def student_payments(request):
    """ Show student's due & completed payments """
    if request.user.role != 'student':
        return redirect('home')

    payments = Payment.objects.filter(student=request.user).order_by('-due_date')
    return render(request, 'payments/student_payments.html', {'payments': payments})

@login_required
def manager_payments(request):
    if request.user.role != 'manager':
        return redirect('home')

    students = Payment.objects.select_related('student').order_by('status', 'due_date')

    return render(request, 'payments/manager_payments.html', {"students": students})

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from payments.models import Payment

@login_required
def toggle_payment_status(request, payment_id):  # ✅ Accept payment_id
    if request.user.role != 'manager':
        return redirect('home')

    payment = get_object_or_404(Payment, id=payment_id)

    # ✅ Toggle status
    payment.status = "paid" if payment.status == "pending" else "pending"
    payment.save()

    return redirect("manager_payments")  # Redirect back to manager's payments page


@login_required
def toggle_payment_status(request, payment_id):
    if request.user.role != 'manager':
        return redirect('home')

    payment = get_object_or_404(Payment, id=payment_id)
    
    if payment.status == "pending":
        payment.status = "paid"
    else:
        payment.status = "pending"

    payment.save()
    return redirect("manager_payments")

