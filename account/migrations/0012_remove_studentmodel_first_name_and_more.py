# Generated by Django 5.0.1 on 2024-02-09 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_rename_course_category_coursecategory_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentmodel',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='last_name',
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
    ]
