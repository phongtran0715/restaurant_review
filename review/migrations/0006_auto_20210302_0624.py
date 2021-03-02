# Generated by Django 3.1.7 on 2021-03-02 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0005_auto_20210302_0618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='restaurant_id',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.CharField(max_length=10240),
        ),
    ]
