from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from payments.models import Payment
from django.utils.timezone import now
from datetime import timedelta

import cv2
import pytesseract
import numpy as np
from PIL import Image
from django.utils.timezone import now
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm
from payments.models import Payment
import re

# Set the Tesseract OCR path (Modify for your system if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# ✅ **Step 1: Preprocess Image**
def preprocess_image(image_path):
    """Convert the image to grayscale and apply thresholding."""
    image_array = np.asarray(bytearray(image_path.read()), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


# ✅ **Step 2: Extract Text using OCR**
def extract_text_from_image(image):
    """Run OCR on the preprocessed image and extract text."""
    pil_image = Image.fromarray(image)  # Convert OpenCV image to PIL Image
    extracted_text = pytesseract.image_to_string(pil_image).lower()  # Convert to lowercase
    return extracted_text


# ✅ **Step 3: Name Matching**
def verify_name_in_id(extracted_text, first_name, last_name):
    """
    Check if both first and last names appear in the extracted text.
    """
    
    lines = extracted_text.splitlines()
    
    # Clean and process each line: remove unwanted characters and convert to lowercase
    cleaned_lines = []
    for line in lines:
        # Remove spaces, special characters, and convert to lowercase
        cleaned_line = re.sub(r'[^a-zA-Z\s]', '', line).strip().lower()
        cleaned_lines.append(cleaned_line)
    
    print(f"Processed Lines: {cleaned_lines}") 

    first_name, last_name = first_name.lower(), last_name.lower()  # Convert to lowercase

    return first_name in cleaned_lines and last_name in cleaned_lines


# ✅ **Step 4: Register Function**
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            id_card = request.FILES.get('id_card')  # Get the uploaded ID card
            
            print(first_name)
            print(last_name)

            # 🔹 **Ensure ID Card is uploaded**
            if not id_card:
                print(request, "Please upload an ID card for verification.")
                return redirect('register')

            try:
                # ✅ **Read and preprocess the uploaded ID card**
                print(id_card)
                preprocessed_image = preprocess_image(id_card)
                print(id_card)
                extracted_text = extract_text_from_image(preprocessed_image)
                print(extracted_text)

                # ✅ **Verify if the extracted text contains the first & last name**
                if not verify_name_in_id(extracted_text, first_name, last_name):
                    print(request, "Your ID card does not match your entered name. Please try again.")
                    return redirect('register')

            except Exception as e:
                print(request, f"Error processing ID card: {e}")
                return redirect('register')

            # ✅ **If the name is verified, save the user and log them in**
            student = form.save()
            login(request, student)

            # ✅ **Create a payment for students**
            if student.role == 'student':
                due_date = now().date() + timedelta(days=30)  # Set payment due in 30 days
                Payment.objects.create(
                    amount=10000,  # Fixed monthly fee
                    student=student,
                    due_date=due_date,
                    status="pending",
                )

            messages.success(request, "Registration successful! You are now logged in.")
            
            # ✅ Redirect based on role
            if student.role == "student":
                return redirect("student_dashboard")  # Redirect drivers to their dashboard
            elif student.role == "driver":
                return redirect("driver_dashboard")  # Redirect drivers to their dashboard
            elif student.role == "manager":
                return redirect("manager_dashboard")  # Redirect drivers to their dashboard
            else:
                return redirect('/')  # Redirect to homepage after successful login

            return redirect('home')

    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


from django.template.loader import get_template 

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.utils.timezone import now
from datetime import timedelta
from payments.models import Payment

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.timezone import now
from payments.models import Payment
from django.contrib.auth import login
from datetime import timedelta

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # ✅ Check if the user is a student
            if user.role == 'student':
                today = now().date()

                # 🔹 Step 1: **Check if the student has an overdue payment (more than 30 days late)**
                overdue_payment = Payment.objects.filter(
                    student=user,
                    status="pending",
                    due_date__lt=today 
                ).first()  # Get the first matching overdue payment

                if overdue_payment:
                    # If overdue payment exists, prevent login and show error message
                    messages.error(request, "Your account is disabled due to overdue payments. Please contact support.")
                    return redirect('login')  # Prevent login if overdue payment exists
                
                # 🔹 Step 2: **Generate the current month's payment if it doesn't exist**
                recent_payment = Payment.objects.filter(
                    student=user,
                    due_date__gte=today - timedelta(days=30)  # ❗ Payment exists in last 30 days
                ).exists()

                if not recent_payment:
                    # **Create a new payment**
                    Payment.objects.create(
                        student=user,
                        amount=10000,  # ❗ Monthly Fee = PKR 10,000
                        due_date=today + timedelta(days=30),  # ❗ Due 30 days from today
                        status="pending"
                    )

            # ✅ Log in the user after all checks are passed
            login(request, user)
            
            # ✅ Redirect based on role
            if user.role == "student":
                return redirect("student_dashboard")  # Redirect drivers to their dashboard
            elif user.role == "driver":
                return redirect("driver_dashboard")  # Redirect drivers to their dashboard
            elif user.role == "manager":
                return redirect("manager_dashboard")  # Redirect drivers to their dashboard
            else:
                return redirect('/')  # Redirect to homepage after successful login

    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})



from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # Log out the user
    return redirect('/')  # Redirect to the home page after logging out


def home(request):
    print(get_template('home.html'))  # Debug to verify template loading
    return render(request, 'home.html')
