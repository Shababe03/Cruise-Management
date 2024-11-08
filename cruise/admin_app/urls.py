from django.urls import path
from admin_app.views import EditModelView, DeleteModelView
from .views import (
    custom_admin_login, admin_dashboard, admin_logout,
    usermodule_list, cruise_list, destination_list, booking_list,
    employee_list, customer_list, task_list, promotion_list,
    inventory_list, feedback_list, activitylog_list
)

urlpatterns = [
    # Main urls
    path('', custom_admin_login, name='admin_login'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('logout/', admin_logout, name='admin_logout'),

    # Model list views
    path('usermodule/', usermodule_list, name='usermodule_list'),
    path('cruise/', cruise_list, name='cruise_list'),
    path('destination/', destination_list, name='destination_list'),
    path('booking/', booking_list, name='booking_list'),
    path('employee/', employee_list, name='employee_list'),
    path('customer/', customer_list, name='customer_list'),
    path('task/', task_list, name='task_list'),
    path('promotion/', promotion_list, name='promotion_list'),
    path('inventory/', inventory_list, name='inventory_list'),
    path('feedback/', feedback_list, name='feedback_list'),
    path('activitylog/', activitylog_list, name='activitylog_list'),

    path('<str:model_name>/edit/<int:pk>/', EditModelView.as_view(), name='edit_model'),
    path('<str:model_name>/delete/<int:pk>/', DeleteModelView.as_view(), name='delete_model'),


]
