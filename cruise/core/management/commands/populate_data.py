from django.core.management.base import BaseCommand
from core.models import Destination, OnboardService, Cruise

class Command(BaseCommand):
    help = 'Populate Cruises, Destinations, and Services'

    def handle(self, *args, **options):
        # Add destinations first
        destinations_data = [
            {
                "name": "The Caribbean",
                "description": "A tropical paradise with beautiful beaches.",
                "average_temperature": "80°F",
                "best_time_to_visit": "December to April",
                "activities": "Snorkeling, Diving, Sunbathing",
            },
            {
                "name": "Alaska",
                "description": "Majestic landscapes and stunning wildlife.",
                "average_temperature": "50°F",
                "best_time_to_visit": "May to September",
                "activities": "Hiking, Whale Watching, Glacier Tours",
            },
            {
                "name": "Mediterranean",
                "description": "Rich in history and culture.",
                "average_temperature": "75°F",
                "best_time_to_visit": "April to June",
                "activities": "Sightseeing, Wine Tasting, Beach Days",
            },
            {
                "name": "The Bahamas",
                "description": "An archipelago known for its crystal-clear waters.",
                "average_temperature": "78°F",
                "best_time_to_visit": "December to April",
                "activities": "Scuba Diving, Fishing, Island Hopping",
            },
            {
                "name": "The Nile",
                "description": "Experience the wonders of ancient Egypt.",
                "average_temperature": "85°F",
                "best_time_to_visit": "October to April",
                "activities": "River Cruising, Cultural Tours",
            },
            {
                "name": "Hawaii",
                "description": "Beautiful islands with lush landscapes.",
                "average_temperature": "77°F",
                "best_time_to_visit": "April to October",
                "activities": "Surfing, Hiking, Luau",
            },
        ]

        # Create and save destinations
        destination_instances = []
        for data in destinations_data:
            destination, created = Destination.objects.get_or_create(**data)
            destination_instances.append(destination)

        # Add cruises next
        cruises_data = [
            {
                "name": "Caribbean Dream",
                "start_date": "2024-03-01",
                "end_date": "2024-03-08",
                "cabins_available": 150,
            },
            {
                "name": "Alaska Wilderness Adventure",
                "start_date": "2024-06-10",
                "end_date": "2024-06-17",
                "cabins_available": 100,
            },
            {
                "name": "Mediterranean Marvels",
                "start_date": "2024-05-15",
                "end_date": "2024-05-22",
                "cabins_available": 200,
            },
            {
                "name": "Hawaii Island Adventure",
                "start_date": "2024-07-01",
                "end_date": "2024-07-14",
                "cabins_available": 120,
            },
            {
                "name": "Nile River Adventure",
                "start_date": "2024-09-05",
                "end_date": "2024-09-12",
                "cabins_available": 180,
            },
            {
                "name": "Bahamas Escape",
                "start_date": "2024-11-20",
                "end_date": "2024-11-27",
                "cabins_available": 90,
            },
        ]

        cruise_instances = []
        for cruise_data in cruises_data:
            cruise, created = Cruise.objects.get_or_create(**cruise_data)
            cruise_instances.append(cruise)

            # Associate destinations with the cruise instance
            for destination in destination_instances:
                cruise.destinations.add(destination)  # Use add() to associate with the Many-to-Many field

        # Add onboard services
        services_data = [
            {
                "service_name": "Onboard Dining",
                "service_type": "Meal",
                "description": "Gourmet dining options from world-renowned chefs.",
                "duration": "2 hours",
                "availability": True,
                "additional_info": "Reservations recommended."
            },
            {
                "service_name": "Spa & Wellness",
                "service_type": "Activity",
                "description": "Relax and rejuvenate at our luxurious spa.",
                "duration": "1 hour",
                "availability": True,
                "additional_info": "Various treatments available."
            },
            {
                "service_name": "Exclusive Shore Excursions",
                "service_type": "Activity",
                "description": "Private VIP shore excursions.",
                "duration": "Half-day",
                "availability": True,
                "additional_info": "Limited spots available."
            },
            {
                "service_name": "Concierge Services",
                "service_type": "Service",
                "description": "Personalized assistance for bookings.",
                "duration": "Ongoing",
                "availability": True,
                "additional_info": "Contact concierge for help."
            },
            {
                "service_name": "Private Butler Service",
                "service_type": "Service",
                "description": "Dedicated butler services for premium suite guests.",
                "duration": "24/7",
                "availability": True,
                "additional_info": "Available upon request."
            },
            {
                "service_name": "Priority Boarding & Disembarkation",
                "service_type": "Service",
                "description": "Skip the lines for a seamless experience.",
                "duration": "Varies",
                "availability": True,
                "additional_info": "Available for premium guests."
            },
            {
                "service_name": "In-Suite Dining with Private Chef",
                "service_type": "Meal",
                "description": "Personalized dining experience in your suite.",
                "duration": "2 hours",
                "availability": True,
                "additional_info": "Must be arranged in advance."
            },
            {
                "service_name": "Personal Fitness Trainers",
                "service_type": "Activity",
                "description": "Access personal trainers for tailored fitness sessions.",
                "duration": "1 hour",
                "availability": True,
                "additional_info": "Private sessions available."
            },
            {
                "service_name": "Pet Care & Companion Services",
                "service_type": "Service",
                "description": "Travel worry-free with pet-friendly accommodations.",
                "duration": "Varies",
                "availability": True,
                "additional_info": "Available for suite guests."
            },
            {
                "service_name": "Exclusive Lounge Access",
                "service_type": "Service",
                "description": "Access to private lounges with refreshments.",
                "duration": "Ongoing",
                "availability": True,
                "additional_info": "Access for premium guests."
            },
            {
                "service_name": "Photography & Videography",
                "service_type": "Service",
                "description": "Capture unforgettable memories with professional services.",
                "duration": "Varies",
                "availability": True,
                "additional_info": "Booking required."
            },
            {
                "service_name": "Personalized Luxury Spa",
                "service_type": "Activity",
                "description": "Custom spa treatments tailored just for you.",
                "duration": "1 hour",
                "availability": True,
                "additional_info": "Must be booked in advance."
            },
        ]

        for service_data in services_data:
            cruise = Cruise.objects.first()  # Example: Associate with the first cruise
            OnboardService.objects.get_or_create(cruise=cruise, **service_data)

        self.stdout.write(self.style.SUCCESS('Destinations, Services, and Cruises have been added successfully.'))
