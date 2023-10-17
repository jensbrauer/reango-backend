# Generated by Django 4.2.5 on 2023-10-11 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_product_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='user_type',
            field=models.CharField(choices=[('STORE', 'STORE'), ('FEATURED', 'FEATURED'), ('USER', 'USER')], default='USER', max_length=20),
        ),
    ]