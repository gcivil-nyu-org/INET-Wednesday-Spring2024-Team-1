# Generated by Django 5.0.2 on 2024-03-26 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("groceryStore", "0003_ingredient"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Ingredient",
        ),
    ]