# Generated by Django 3.1.7 on 2021-04-05 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_scrape', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='email_body',
            new_name='email_body_html',
        ),
        migrations.AddField(
            model_name='email',
            name='email_body_text',
            field=models.TextField(blank=True, max_length=40960),
        ),
    ]
