from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer, UserSerializer


# ── Static HTML views ──────────────────────────────────────────────────────────

def index(request):
    return render(request, 'index.html', {})


# ── Menu API ───────────────────────────────────────────────────────────────────

class MenuItemsView(generics.ListCreateAPIView):
    """
    GET  /restaurant/menu/        → list all menu items
    POST /restaurant/menu/        → create a menu item (auth required)
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /restaurant/menu/<pk>/  → retrieve a single item
    PUT    /restaurant/menu/<pk>/  → full update
    PATCH  /restaurant/menu/<pk>/  → partial update
    DELETE /restaurant/menu/<pk>/  → delete
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


# ── Booking API ────────────────────────────────────────────────────────────────

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet handles all CRUD for table bookings.
    All actions require authentication.

    GET    /restaurant/booking/        → list bookings
    POST   /restaurant/booking/        → create booking
    GET    /restaurant/booking/<pk>/   → retrieve booking
    PUT    /restaurant/booking/<pk>/   → full update
    PATCH  /restaurant/booking/<pk>/   → partial update
    DELETE /restaurant/booking/<pk>/   → delete
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


# ── User views (convenience) ────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """GET /restaurant/users/me/ → return the currently authenticated user."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserListView(generics.ListAPIView):
    """GET /restaurant/users/ → list all users (auth required)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
