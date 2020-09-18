# Generated by Django 3.1.1 on 2020-09-15 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cetus3pur', '0004_eab_approval_eab_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eab_approval',
            name='decision',
            field=models.CharField(choices=[('APP', 'Approved'), ('REJ', 'Rejected'), ('PEN', 'Pending')], max_length=3),
        ),
    ]