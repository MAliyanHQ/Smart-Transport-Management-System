from django import forms
from .models import Vehicle, Route, Assignment, Trip

# Form for adding/editing vehicles
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['number_plate', 'model', 'capacity', 'description']


# Form for adding/editing routes
class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'start_stop', 'end_stop']

# Form for assigning drivers to vehicles and routes
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['driver', 'vehicle', 'route']
        
# Form for assigning trip to students
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['assignment']
        
    def clean(self):
        """ Ensure the trip doesn't exceed vehicle capacity before saving """
        cleaned_data = super().clean()
        assignment = cleaned_data.get('assignment')

        if assignment:
            # ✅ Get the vehicle capacity
            vehicle_capacity = assignment.vehicle.capacity if assignment.vehicle else 0
            
            # ✅ Get the current number of students in the trip (avoiding recursion)
            trip = Trip.objects.filter(assignment=assignment).first()
            current_student_count = trip.students.count() if trip else 0
            
            if current_student_count >= vehicle_capacity:
                raise forms.ValidationError(f"Trip is full! Max capacity: {vehicle_capacity}")

        return cleaned_data
