# Generated by Django 4.1.2 on 2022-10-21 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ads", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ad",
            name="author",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="users.user"
            ),
        ),
        migrations.AddField(
            model_name="ad",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="ads.category",
            ),
        ),
    ]
