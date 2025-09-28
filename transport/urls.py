from django.urls import path
from . import views

urlpatterns = [
    path('delete-bus-stop/', views.delete_stop, name='delete_stop'),
    path('get-stops/', views.get_bus_stops, name='get_stops'),
    path('add-bus-stop/', views.add_stop, name='add_stop'),
    path('bus-stops/', views.bus_stops, name='bus_stops'),
    path('routes/', views.routes, name='routes'),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('delete-vehicle/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('add-route/', views.add_route, name='add_route'),
    path('delete-route/<int:route_id>/', views.delete_route, name='delete_route'),
    path('assign-driver/', views.assign_driver, name='assign_driver'),
    path("delete-assignment/<int:assignment_id>/", views.delete_assignment, name="delete_assignment"),
    path('get_route/', views.get_route, name='get_route'),
    path('student-trip/', views.student_trip, name='student_trip'),
    path('driver-dashboard/', views.driver_dashboard, name="driver_dashboard"),
    path('toggle-onboard/<int:trip_id>/<int:student_id>/', views.toggle_onboard_status, name="toggle_onboard_status"),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path("manager-dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path('delete-driver-assignment/<int:assignment_id>/', views.delete_driver_assignment, name='delete_driver_assignment'),
]
