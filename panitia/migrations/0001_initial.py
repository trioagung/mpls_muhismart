# Generated by Django 5.2.4 on 2025-07-11 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kelompok',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100, unique=True)),
                ('ketua', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Anggota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('is_ketua', models.BooleanField(default=False)),
                ('kelompok', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anggota', to='panitia.kelompok')),
            ],
        ),
        migrations.CreateModel(
            name='Absensi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hadir', models.BooleanField(default=False)),
                ('agenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panitia.agenda')),
                ('anggota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panitia.anggota')),
            ],
            options={
                'unique_together': {('anggota', 'agenda')},
            },
        ),
    ]
