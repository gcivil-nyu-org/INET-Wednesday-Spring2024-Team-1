# Generated by Django 5.0.2 on 2024-04-09 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("groceryStore", "0006_alter_order_calories"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="recipe",
        ),
        migrations.RemoveField(
            model_name="order",
            name="total_price",
        ),
    ]
