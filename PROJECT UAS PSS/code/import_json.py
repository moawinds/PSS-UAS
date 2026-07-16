import os
import sys
import json
from random import randint

# Menyesuaikan path agar bisa mengimport settings
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), *[os.pardir] * 0))) 
os.environ['DJANGO_SETTINGS_MODULE'] = 'simplelms.settings'

import django
django.setup()

from django.contrib.auth.models import User
from core.models import Course, CourseContent, Comment

filepath = './csv_data/'

# 1. Bulk Create Contents
print("Bulk Creating Contents from JSON...")
with open(filepath + 'contents.json') as jsonfile:
    contents = json.load(jsonfile)
    obj_create = []
    for num, row in enumerate(contents):
        if not CourseContent.objects.filter(pk=num+1).exists():
            obj_create.append(CourseContent(
                course_id=Course.objects.get(pk=int(row['course_id'])),
                video_url=row['video_url'],
                name=row['name'],
                description=row['description'],
                id=num+1
            ))
    CourseContent.objects.bulk_create(obj_create)

# 2. Bulk Create Comments
print("Bulk Creating Comments from JSON...")
with open(filepath + 'comments.json') as jsonfile:
    comments = json.load(jsonfile)
    obj_create = []
    for num, row in enumerate(comments):
        # Logika randint dari panduan dosen
        if int(row['user_id']) > 50:
            row['user_id'] = randint(5, 40)
            
        if not Comment.objects.filter(pk=num+1).exists():
            obj_create.append(Comment(
                content_id=CourseContent.objects.get(pk=int(row['content_id'])),
                user_id=User.objects.get(pk=int(row['user_id'])),
                id=num+1,
                comment=row['comment']
            ))
    Comment.objects.bulk_create(obj_create)

print("Berhasil melakukan Bulk Create data dari JSON!")
