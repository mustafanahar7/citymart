# Generated by Django 5.0.4 on 2024-09-06 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appone', '0010_rename_bill_amount_websiteorder_bill_mrp_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='websiteorderitems',
            name='product_mrp_price',
            field=models.FloatField(default=0),
        ),
    ]