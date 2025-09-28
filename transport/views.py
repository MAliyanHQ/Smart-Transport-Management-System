from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import BusStop, Route, Vehicle, Trip
from django.shortcuts import get_object_or_404
from django.shortcuts import render
import json

from django.shortcuts import render
from .models import BusStop


def routes(request):
    routes = Route.objects.all()
    return render(request, 'transport/routes.html', {'routes': routes})

from django.shortcuts import render
from django.http import JsonResponse
from .models import BusStop

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BusStop
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BusStop
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BusStop
import json

import requests

def get_address_from_coordinates(lat, lng):
    """Fetches the address using Google Maps API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key=AIzaSyBMTwxml0qqFhVy6NrkBg8gyvd_mAk1Drc"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        return data['results'][0]['formatted_address']  # ✅ Get the first formatted address
    return "Address not found"

@csrf_exempt
def add_stop(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if not all([name, latitude, longitude]):
                return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

            address = get_address_from_coordinates(latitude, longitude)
            
            bus_stop = BusStop.objects.create(
                name=name,
                latitude=latitude,
                longitude=longitude,
                address=address
            )
            return JsonResponse({'status': 'success', 'message': 'Bus stop added successfully!', 'id': bus_stop.id}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)



def student_trip(request):
    """
    View for students to select their trip.
    Fetches all bus stops for selection.
    """
    bus_stops = BusStop.objects.all()
    return render(request, 'transport/student_trip.html', {'bus_stops': bus_stops})

def manage_bus_stops(request):
    return render(request, 'manage_bus_stops.html')


from django.http import JsonResponse
from .models import Route

def get_route(request):
    start_stop_id = request.GET.get('start')
    end_stop_id = request.GET.get('end')

    try:
        route = Route.objects.get(start_stop_id=start_stop_id, end_stop_id=end_stop_id)
        travel_time = route.travel_time  # Assume this is stored in seconds
        return JsonResponse({"status": "success", "travel_time": travel_time})
    except Route.DoesNotExist:
        return JsonResponse({"status": "error", "message": "No route found"})


def student_trip(request):
    bus_stops = BusStop.objects.all()
    return render(request, 'transport/student_trip.html', {'bus_stops': bus_stops})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BusStop
import json

@csrf_exempt
def delete_stop(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if not all([latitude, longitude]):
                return JsonResponse({'status': 'error', 'message': 'Latitude and longitude are required.'}, status=400)

            # Find the bus stop by latitude and longitude
            bus_stop = BusStop.objects.filter(latitude=latitude, longitude=longitude).first()
            if bus_stop:
                bus_stop.delete()
                return JsonResponse({'status': 'success', 'message': 'Bus stop deleted successfully.'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Bus stop not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)





def get_bus_stops(request):
    if request.method == "GET":
        bus_stops = BusStop.objects.all().values('name', 'latitude', 'longitude', 'address')
        return JsonResponse(list(bus_stops), safe=False)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})

from django.shortcuts import render
import json
from .models import BusStop  # Import your BusStop model

def bus_stops(request):
    stops = BusStop.objects.all()

    # Prepare bus stops data for Google Maps
    bus_stops_data = [
        {"lat": stop.latitude, "lng": stop.longitude, "name": stop.name}
        for stop in stops
    ]
    bus_stops_json = json.dumps(bus_stops_data)

    if request.user.role == 'manager':
        return render(
            request,
            'transport/manager_bus_stops.html',
            {'bus_stops': stops, 'bus_stops_json': bus_stops_json}
        )
    else:
        return render(
            request,
            'transport/bus_stops.html',
            {'bus_stops': stops, 'bus_stops_json': bus_stops_json}
        )

    
    
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


def manage_trip_students(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    all_students = User.objects.filter(role='student')

    if request.method == 'POST':
        # Handle adding or removing students
        selected_students = request.POST.getlist('students')
        trip.students.set(selected_students)  # Update Many-to-Many relationship
        trip.current_students_count = trip.students.count()
        trip.save()
        return redirect('manage_trip_students', trip_id=trip_id)

    return render(request, 'transport/manage_trip_students.html', {
        'trip': trip,
        'all_students': all_students,
        'selected_students': trip.students.all()
    })
    
# VEHICLES 
    
from django.shortcuts import render, redirect
from .forms import VehicleForm
from .models import Vehicle

def add_vehicle(request):
    # Handle form submission
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_vehicle')  # Redirect to refresh the page after saving

    # Fetch all saved vehicles
    vehicles = Vehicle.objects.all()

    # Render the page with the form and saved vehicles
    form = VehicleForm()
    return render(request, 'transport/add_vehicle.html', {'form': form, 'vehicles': vehicles})

from django.shortcuts import get_object_or_404

def delete_vehicle(request, vehicle_id):
    # Fetch and delete the vehicle
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    vehicle.delete()
    return redirect('add_vehicle')  # Redirect back to the add vehicle page


# ROUTES

from django.shortcuts import render, redirect, get_object_or_404
from .forms import RouteForm
from .models import Route

def add_route(request):
    # Handle form submission
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_route')  # Redirect to refresh the page after saving

    # Fetch all saved routes
    routes = Route.objects.all()

    # Render the page with the form and saved routes
    form = RouteForm()
    return render(request, 'transport/add_route.html', {'form': form, 'routes': routes})

def delete_route(request, route_id):
    # Fetch and delete the route
    route = get_object_or_404(Route, id=route_id)
    route.delete()
    return redirect('add_route')  # Redirect back to the add route page



# ASSIGNMENTS

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Assignment

@login_required
def delete_driver_assignment(request, assignment_id):
    """Handles deleting a driver's assignment (Manager Only)"""
    if request.user.role != 'manager':
        messages.error(request, "You do not have permission to delete assignments.")
        return redirect('manager_dashboard')  # Redirect unauthorized users

    # ✅ Get the assignment or return 404 if not found
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # ✅ Delete the assignment
    assignment.delete()
    messages.success(request, "Driver assignment deleted successfully.")

    return redirect('assign_driver')  # Redirect back to assignment page


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AssignmentForm
from .models import Assignment, Route, BusStop  # Ensure BusStop is imported
from .utils import fetch_route_traffic_data, calculate_fuel_cost  # Utility functions
from .utils import seconds_to_time, time_to_seconds # Utility functions
from datetime import time, timedelta, datetime

@login_required
def assign_driver(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            
            assignment = form.save(commit=False)

            # Debug: Print form data
            print("Form data:", form.cleaned_data)

            # Fetch the selected route
            route = assignment.route

            try:
                # Fetch start and end stops from the route
                start_stop = BusStop.objects.get(id=route.start_stop_id)
                end_stop = BusStop.objects.get(id=route.end_stop_id)
                
                start_time = request.POST.get('start_time')

                # Get their latitude and longitude
                start_stop_coords = {"lat": start_stop.latitude, "lng": start_stop.longitude}
                end_stop_coords = {"lat": end_stop.latitude, "lng": end_stop.longitude}

                print(f"Start Stop: {start_stop_coords}, End Stop: {end_stop_coords}")

                # Fetch route traffic data (distance and time)
                traffic_data = fetch_route_traffic_data(start_stop_coords, end_stop_coords)

                # Calculate travel cost based on traffic data
                avg_mileage = 12.0  # Average mileage in km/l
                fuel_price = 280.0  # Fuel price per liter
                travel_cost = calculate_fuel_cost(traffic_data['distance'], avg_mileage, fuel_price)

                # Save travel time and cost to the assignment
                # assignment.travel_time = traffic_data['time']
                print("hiyy")
                # assignment.end_time = time(hour=15, minute=45, second=22)
                start_time_str = request.POST.get('start_time')
                print(start_time_str)
                assignment.start_time = start_time_str
                # print(assignment.end_time)
                assignment.travel_time = timedelta(seconds=int(traffic_data['time']))
                print(traffic_data['time'])  # Inspect the value
                print(assignment.travel_time)
                start_time = datetime.strptime(start_time_str, "%H:%M").time()  # ✅ Convert to time object
                assignment.start_time = start_time
                
                start_datetime = datetime.combine(datetime.today(), start_time)  # Convert time to datetime
                end_datetime = start_datetime + assignment.travel_time  # ✅ Add timedelta
                assignment.end_time = end_datetime.time()  # ✅ Convert back to time
                
                assignment.travel_cost = travel_cost
                print(assignment.travel_cost)
                assignment.save()  # Save the assignment to the database

                print("Assignment saved successfully:", assignment)

                messages.success(request, "Driver assigned successfully with travel details calculated.")
                return redirect('assign_driver')

            except BusStop.DoesNotExist as e:
                print("BusStop error:", e)
                messages.error(request, f"Error fetching start or end stop details: {e}")
            except Exception as e:
                print("Error:", e)
                messages.error(request, f"Error calculating route details: {e}")
        else:
            print("Form errors:", form.errors)

    else:
        form = AssignmentForm()

    # Fetch assignments for the list
    assignments = Assignment.objects.select_related('driver', 'vehicle', 'route')
    return render(request, 'transport/assign_driver.html', {'form': form, 'assignments': assignments})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Trip

def delete_assignment(request):
    """Handles trip cancellation for the logged-in student"""
    if request.method == "POST":
        student = request.user

        # ✅ Check if the student has an existing trip
        existing_trip = Trip.objects.filter(assigned_students=student).first()

        if existing_trip:
            # ✅ Remove the student from the assigned trip
            existing_trip.assigned_students.remove(student)

            # ✅ Check if trip becomes empty after removal → delete it
            if existing_trip.assigned_students.count() == 0:
                existing_trip.delete()

            messages.success(request, "Your trip has been canceled successfully.")
        else:
            messages.error(request, "No active trip found to cancel.")

    return redirect("student_trip")  # Redirect back to the trip selection page


def delete_assignment(request):
    """Handles trip cancellation for the logged-in student"""
    if request.method == "POST":
        student = request.user

        # ✅ Check if the student has an existing trip
        existing_trip = Trip.objects.filter(assigned_students=student).first()

        if existing_trip:
            # ✅ Remove the student from the assigned trip
            existing_trip.assigned_students.remove(student)

            # ✅ Check if trip becomes empty after removal → delete it
            if existing_trip.assigned_students.count() == 0:
                existing_trip.delete()

            messages.success(request, "Your trip has been canceled successfully.")
        else:
            messages.error(request, "No active trip found to cancel.")

    return redirect("student_trip")  # Redirect back to the trip selection page


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import Trip, Assignment, BusStop
from transport.utils import find_closest_start_stop

def student_trip(request):
    assigned_trip = None  

    if request.method == "POST":
        if "delete_assignment" in request.POST:
            return delete_assignment(request)
        try:
            # ✅ Parse input values safely
            current_lat = float(request.POST.get("current_lat"))
            current_lng = float(request.POST.get("current_lng"))
            destination_stop_id = int(request.POST.get("destination_stop_id"))

            # ✅ Fetch all assignments with routes ending at the chosen stop
            assignments = Assignment.objects.filter(route__end_stop_id=destination_stop_id).select_related("route", "vehicle")

            if not assignments.exists():
                messages.error(request, "No available trips to this destination.")
                return redirect("student_trip")

            # ✅ Collect start stop IDs from all available assignments
            start_stop_ids = list(assignments.values_list("route__start_stop_id", flat=True))

            # ✅ Fetch all start stops in one query (Avoid recursion)
            bus_stops = {stop.id: stop for stop in BusStop.objects.filter(id__in=start_stop_ids)}

            # ✅ Find the closest start stop
            start_stops = [(stop.id, stop.latitude, stop.longitude) for stop in bus_stops.values()]
            closest_start_stop_id = find_closest_start_stop((current_lat, current_lng), start_stops)

            if not closest_start_stop_id:
                messages.error(request, "No valid start stop found.")
                return redirect("student_trip")

            # ✅ Find the matching assignment for this start stop
            selected_assignment = assignments.filter(
                route__start_stop_id=closest_start_stop_id
            ).first()

            if not selected_assignment:
                messages.error(request, "No valid trip found for your selected route.")
                return redirect("student_trip")
            
            # ✅ Check the vehicle capacity before creating the trip
            vehicle_capacity = selected_assignment.vehicle.capacity
            assigned_students_count = selected_assignment.trip_set.aggregate(count=Count('assigned_students'))['count']

            # Check if the vehicle is already at full capacity
            if assigned_students_count >= vehicle_capacity:
                messages.error(request, "The vehicle is already at full capacity. Unable to assign you to this trip.")
                return redirect("student_trip")
            
            # ✅ Check if the trip start time is at least 3 hours from now
            current_time = now().time()
            allowed_time = (now() + timedelta(hours=3)).time()

            if selected_assignment.start_time > allowed_time:
                messages.error(request, "You can only book a trip that starts at least 3 hours from now.")
                return redirect("student_trip")

            # ✅ Remove old assignment if it exists for this student
            existing_trip = Trip.objects.filter(assigned_students=request.user).first()
            if existing_trip:
                existing_trip.assigned_students.remove(request.user)

            # ✅ Fetch or create the trip for this assignment
            trip, created = Trip.objects.get_or_create(assignment=selected_assignment)

            # ✅ Ensure the student is assigned to the trip
            if request.user not in trip.assigned_students.all():
                trip.assigned_students.add(request.user)


            # ✅ Prepare trip details for display
            assigned_trip = {
                "start_stop": bus_stops[closest_start_stop_id].name,
                "end_stop": BusStop.objects.get(id=destination_stop_id).name,
                "route_name": trip.assignment.route.name,
                "vehicle_number": trip.assignment.vehicle.number_plate,
                "departure_time": trip.assignment.start_time.strftime("%H:%M"),
                "students_enrolled": trip.assigned_students.count(),
                "vehicle_capacity": trip.assignment.vehicle.capacity,
            }

            # ✅ Notify the user
            messages.success(request, f"You have been assigned to this trip! Start at {assigned_trip['start_stop']}.")

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    # ✅ Check if the student already has an assigned trip when the page loads
    existing_trip = Trip.objects.filter(assigned_students=request.user).select_related("assignment__route", "assignment__vehicle").first()

    # ✅ Ensure assigned_trip is shown when the page loads if the student already has one
    if existing_trip and assigned_trip is None:
        assigned_trip = {
            "start_stop": existing_trip.assignment.route.start_stop.name,
            "end_stop": existing_trip.assignment.route.end_stop.name,
            "route_name": existing_trip.assignment.route.name,
            "vehicle_number": existing_trip.assignment.vehicle.number_plate,
            "departure_time": existing_trip.assignment.start_time.strftime("%H:%M"),
            "students_enrolled": existing_trip.assigned_students.count(),
            "vehicle_capacity": existing_trip.assignment.vehicle.capacity,
        }

    return render(request, "transport/student_trip.html", {
        "bus_stops": BusStop.objects.all(),
        "assigned_trip": assigned_trip
    })

## Driver Functions

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assignment, Trip

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Assignment, Trip

@login_required
def driver_dashboard(request):
    """View for drivers to see their assigned trips"""
    driver_assignments = Assignment.objects.filter(driver=request.user).select_related("route", "vehicle")

    assignments_with_trips = []
    
    for assignment in driver_assignments:
        trip = Trip.objects.filter(assignment=assignment).first()  # Get the trip if exists

        assignments_with_trips.append({
            "route_name": assignment.route.name,
            "vehicle_number": assignment.vehicle.number_plate,
            "start_time": assignment.start_time.strftime("%I:%M %p"),  # Format AM/PM
            "capacity": assignment.vehicle.capacity,
            "trip_exists": bool(trip),  # ✅ Check if trip exists
            "trip": trip,  # Pass trip object to template if available
            "onboard_students": trip.onboard_students.count() if trip else 0,
            "assigned_students": trip.assigned_students.count() if trip else 0,
        })

    return render(request, "transport/driver_dashboard.html", {"assignments": assignments_with_trips})


@login_required
def toggle_onboard_status(request, trip_id, student_id):
    """Toggle onboard status for a student in a trip"""
    trip = get_object_or_404(Trip, id=trip_id, assignment__driver=request.user)

    # ✅ Ensure the student is assigned to the trip
    if student_id in trip.assigned_students.values_list("id", flat=True):
        if student_id in trip.onboard_students.values_list("id", flat=True):
            trip.onboard_students.remove(student_id)  # Remove from onboard
        else:
            trip.onboard_students.add(student_id)  # Add to onboard
        trip.save()
        messages.success(request, "Onboard status updated.")
    else:
        messages.error(request, "Student is not assigned to this trip.")

    return redirect("driver_dashboard")

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Trip
from payments.models import Payment
from django.utils.timezone import now


@login_required
def student_dashboard(request):
    """Displays the student dashboard with trip & payment details"""
    
    student = request.user  # Get the logged-in student
    
    # ✅ Fetch the assigned trip (if any)
    assigned_trip = Trip.objects.filter(assigned_students=student).select_related(
        "assignment__route", "assignment__vehicle"
    ).first()

    trip_info = None
    if assigned_trip:
        trip_info = {
            "route_name": assigned_trip.assignment.route.name,
            "start_stop": assigned_trip.assignment.route.start_stop.name,
            "end_stop": assigned_trip.assignment.route.end_stop.name,
            "vehicle_number": assigned_trip.assignment.vehicle.number_plate,
            "departure_time": assigned_trip.assignment.start_time.strftime("%H:%M"),
            "students_enrolled": assigned_trip.assigned_students.count(),
            "vehicle_capacity": assigned_trip.assignment.vehicle.capacity,
        }

    # ✅ Fetch the most recent payment (to check due status)
    latest_payment = Payment.objects.filter(student=student).order_by("-due_date").first()

    payment_status = None
    if latest_payment:
        if latest_payment.status == "pending":
            payment_status = {
                "status": "Due",
                "amount": latest_payment.amount,
                "due_date": latest_payment.due_date.strftime("%Y-%m-%d"),
            }
        else:
            next_due_date = latest_payment.due_date + timedelta(days=30)  # Next month's due date
            payment_status = {
                "status": "Paid",
                "next_due_date": next_due_date.strftime("%Y-%m-%d"),
            }

    return render(request, "transport/student_dashboard.html", {
        "trip_info": trip_info,
        "payment_status": payment_status
    })
    
    
from django.shortcuts import render
from .models import Assignment, Vehicle, Trip
from payments.models import Payment

def manager_dashboard(request):
    if request.user.role != 'manager':
        return redirect('home')

    # ✅ Fetch assignments with related fields (Correct field name used)
    assignments = Assignment.objects.select_related("driver", "vehicle", "route")

    # ✅ Fetch all vehicles
    vehicles = Vehicle.objects.all()

    # ✅ Fetch trips with student count
    trips = Trip.objects.prefetch_related("assigned_students")

    # ✅ Fetch latest payments
    recent_payments = Payment.objects.order_by("-due_date")[:10]  # Last 10 payments

    return render(request, "transport/manager_dashboard.html", {
        "assignments": assignments,
        "vehicles": vehicles,
        "trips": trips,
        "recent_payments": recent_payments
    })


