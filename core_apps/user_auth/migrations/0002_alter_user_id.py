# Generated by Django 5.2 on 2025-04-28 18:12

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_auth", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("13a2541c-e942-4eab-945a-07656bd45d28"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
