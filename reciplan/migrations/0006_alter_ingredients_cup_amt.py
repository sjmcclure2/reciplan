# Generated by Django 4.0.1 on 2022-02-06 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reciplan', '0005_remove_ingredients_in_cart_ingredients_cup_amt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='cup_amt',
            field=models.FloatField(),
        ),
    ]