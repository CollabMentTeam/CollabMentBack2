# Generated by Django 5.0 on 2024-05-10 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protoAuth', '0029_customuser_instagram_customuser_telegram_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='applications_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]