# Generated by Django 3.1.7 on 2021-03-02 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_auto_20210302_0410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
