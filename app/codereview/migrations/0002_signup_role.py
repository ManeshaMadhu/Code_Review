# Generated by Django 5.1.1 on 2025-04-12 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codereview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='role',
            field=models.CharField(blank=True, choices=[("I'm a Student", 'Student'), ("I'm a Teacher", 'Teacher'), ("I'm a Proffesional", 'Proffesional')], max_length=255, null=True),
        ),
    ]
