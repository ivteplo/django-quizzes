# Generated by Django 4.0.6 on 2022-12-02 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_type',
        ),
    ]