# Generated by Django 4.0.1 on 2022-02-21 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reciplan', '0008_ingredients_cup_amt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='amt',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='unit_of_measure',
            field=models.CharField(choices=[('fl_oz', 'fl_oz'), ('fl_cups', 'fl_cups'), ('cups', 'cups'), ('pints', 'pints'), ('quarts', 'quarts'), ('gallons', 'gallons'), ('tsp', 'tsp'), ('Tbsp', 'Tbsp'), ('grams', 'grams'), ('Kg', 'Kg'), ('oz', 'oz'), ('lbs', 'lbs'), ('mL', 'mL'), ('liters', 'liters'), ('ea', 'ea')], max_length=100),
        ),
    ]
