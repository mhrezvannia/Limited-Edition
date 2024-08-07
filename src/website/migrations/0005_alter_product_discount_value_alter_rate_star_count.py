# Generated by Django 4.2 on 2024-08-07 18:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='star_count',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
