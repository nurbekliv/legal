# Generated by Django 5.1.1 on 2024-09-09 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0003_alter_lesson_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
