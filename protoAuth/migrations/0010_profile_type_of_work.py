# Generated by Django 5.0 on 2024-03-01 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protoAuth', '0009_profile_desired_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='type_of_work',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]