# Generated by Django 4.0.5 on 2022-06-25 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_alter_poll_users_voted'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='max_options',
            field=models.IntegerField(default=1),
        ),
    ]