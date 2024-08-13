# Generated by Django 5.0.7 on 2024-08-12 08:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=50)),
                ('email', models.CharField(default='', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='Customer name', max_length=50)),
                ('email', models.CharField(default='', max_length=200)),
                ('address', models.CharField(default='', max_length=50)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.contacts')),
            ],
            options={
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('slug', models.CharField(default='', max_length=50)),
                ('project', models.CharField(default='Project name', max_length=50)),
                ('description', models.CharField(default='Description of requirements, notes, etc...', max_length=500)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.customers')),
            ],
            options={
                'verbose_name_plural': 'Orders',
            },
        ),
    ]
