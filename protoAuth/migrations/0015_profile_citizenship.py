# Generated by Django 5.0 on 2024-03-02 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protoAuth', '0014_profile_experience_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='citizenship',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
