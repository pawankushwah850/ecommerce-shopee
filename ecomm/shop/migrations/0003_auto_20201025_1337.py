# Generated by Django 3.1.2 on 2020-10-25 13:37

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20201023_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productDetails',
            field=ckeditor.fields.RichTextField(),
        ),
    ]