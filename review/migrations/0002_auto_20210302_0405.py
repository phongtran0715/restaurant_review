# Generated by Django 3.1.7 on 2021-03-02 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='category',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.AlterField(
            model_name='review',
            name='country',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.AlterField(
            model_name='review',
            name='state',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.AlterField(
            model_name='review',
            name='timestamp',
            field=models.DateField(auto_now_add=True),
        ),
    ]
