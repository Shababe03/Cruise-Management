from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission, BaseUserManager
from django.db import models

# User and Profile-Related Models
class UserModuleManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class UserModule(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    
    objects = UserModuleManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        related_name='user_module_set',
        blank=True,
        help_text="Groups this user belongs to."
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_module_permissions_set',
        blank=True,
        help_text="Specific permissions for this user."
    )

    def __str__(self):
        return self.email
    
class UserRole(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ActivityLog(models.Model):
    user = models.ForeignKey(UserModule, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"

class Admin(models.Model):
    user = models.OneToOneField(UserModule, on_delete=models.CASCADE, related_name='admin_profile')
    managed_cruises = models.ManyToManyField('Cruise', related_name='managed_by_admin')

    def __str__(self):
        return f"Admin: {self.user.username}"

class Employee(models.Model):
    user = models.OneToOneField(UserModule, on_delete=models.CASCADE, related_name='employee_profile')
    position = models.CharField(max_length=100)
    tasks = models.ManyToManyField('Task', related_name='employees')
    
    def __str__(self):
        return f"Employee: {self.user.username}"

class Customer(models.Model):
    user = models.OneToOneField(UserModule, on_delete=models.CASCADE, related_name='customer_profile')
    loyalty_points = models.IntegerField(default=0)
    bookings = models.ManyToManyField('Booking', through='CustomerBooking', related_name='customer_bookings_set')
    preferred_cabin_type = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Customer: {self.user.username}"

class LoyaltyProgram(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='loyalty_program')
    points = models.IntegerField(default=0)
    level = models.CharField(max_length=50, default='Bronze')

    def __str__(self):
        return f"Loyalty Program for {self.customer.user.username}"

class SpecialRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='special_requests')
    request_type = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return f"Special Request by {self.customer.user.username} - {self.request_type}"

# Cruise-Related Models
class Cruise(models.Model):
    name = models.CharField(max_length=100)
    destinations = models.ManyToManyField('Destination', related_name='cruises')
    start_date = models.DateField()
    end_date = models.DateField()
    cabins_available = models.IntegerField()

    def __str__(self):
        destinations_names = ", ".join(destination.name for destination in self.destinations.all())
        return f"Cruise: {self.name} to {destinations_names}"

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    average_temperature = models.CharField(max_length=50, blank=True, null=True)
    best_time_to_visit = models.CharField(max_length=100, blank=True, null=True)
    activities = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class OnboardService(models.Model):
    cruise = models.ForeignKey(Cruise, on_delete=models.CASCADE, related_name='onboard_services')
    service_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    availability = models.BooleanField(default=True)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Service: {self.service_name} on {self.cruise.name}"

# Booking and Payment Models
class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='booking_list')
    cruise = models.ForeignKey(Cruise, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    cabin_number = models.CharField(max_length=10)
    additional_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking: {self.cruise.name} by {self.customer.user.username}"

class CustomerBooking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    is_refunded = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for {self.booking.cruise.name}, Amount: {self.amount}"

class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='invoice')
    issued_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice for {self.booking}"

class RefundRequest(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='refund_requests')
    request_date = models.DateField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Refund Request for {self.booking}"

# Employee Management and Task Models
class Task(models.Model):
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Task: {self.description}, Due: {self.due_date}"

class Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='shifts')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    shift_type = models.CharField(max_length=50)

    def __str__(self):
        return f"Shift for {self.employee.user.username} on {self.start_time.date()}"

class ShiftSwapRequest(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='swap_requests')
    requested_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='requested_swaps')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Swap Request for {self.shift} by {self.requested_by.user.username}"

# Promotions and Inventory Management
class Promotion(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Campaign: {self.title}"

class CustomerSegment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    criteria = models.TextField()  # Define criteria for segmentation

    def __str__(self):
        return f"Segment: {self.name}"

class Inventory(models.Model):
    cruise = models.ForeignKey(Cruise, on_delete=models.CASCADE, related_name='inventory')
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Inventory: {self.item_name} on {self.cruise.name}"

# Feedback Models
class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='feedbacks')
    cruise = models.ForeignKey(Cruise, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveIntegerField(default=0)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Feedback by {self.customer.user.username} for {self.cruise.name}"

class Itinerary(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='itineraries')
    day = models.IntegerField()
    activity = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Itinerary Day {self.day} for {self.booking}"
