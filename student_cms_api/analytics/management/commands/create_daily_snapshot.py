from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, date
from analytics.models import AnalyticsSnapshot, DepartmentAnalytics


class Command(BaseCommand):
    help = 'Create daily analytics snapshot'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date for snapshot in YYYY-MM-DD format (default: today)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force create snapshot even if it already exists',
        )

    def handle(self, *args, **options):
        # Parse date
        if options['date']:
            try:
                snapshot_date = datetime.strptime(options['date'], '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('Invalid date format. Use YYYY-MM-DD')
                )
                return
        else:
            snapshot_date = timezone.now().date()

        self.stdout.write(f'Creating analytics snapshot for {snapshot_date}...')

        # Check if snapshot already exists
        if AnalyticsSnapshot.objects.filter(snapshot_date=snapshot_date).exists():
            if not options['force']:
                self.stdout.write(
                    self.style.WARNING(
                        f'Snapshot for {snapshot_date} already exists. Use --force to recreate.'
                    )
                )
                return
            else:
                # Delete existing snapshot
                AnalyticsSnapshot.objects.filter(snapshot_date=snapshot_date).delete()
                DepartmentAnalytics.objects.filter(snapshot_date=snapshot_date).delete()
                self.stdout.write('Deleted existing snapshot.')

        try:
            # Create main snapshot
            snapshot = AnalyticsSnapshot.create_daily_snapshot(snapshot_date)
            self.stdout.write(
                self.style.SUCCESS(f'Created analytics snapshot: {snapshot.id}')
            )

            # Create department snapshots
            dept_snapshots = DepartmentAnalytics.create_department_snapshots(snapshot_date)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created {len(dept_snapshots)} department analytics snapshots'
                )
            )

            # Display summary
            self.stdout.write('\nSnapshot Summary:')
            self.stdout.write(f'Date: {snapshot.snapshot_date}')
            self.stdout.write(f'Total Complaints: {snapshot.total_complaints}')
            self.stdout.write(f'Resolved Complaints: {snapshot.resolved_complaints}')
            self.stdout.write(f'Total Feedback: {snapshot.total_feedback}')
            self.stdout.write(f'Average Rating: {snapshot.average_rating}')
            self.stdout.write(f'Total Users: {snapshot.total_users}')
            self.stdout.write(f'Active Users Today: {snapshot.active_users_today}')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating snapshot: {str(e)}')
            )

