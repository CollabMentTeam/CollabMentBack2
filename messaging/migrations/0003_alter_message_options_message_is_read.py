# Generated by Django 5.0 on 2024-02-11 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('timestamp',)},
        ),
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]