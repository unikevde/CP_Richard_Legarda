# Generated by Django 5.1.4 on 2025-01-16 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='switch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('ip', models.CharField(max_length=15)),
                ('piso', models.CharField(max_length=10)),
                ('agencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Web.agencia')),
            ],
        ),
    ]
