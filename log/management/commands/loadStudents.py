# your_app/management/commands/import_students.py
import csv
from django.core.management.base import BaseCommand
from log.models import Student

class Command(BaseCommand):
    help = 'Import student data from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                uid = row['uid']
                # Create or update student object
                student, created = Student.objects.get_or_create(uid=uid, defaults={'name': name})
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created student: {name} (UID: {uid})'))
                else:
                    self.stdout.write(self.style.WARNING(f'Student already exists: {name} (UID: {uid})'))
