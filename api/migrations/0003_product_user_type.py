# Generated by Django 4.2.5 on 2023-10-11 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user_type',
            field=models.IntegerField(choices=[(0, 'STORE'), (1, 'FEATURED'), (2, 'USER')], default=2),
        ),
    ]
