# Generated by Django 5.0.2 on 2024-03-13 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_customuser_last_login"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="last_login",
            field=models.DateTimeField(null=True),
        ),
    ]