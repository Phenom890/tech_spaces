# Generated by Django 5.0.4 on 2024-11-06 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_course_question_answer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='user',
            new_name='student',
        ),
    ]
