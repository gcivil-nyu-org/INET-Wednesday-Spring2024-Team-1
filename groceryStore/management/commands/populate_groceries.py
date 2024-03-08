from django.core.management.base import BaseCommand
from groceryStore.models import Grocery
import csv

class Command(BaseCommand):
    help = 'Populate the Grocery table from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='path to the file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Grocery.objects.create(
                    gname=row['gname'],
                    price=row['price'],
                    stock=row['stock']
                )

        self.stdout.write(self.style.SUCCESS('Grocery data populated successfully!'))
