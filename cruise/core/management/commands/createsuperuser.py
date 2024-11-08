from django.core.management.commands import createsuperuser
from django.utils.translation import gettext_lazy as _
from core.models import UserModule

class Command(createsuperuser.Command):
    help = _("Create a superuser, setting the role to 'admin'")

    def handle(self, *args, **kwargs):
        # Call the parent class to handle the regular superuser creation
        super().handle(*args, **kwargs)
        
        # After superuser is created, update the role field
        username = kwargs.get('username')
        user = UserModule.objects.get(username=username)
        user.role = 'admin'
        user.save()

        print(f"Superuser created with role='admin' for user {username}")
