import os
import sys

# Menyesuaikan path agar bisa mengimport settings (Sesuai Gambar)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), *[os.pardir] * 0))) 
os.environ['DJANGO_SETTINGS_MODULE'] = 'simplelms.settings'

import django
django.setup()

import csv
from django.contrib.auth.models import User
from core.models import Course, CourseMember

# 1. Import User
print("Importing Users...")
with open('./csv_data/user-data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num, row in enumerate(reader):
        if not User.objects.filter(username=row['username']).exists():
            User.objects.create_user(
                id=num+2, # +2 agar tidak bentrok dengan admin
                username=row['username'],
                password=row['password'],
                email=row['email']
            )

# 2. Import Course
print("Importing Courses...")
with open('./csv_data/course-data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num, row in enumerate(reader):
        if not Course.objects.filter(pk=num+1).exists():
            Course.objects.create(
                id=num+1,
                name=row['name'],
                description=row['description'],
                price=row['price'],
                teacher=User.objects.get(pk=int(row['teacher']))
            )

# 3. Import Member
print("Importing Members...")
with open('./csv_data/member-data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num, row in enumerate(reader):
        if not CourseMember.objects.filter(pk=num+1).exists():
            CourseMember.objects.create(
                id=num+1,
                course_id=Course.objects.get(pk=int(row['course_id'])),
                user_id=User.objects.get(pk=int(row['user_id'])),
                roles=row['roles']
            )

print("Berhasil mengimport data dari CSV!")
