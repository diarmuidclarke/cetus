# Generated by Django 3.1.1 on 2020-09-08 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cetus3pur', '0002_auto_20200906_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='rrresponsiblemanager',
            name='user_ac',
            field=models.CharField(default='<null>', max_length=10),
        ),
    ]