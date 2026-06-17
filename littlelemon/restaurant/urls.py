from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'booking', views.BookingViewSet, basename='booking')

urlpatterns = [
    # Static HTML
    path('', views.index, name='index'),

    # Menu API
    path('menu/', views.MenuItemsView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-detail'),

    # Booking API (router generates all CRUD paths)
    path('', include(router.urls)),

    # User endpoints
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/me/', views.current_user, name='current-user'),
]
