# Generated by Django 2.0.2 on 2018-02-06 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='bio',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
    ]
