# Generated by Django 4.2.3 on 2023-07-05 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
            ],
        ),
    ]
