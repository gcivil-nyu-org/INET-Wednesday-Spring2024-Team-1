# Generated by Django 5.0.2 on 2024-03-26 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_alter_customuser_last_login"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="credentials",
            field=models.TextField(blank=True, null=True),
        ),
    ]