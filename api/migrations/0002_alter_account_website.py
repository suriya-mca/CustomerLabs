# Generated by Django 5.0.6 on 2024-05-25 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='website',
            field=models.CharField(blank=True, null=True),
        ),
    ]
