from django.contrib import admin
from .models import (
    UserModule,
    Admin,
    Employee,
    Customer,
    Destination,
    Cruise,
    OnboardService,
    Booking,
    CustomerBooking,
    Payment,
    Task,
    Inventory,
    Promotion,
)

# Register the models in the Django admin
admin.site.register(UserModule)
admin.site.register(Admin)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Destination)
admin.site.register(Cruise)
admin.site.register(OnboardService)
admin.site.register(Booking)
admin.site.register(CustomerBooking)
admin.site.register(Payment)
admin.site.register(Task)
admin.site.register(Inventory)
admin.site.register(Promotion)
