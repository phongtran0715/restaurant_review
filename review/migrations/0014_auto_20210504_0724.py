# Generated by Django 3.1.7 on 2021-05-04 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0013_auto_20210504_0600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapereviewstatus',
            name='scrape_url',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
    ]
