# Generated by Django 5.0 on 2024-03-01 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protoAuth', '0011_profile_operating_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name_organization',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]