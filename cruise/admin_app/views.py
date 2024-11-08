from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.http import Http404
from django.apps import apps
from django.urls import reverse, NoReverseMatch
from django.forms import modelform_factory
from .forms import get_dynamic_form
from django.contrib.auth.decorators import login_required
from core.models import (
    UserModule, Cruise, Destination, Booking, Employee, Customer,
    Task, Promotion, Inventory, Feedback, ActivityLog
)

# Main dashboard view
@login_required
def admin_dashboard(request):
    context = {
        'user_count': UserModule.objects.count(),
        'cruise_count': Cruise.objects.count(),
        'destination_count': Destination.objects.count(),
        'booking_count': Booking.objects.count(),
        'employee_count': Employee.objects.count(),
        'customer_count': Customer.objects.count(),
        'task_count': Task.objects.count(),
        'promotion_count': Promotion.objects.count(),
        'inventory_count': Inventory.objects.count(),
        'feedback_count': Feedback.objects.count(),
        'activity_log_count': ActivityLog.objects.count(),
    }
    return render(request, 'admin_app/dashboard.html', context)

# Model list views
@login_required
def usermodule_list(request):
    users = UserModule.objects.all()
    return render(request, 'admin_app/models/usermodule_list.html', {'users': users})

@login_required
def cruise_list(request):
    cruises = Cruise.objects.all()
    return render(request, 'admin_app/models/cruise_list.html', {'cruises': cruises})

@login_required
def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'admin_app/models/destination_list.html', {'destinations': destinations})

@login_required
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'admin_app/models/booking_list.html', {'bookings': bookings})

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'admin_app/models/employee_list.html', {'employees': employees})

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'admin_app/models/customer_list.html', {'customers': customers})

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'admin_app/models/task_list.html', {'tasks': tasks})

@login_required
def promotion_list(request):
    promotions = Promotion.objects.all()
    return render(request, 'admin_app/models/promotion_list.html', {'promotions': promotions})

@login_required
def inventory_list(request):
    inventory = Inventory.objects.all()
    return render(request, 'admin_app/models/inventory_list.html', {'inventory': inventory})

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'admin_app/models/feedback_list.html', {'feedbacks': feedbacks})

@login_required
def activitylog_list(request):
    logs = ActivityLog.objects.all()
    return render(request, 'admin_app/models/activitylog_list.html', {'logs': logs})

# Login, logout, and other admin views
def custom_admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')  # Ensure this is unique

        # Check if the username already exists
        if UserModule.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'admin_app/login.html')

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_active and user.role == 'admin':
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            messages.error(request, 'Invalid email or password for admin.')
            return render(request, 'admin_app/login.html')

    return render(request, 'admin_app/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')

class EditModelView(View):
    def get(self, request, model_name, pk):
        model = apps.get_model('core', model_name)
        obj = get_object_or_404(model, pk=pk)
        form_class = modelform_factory(model, exclude=[])
        form = form_class(instance=obj)

        # Generate list URL based on model name
        list_url = reverse(f'{model_name}_list')

        context = {
            'form': form,
            'object': obj,
            'model_verbose_name': model._meta.verbose_name,
            'list_url': list_url,  # Pass list URL here
        }
        return render(request, 'admin_app/models/edit_model.html', context)

    def post(self, request, model_name, pk):
        model = apps.get_model('core', model_name)
        obj = get_object_or_404(model, pk=pk)
        form_class = modelform_factory(model, exclude=[])
        form = form_class(request.POST, instance=obj)

        if form.is_valid():
            form.save()
            messages.success(request, f"{model._meta.verbose_name} updated successfully.")
            return redirect(reverse(f'{model_name}_list'))

        list_url = reverse(f'{model_name}_list')
        
        context = {
            'form': form,
            'object': obj,
            'model_verbose_name': model._meta.verbose_name,
            'list_url': list_url,
        }
        return render(request, 'admin_app/models/edit_model.html', context)
    

class DeleteModelView(View):
    def get(self, request, model_name, pk):
        model = apps.get_model('core', model_name)
        obj = get_object_or_404(model, pk=pk)
        
        # Generate list URL for the cancel button in the confirm delete template
        list_url = reverse(f'{model_name}_list')

        context = {
            'object': obj,
            'model_verbose_name': model._meta.verbose_name,
            'list_url': list_url,
        }
        return render(request, 'admin_app/models/confirm_delete.html', context)

    def post(self, request, model_name, pk):
        model = apps.get_model('core', model_name)
        obj = get_object_or_404(model, pk=pk)
        
        # Capture the list URL before deleting
        list_url = reverse(f'{model_name}_list')
        
        # Delete the object and redirect
        obj.delete()
        messages.success(request, f"{model._meta.verbose_name} deleted successfully.")
        return redirect(list_url)