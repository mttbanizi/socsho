# Generated by Django 4.0.2 on 2022-04-02 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('single_message', '0002_alter_payam_user_alter_room_user_dualpayam'),
    ]

    operations = [
        migrations.AddField(
            model_name='dualpayam',
            name='roomname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
