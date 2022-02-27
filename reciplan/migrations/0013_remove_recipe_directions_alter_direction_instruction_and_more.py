# Generated by Django 4.0.1 on 2022-02-25 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reciplan', '0012_direction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='directions',
        ),
        migrations.AlterField(
            model_name='direction',
            name='instruction',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='direction',
            name='step',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='amt',
            field=models.FloatField(verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Item'),
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='unit_of_measure',
            field=models.CharField(choices=[('fl_oz', 'fl_oz'), ('fl_cups', 'fl_cups'), ('cups', 'cups'), ('pints', 'pints'), ('quarts', 'quarts'), ('gallons', 'gallons'), ('tsp', 'tsp'), ('Tbsp', 'Tbsp'), ('grams', 'grams'), ('Kg', 'Kg'), ('oz', 'oz'), ('lbs', 'lbs'), ('mL', 'mL'), ('liters', 'liters'), ('ea', 'ea')], max_length=100, verbose_name='Unit of Measure'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='o_yield',
            field=models.IntegerField(verbose_name='Yield (servings)'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='URL Source'),
        ),
    ]