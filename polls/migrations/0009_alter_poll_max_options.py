# Generated by Django 4.0.5 on 2022-06-25 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_poll_max_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='max_options',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
