# Generated by Django 4.0.1 on 2022-01-23 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reciplan', '0003_alter_recipe_ingredients'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.AddField(
            model_name='recipe',
            name='directions',
            field=models.TextField(default='Directions'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='o_yield',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('amt', models.IntegerField()),
                ('unit_of_measure', models.CharField(max_length=10)),
                ('in_cart', models.BooleanField(default=False)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reciplan.recipe')),
            ],
        ),
    ]
