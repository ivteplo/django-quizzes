# Generated by Django 4.0.6 on 2022-11-23 16:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(3, 'The name of the quiz has to be at least three characters long')])),
                ('description', models.CharField(max_length=500, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_quizzes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quizzes',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(2, 'The question has to be at least two characters long')])),
                ('question_type', models.IntegerField(choices=[(0, 'Multiple choice question'), (1, 'Question with text input')])),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='app.quiz')),
            ],
            options={
                'db_table': 'quiz_questions',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(2, 'The answer has to be at least two characters long')])),
                ('is_right', models.BooleanField(default=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='app.question')),
            ],
            options={
                'db_table': 'quiz_question_answers',
            },
        ),
    ]
