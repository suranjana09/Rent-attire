# Generated by Django 3.2 on 2021-06-16 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_product_materialandcare'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='rent_duration',
            field=models.CharField(default='4 days', max_length=50),
        ),
    ]
