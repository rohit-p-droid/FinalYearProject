# Generated by Django 4.2.5 on 2023-11-02 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_ticket_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='city',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='monument',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='ticketCount',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='ticketPrice',
        ),
        migrations.AlterField(
            model_name='monuments',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True),
        ),
    ]