# Generated by Django 3.2.12 on 2024-03-22 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('rate', models.FloatField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]