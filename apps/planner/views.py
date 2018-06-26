from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'planner/index.html')

def createUser(request):
	result = User.objects.validateRegistration(request.POST)
	if type(result) is list:
		for error in result:
			messages.error(request, error)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
	return redirect('/travels')

def login(request):
	result = User.objects.validateLogin(request.POST)
	if type(result) is str:
		messages.error(request, result)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		return redirect('/travels')

def travels(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'all_trips': Trip.objects.exclude(joined_by=request.session['user_id']),
        'trip': Trip.objects.filter(created_by=request.session['user_id']),
        'joined': Trip.objects.filter(joined_by=request.session['user_id'])
    }
    return render(request, 'planner/travels.html', context)

def addtrip(request):
    return render(request, 'planner/add.html')

def postTrip(request):
    result = Trip.objects.validateTrip(request.POST, request.POST['user_id'])
    if type(result) is list:
        for error in result:
            messages.error(request, error)
        return redirect('/addtrip')
    else:
        return redirect('/travels')

def view(request, trip_id):
    context = {
        'view': Trip.objects.filter(id=trip_id),
        'joined': User.objects.filter(joined=trip_id)
    }
    return render(request, 'planner/view.html', context)

def join(request):
    this_trip = Trip.objects.get(id=request.POST['trip_id'])
    this_user = User.objects.get(id=request.session['user_id'])
    this_trip.joined_by.add(this_user)
    this_trip.save()
    return redirect('/travels')

def cancel(request, trip_id):
    this_trip = Trip.objects.get(id=trip_id)
    this_user = User.objects.get(id=request.session['user_id'])
    this_trip.joined_by.remove(this_user)
    this_trip.save()
    return redirect('/travels')
def logout(request):
    request.session.clear()
    return redirect('/')

def delete(request, trip_id):
    this = Trip.objects.get(id=trip_id)
    this.delete()
    return redirect('/travels')
# Create your views here.
