from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from job_tracker.models import JobApplication

class Command(BaseCommand):
    help = 'Creates 5 example job applications for anonymous users'

    def handle(self, *args, **options):
        # Create a dedicated user for example jobs if it doesn't exist
        user, created = User.objects.get_or_create(
            username='example_user',
            defaults={'first_name': 'Example', 'last_name': 'User', 'is_staff': False}
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created example user'))

        # Create 5 example job applications
        JobApplication.objects.get_or_create(
            user=user,
            job_title='Senior Python Developer',
            company_name='TechCorp',
            original_job_description='Seeking an experienced Python developer to work on our flagship data analysis platform.',
            status='Applied',
            is_example=True,
            date_applied='2025-07-10'
        )

        JobApplication.objects.get_or_create(
            user=user,
            job_title='Frontend Engineer (React)',
            company_name='Innovate Inc.',
            original_job_description='Join our dynamic frontend team to build beautiful and responsive user interfaces with React and TypeScript.',
            status='Interviewing',
            is_example=True,
            date_applied='2025-07-11'
        )

        JobApplication.objects.get_or_create(
            user=user,
            job_title='UX/UI Designer',
            company_name='Creative Solutions',
            original_job_description='We are looking for a talented designer to create intuitive and engaging user experiences for our mobile applications.',
            status='Applied',
            is_example=True,
            date_applied='2025-07-12'
        )

        JobApplication.objects.get_or_create(
            user=user,
            job_title='DevOps Engineer',
            company_name='CloudNet',
            original_job_description='Help us build and maintain our cloud infrastructure using AWS, Docker, and Kubernetes.',
            status='Offer',
            is_example=True,
            date_applied='2025-07-13'
        )

        JobApplication.objects.get_or_create(
            user=user,
            job_title='Product Manager',
            company_name='Visionary Products',
            original_job_description='Lead the development of our next-generation products from conception to launch.',
            status='Rejected',
            is_example=True,
            date_applied='2025-07-14'
        )

        self.stdout.write(self.style.SUCCESS('Successfully created 5 example job applications'))
