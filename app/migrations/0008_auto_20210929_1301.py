# Generated by Django 3.2.3 on 2021-09-29 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210928_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderplaced',
            name='rent_duration',
        ),
        migrations.AddField(
            model_name='cart',
            name='rent_duration',
            field=models.CharField(default='4 days', max_length=6),
        ),
        migrations.DeleteModel(
            name='BlogComment',
        ),
    ]
