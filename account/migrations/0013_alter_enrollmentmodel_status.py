# Generated by Django 4.2.2 on 2024-02-12 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_remove_studentmodel_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollmentmodel',
            name='status',
            field=models.CharField(choices=[('enrolled', 'Enrolled'), ('completed', 'COMPLETED'), ('running', 'RUNNING')], max_length=150),
        ),
    ]
