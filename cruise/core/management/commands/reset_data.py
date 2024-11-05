from django.core.management.base import BaseCommand
from django.db import connection, transaction
from core.models import (
    UserModule, Admin, Employee, Customer, Destination,
    Cruise, OnboardService, Booking, CustomerBooking, Payment,
    Task, Inventory, Promotion
)

class Command(BaseCommand):
    help = "Reset data and primary key sequences for all models"

    def handle(self, *args, **kwargs):
        models = [
            Promotion, Inventory, Task, Payment, CustomerBooking, Booking,
            OnboardService, Cruise, Destination, Customer, Employee, Admin,
            UserModule
        ]

        with transaction.atomic():
            # Step 1: Delete all data from each model
            for model in models:
                model.objects.all().delete()
                self.stdout.write(self.style.WARNING(f"Deleted data from {model.__name__}"))

            # Step 2: Reset primary key sequences for each model (specific to DB types)
            self.reset_sequences(models)

        self.stdout.write(self.style.SUCCESS("Data reset and primary key sequences reset for all models."))

    def reset_sequences(self, models):
        # Reset ID sequence for each table
        with connection.cursor() as cursor:
            for model in models:
                table_name = model._meta.db_table
                # Resetting based on different DB engines
                if 'sqlite' in connection.settings_dict['ENGINE']:
                    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
                elif 'postgresql' in connection.settings_dict['ENGINE']:
                    cursor.execute(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1;")
                elif 'mysql' in connection.settings_dict['ENGINE']:
                    cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")
                self.stdout.write(self.style.NOTICE(f"Primary key reset for {table_name}"))
