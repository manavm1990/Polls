# Generated by Django 4.0.10 on 2023-04-01 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("questions", "0003_alter_question_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="choice",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="choices",
                to="questions.question",
            ),
        ),
    ]
