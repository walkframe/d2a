# Generated by Django 3.0.3 on 2020-06-06 10:50

import books.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='email',
            field=books.models.CustomEmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.IntegerField(default=100),
        ),
    ]
