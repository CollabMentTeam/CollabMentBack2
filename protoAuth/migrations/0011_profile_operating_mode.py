# Generated by Django 5.0 on 2024-03-01 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protoAuth', '0010_profile_type_of_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='operating_mode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]