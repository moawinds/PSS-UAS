# Generated manually to re-add price and teacher fields to Course model

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_course_price_remove_course_teacher'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.IntegerField(
                default=10000,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name='harga',
            ),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.RESTRICT,
                to=settings.AUTH_USER_MODEL,
                verbose_name='pengajar',
            ),
        ),
    ]
