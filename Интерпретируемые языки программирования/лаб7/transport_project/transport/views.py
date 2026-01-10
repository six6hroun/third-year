from django.shortcuts import render, get_object_or_404, redirect
from .models import Trips
from .forms import TripForm

def home(request):
    trips = Trips.objects.all()
    return render(request, 'transport/home.html', {'trips': trips})

def trip_detail(request, trip_id):
    trip = get_object_or_404(Trips, pk=trip_id)
    return render(request, 'transport/trip_detail.html', {'trip': trip})

def trip_add(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TripForm()
    return render(request, 'transport/trip_form.html', {'form': form})

def trip_edit(request, trip_id):
    trip = get_object_or_404(Trips, pk=trip_id)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('trip_detail', trip_id=trip.id)
    else:
        form = TripForm(instance=trip)
    return render(request, 'transport/trip_form.html', {'form': form})