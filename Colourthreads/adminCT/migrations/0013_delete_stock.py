# Generated by Django 3.2.9 on 2021-11-18 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminCT', '0012_rename_stocks_stock'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Stock',
        ),
    ]
