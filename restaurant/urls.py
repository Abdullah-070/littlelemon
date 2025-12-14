from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

# DRF Router for ViewSets
router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet, basename='booking')

urlpatterns = [
    # Static HTML pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('reservations/', views.reservations, name='reservations'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/menu/', views.MenuItemsView.as_view(), name='menu-list'),
    path('api/menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-detail'),
    path('api/booked-slots/', views.get_booked_slots, name='booked-slots'),
    
    # Authentication
    path('api/register/', views.register, name='register'),
    path('api/token/', obtain_auth_token, name='api-token'),
    path('api-auth/', include('rest_framework.urls')),
]