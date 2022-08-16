# Generated by Django 4.0.6 on 2022-08-16 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes_app', '0004_alter_user_managers'),
    ]

    database_operations = [
        migrations.AlterModelTable('Quiz', 'app_quiz')
    ]

    state_operations = [
        migrations.DeleteModel('Quiz')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations
        )
    ]