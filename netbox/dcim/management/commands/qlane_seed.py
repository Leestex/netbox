from django.core.management.base import BaseCommand
from django.db import transaction

from dcim.choices import DeviceStatusChoices
from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Rack, Site

# Sample inventory this test target starts with: (name, mounted in rack R1, status)
DEVICES = (
    ('app-srv-01', True, DeviceStatusChoices.STATUS_ACTIVE),
    ('app-srv-02', True, DeviceStatusChoices.STATUS_ACTIVE),
    ('core-rtr-01', True, DeviceStatusChoices.STATUS_OFFLINE),
    ('db-srv-01', True, DeviceStatusChoices.STATUS_OFFLINE),
    ('edge-fw-01', False, DeviceStatusChoices.STATUS_ACTIVE),
    ('lab-sw-01', False, DeviceStatusChoices.STATUS_ACTIVE),
    ('spare-ap-01', False, DeviceStatusChoices.STATUS_ACTIVE),
)


class Command(BaseCommand):
    help = "Load the sample sites, racks and devices this test target starts with. Safe to run more than once."

    @transaction.atomic
    def handle(self, *args, **options):
        site, _ = Site.objects.get_or_create(slug='lab-1', defaults={'name': 'Lab 1'})
        rack, _ = Rack.objects.get_or_create(site=site, name='R1')
        manufacturer, _ = Manufacturer.objects.get_or_create(slug='generic', defaults={'name': 'Generic'})
        device_type, _ = DeviceType.objects.get_or_create(
            manufacturer=manufacturer, slug='generic-1u', defaults={'model': 'Generic 1U'}
        )
        role, _ = DeviceRole.objects.get_or_create(slug='server', defaults={'name': 'Server'})
        created = 0
        for name, in_rack, status in DEVICES:
            _, is_new = Device.objects.get_or_create(
                site=site,
                name=name,
                defaults={
                    'device_type': device_type,
                    'role': role,
                    'rack': rack if in_rack else None,
                    'status': status,
                },
            )
            created += is_new
        self.stdout.write(f'Sample devices: {created} created, {len(DEVICES) - created} already present.')
