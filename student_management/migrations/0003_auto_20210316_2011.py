# Generated by Django 3.1.7 on 2021-03-16 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management', '0002_auto_20210315_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='grade',
            field=models.IntegerField(max_length=2),
        ),
        migrations.AlterField(
            model_name='mark',
            name='year',
            field=models.IntegerField(max_length=4),
        ),
    ]
