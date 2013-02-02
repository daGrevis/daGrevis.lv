from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Imports data from legacy"

    def handle(self, *args, **options):
        raise CommandError("I'm alive!")
