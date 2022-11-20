# Generated by Django 4.0.6 on 2022-11-04 18:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0008_alter_answer_text_alter_question_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(2, 'The answer has to be at least two characters long')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(2, 'The question has to be at least two characters long')]),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_quizzes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(3, 'The name of the quiz has to be at least three characters long')]),
        ),
    ]