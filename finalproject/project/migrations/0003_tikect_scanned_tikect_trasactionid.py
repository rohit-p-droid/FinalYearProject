# Generated by Django 4.2.5 on 2023-12-01 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_tikect'),
    ]

    operations = [
        migrations.AddField(
            model_name='tikect',
            name='scanned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tikect',
            name='trasactionId',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
