# Generated by Django 4.0.6 on 2022-08-19 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_answer_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question',
            new_name='text',
        ),
    ]
