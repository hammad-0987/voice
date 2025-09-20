from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Department
from complaints.models import Complaint
from withdrawals.models import WithdrawalRequest
from feedback.models import ComplaintFeedback
from notifications.utils import create_notification

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating sample data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            User.objects.filter(is_superuser=False).delete()
            Department.objects.all().delete()
            Complaint.objects.all().delete()
            WithdrawalRequest.objects.all().delete()
            ComplaintFeedback.objects.all().delete()

        self.stdout.write('Creating sample data...')

        # Create departments
        departments = [
            {'name': 'Computer Science', 'code': 'CS', 'description': 'Computer Science Department'},
            {'name': 'Mathematics', 'code': 'MATH', 'description': 'Mathematics Department'},
            {'name': 'Physics', 'code': 'PHY', 'description': 'Physics Department'},
            {'name': 'Chemistry', 'code': 'CHEM', 'description': 'Chemistry Department'},
        ]

        dept_objects = []
        for dept_data in departments:
            dept, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults=dept_data
            )
            dept_objects.append(dept)
            if created:
                self.stdout.write(f'Created department: {dept.name}')

        # Create users
        users_data = [
            # Admin
            {
                'username': 'admin',
                'email': 'admin@studentcms.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': 'admin',
                'password': 'admin123',
            },
            # VC
            {
                'username': 'vc',
                'email': 'vc@studentcms.com',
                'first_name': 'Vice',
                'last_name': 'Chancellor',
                'role': 'vc',
                'password': 'vc123',
            },
            # Department Heads
            {
                'username': 'head_cs',
                'email': 'head.cs@studentcms.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'role': 'head',
                'department': dept_objects[0],  # CS
                'password': 'head123',
            },
            {
                'username': 'head_math',
                'email': 'head.math@studentcms.com',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'role': 'head',
                'department': dept_objects[1],  # Math
                'password': 'head123',
            },
            # Staff
            {
                'username': 'staff_cs1',
                'email': 'staff1.cs@studentcms.com',
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'role': 'staff',
                'department': dept_objects[0],  # CS
                'password': 'staff123',
            },
            {
                'username': 'staff_cs2',
                'email': 'staff2.cs@studentcms.com',
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'role': 'staff',
                'department': dept_objects[0],  # CS
                'password': 'staff123',
            },
            # Students
            {
                'username': 'student1',
                'email': 'student1@studentcms.com',
                'first_name': 'Emma',
                'last_name': 'Brown',
                'role': 'student',
                'department': dept_objects[0],  # CS
                'student_id': 'CS2024001',
                'password': 'student123',
            },
            {
                'username': 'student2',
                'email': 'student2@studentcms.com',
                'first_name': 'Michael',
                'last_name': 'Davis',
                'role': 'student',
                'department': dept_objects[1],  # Math
                'student_id': 'MATH2024001',
                'password': 'student123',
            },
            {
                'username': 'student3',
                'email': 'student3@studentcms.com',
                'first_name': 'Sarah',
                'last_name': 'Miller',
                'role': 'student',
                'department': dept_objects[0],  # CS
                'student_id': 'CS2024002',
                'password': 'student123',
            },
        ]

        created_users = {}
        for user_data in users_data:
            password = user_data.pop('password')
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password(password)
                user.save()
                created_users[user.username] = user
                self.stdout.write(f'Created user: {user.username} ({user.role})')

        # Update department heads
        dept_objects[0].head = created_users.get('head_cs') or User.objects.get(username='head_cs')
        dept_objects[0].save()
        dept_objects[1].head = created_users.get('head_math') or User.objects.get(username='head_math')
        dept_objects[1].save()

        # Create sample complaints
        student1 = User.objects.get(username='student1')
        student2 = User.objects.get(username='student2')
        student3 = User.objects.get(username='student3')
        staff1 = User.objects.get(username='staff_cs1')

        complaints_data = [
            {
                'title': 'Library WiFi Connection Issues',
                'description': 'The WiFi in the library keeps disconnecting during study hours. This is affecting my research work.',
                'priority': 'medium',
                'status': 'pending',
                'created_by': student1,
                'department': dept_objects[0],
            },
            {
                'title': 'Classroom Air Conditioning Not Working',
                'description': 'The AC in Room 301 has been broken for a week. It\'s very hot and uncomfortable for lectures.',
                'priority': 'high',
                'status': 'in_progress',
                'created_by': student2,
                'department': dept_objects[1],
                'assigned_to': staff1,
            },
            {
                'title': 'Cafeteria Food Quality Concern',
                'description': 'The food quality in the cafeteria has declined recently. Several students have complained about taste and freshness.',
                'priority': 'medium',
                'status': 'resolved',
                'created_by': student3,
                'department': dept_objects[0],
                'assigned_to': staff1,
            },
        ]

        created_complaints = []
        for complaint_data in complaints_data:
            complaint = Complaint.objects.create(**complaint_data)
            created_complaints.append(complaint)
            self.stdout.write(f'Created complaint: {complaint.complaint_number}')

        # Create sample withdrawal request
        withdrawal = WithdrawalRequest.objects.create(
            type='semester_withdrawal',
            reason='Due to family emergency, I need to take a semester break to help with family business.',
            submitted_by=student1,
        )
        self.stdout.write(f'Created withdrawal request: {withdrawal.request_number}')

        # Create sample feedback
        resolved_complaint = created_complaints[2]  # The resolved complaint
        feedback = ComplaintFeedback.objects.create(
            complaint=resolved_complaint,
            feedback_text='The issue was resolved quickly and the staff was very helpful. Thank you!',
            rating=5,
            submitted_by=student3,
        )
        self.stdout.write(f'Created feedback for complaint: {resolved_complaint.complaint_number}')

        self.stdout.write(
            self.style.SUCCESS('\nSample data created successfully!')
        )
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('VC: vc / vc123')
        self.stdout.write('Head (CS): head_cs / head123')
        self.stdout.write('Head (Math): head_math / head123')
        self.stdout.write('Staff: staff_cs1 / staff123')
        self.stdout.write('Students: student1, student2, student3 / student123')

