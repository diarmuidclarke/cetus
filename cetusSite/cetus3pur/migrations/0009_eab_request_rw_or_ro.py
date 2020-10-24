# Generated by Django 3.1.1 on 2020-10-24 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cetus3pur', '0008_auto_20201024_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='eab_request',
            name='rw_or_ro',
            field=models.CharField(choices=[('RW', 'Read/Write'), ('RO', 'Read Only')], default='RO', max_length=2, verbose_name='Write Permissions'),
        ),
    ]
