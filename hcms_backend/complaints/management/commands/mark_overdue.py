from django.core.management.base import BaseCommand
from django.utils import timezone

from complaints.models import Complaint


class Command(BaseCommand):
    help = 'Mark complaints overdue whose SLA deadline has passed'

    def handle(self, *args, **options):
        now = timezone.now()
        qs = (
            Complaint.objects
            .filter(is_overdue=False)
            .exclude(status='Resolved')
            .filter(sla_deadline__isnull=False, sla_deadline__lt=now)
        )

        updated = qs.update(is_overdue=True)

        self.stdout.write(self.style.SUCCESS(f'Marked {updated} complaints as overdue'))
