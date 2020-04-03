import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from oauth2_provider.models import Application
class Command(BaseCommand):
    help = "Creates an Consuming Application user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--client_id', help="The Client ID", default=os.getenv("TRONTHEIM_CLIENTID", "weak_id"))
        parser.add_argument('--redirect', help="Redirect URIS", default=os.getenv("TRONTHEIM_REDIRECT", "http://localhost:3000"))
        parser.add_argument('--client_secret', help="The Client Secret", default=os.getenv("TRONTHEIM_CLIENTSECRET", "weak_secret"))

    def handle(self, *args, **options):

        if not Application.objects.filter(client_id=options['client_id']).exists():
            Application.objects.create(name="Trontheim",
                                      user_id=1,
                                      client_type="confidential",
                                      redirect_uris=options['redirect'],
                                    client_id= options['client_id'],
                                 client_secret= options['client_secret'],
                                authorization_grant_type="implicit")
            print("Application created")
        else:
            app = Application.objects.get(client_id= options['client_id'])
            app.redirect_uris = options['redirect']
            app.client_id= options['client_id']
            app.client_secret= options['client_secret']
            app.save()
            print("Application already exsisted. Updating")