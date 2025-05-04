from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    path('dashboard/top-products/', views.TopProductsView.as_view(), name='dashboard-top-products'),
    path('dashboard/top-customers/', views.TopCustomersView.as_view(), name='dashboard-top-customers'),
    path('dashboard/revenue/', views.RevenueStatsView.as_view(), name='dashboard-revenue'),
]
