# Generated by Django 3.1.1 on 2020-10-24 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cetus3pur', '0009_eab_request_rw_or_ro'),
    ]

    operations = [
        migrations.AddField(
            model_name='eab_it_action',
            name='id_proxy',
            field=models.CharField(default='todo', max_length=10),
        ),
    ]
