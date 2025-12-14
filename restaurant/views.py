from django.shortcuts import render, redirect
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer, UserSerializer
from .forms import BookingForm


# Static HTML Views
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def book(request):
    form = BookingForm()
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/book/?booked=true')
    
    context = {'form': form}
    return render(request, 'book.html', context)


def reservations(request):
    bookings = Booking.objects.all()
    return render(request, 'bookings.html', {'bookings': bookings})


# API endpoint to get booked slots for a specific date
@api_view(['GET'])
@permission_classes([AllowAny])
def get_booked_slots(request):
    """
    Get all booked time slots for a specific date
    Query parameter: date (YYYY-MM-DD format)
    """
    date_str = request.query_params.get('date')
    
    if not date_str:
        return JsonResponse({'error': 'Date parameter is required'}, status=400)
    
    try:
        # Parse the date string
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    
    # Get all bookings for this date
    booked_slots = Booking.objects.filter(reservation_date=date_obj).values_list('reservation_slot', flat=True)
    booked_slots = list(booked_slots)
    
    return JsonResponse({
        'date': date_str,
        'booked_slots': booked_slots,
        'available_slots': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    })


# API Views

# Menu API ViewSet
class MenuItemsView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]


# Booking API ViewSet
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


# User Registration
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=201)
    return Response(serializer.errors, status=400)