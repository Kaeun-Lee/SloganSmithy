# Generated by Django 3.2.5 on 2021-08-16 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('select', models.CharField(max_length=100, null=True)),
                ('info', models.TextField(null=True)),
                ('sim', models.IntegerField(null=True)),
                ('result', models.TextField(null=True)),
            ],
        ),
    ]
