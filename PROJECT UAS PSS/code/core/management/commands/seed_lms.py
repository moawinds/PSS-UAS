import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Course, CourseContent, Comment, CourseMember

class Command(BaseCommand):
    help = 'Seed database with updated sample LMS data (Bengkel Koding Style)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # 1. Create Users
        admin, _ = User.objects.get_or_create(username='admin', is_staff=True, is_superuser=True)
        admin.set_password('admin123')
        admin.save()
        
        t1, _ = User.objects.get_or_create(username='pak_budi', first_name='Budi', last_name='Susanto')
        t2, _ = User.objects.get_or_create(username='bu_siti', first_name='Siti', last_name='Aminah')
        
        teachers = [t1, t2]
        
        students = []
        for i in range(10):
            s, _ = User.objects.get_or_create(username=f'mhs_{i+1}', first_name=f'Mahasiswa', last_name=f'{i+1}')
            students.append(s)

        # 2. Create Courses
        courses = []
        course_names = ["Django Fundamental", "Python for Data Science", "Web Development with React"]
        for name in course_names:
            course, _ = Course.objects.get_or_create(
                name=name,
                description=f'Belajar {name} secara mendalam dan praktis.',
                price=random.randint(150000, 750000),
                teacher=random.choice(teachers)
            )
            courses.append(course)

        # 3. Create Course Members
        for s in students:
            enrolled_courses = random.sample(courses, 2)
            for c in enrolled_courses:
                CourseMember.objects.get_or_create(course_id=c, user_id=s, roles='std')

        # 4. Create Course Contents & Sub Contents & Comments
        for course in courses:
            for i in range(3):
                video_url = f'/static/videos/materi{i+1}.mp4'
                content, _ = CourseContent.objects.get_or_create(
                    course_id=course,
                    name=f'Materi {i+1}: Pengenalan {course.name}',
                    description=f'Ini adalah penjelasan materi {i+1}',
                    defaults={'video_url': video_url}
                )
                if not content.video_url:
                    content.video_url = video_url
                    content.save()
                # Add a sub-content
                sub, _ = CourseContent.objects.get_or_create(
                    course_id=course,
                    name=f'Sub-materi {i+1}.1: Detail Teknis',
                    description='Detail teknis materi.',
                    parent_id=content
                )
                
                # Add some comments
                # Get members of this course
                members = CourseMember.objects.filter(course_id=course)
                for j in range(2):
                    if members:
                        Comment.objects.get_or_create(
                            content_id=content,
                            member_id=random.choice(members),
                            comment=f'Wah materinya keren banget! (Komentar ke-{j+1})'
                        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded updated LMS data'))
