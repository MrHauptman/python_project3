# Generated by Django 4.0.4 on 2022-06-16 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furniture', '0003_admincreatevote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chargrade', models.CharField(max_length=1000)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]