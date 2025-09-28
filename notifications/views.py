from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.shortcuts import render 

def notifications(request):
    if not request.user.is_authenticated:
        return redirect('/users/login/')
    user_notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notifications/notifications.html', {'notifications': user_notifications})
