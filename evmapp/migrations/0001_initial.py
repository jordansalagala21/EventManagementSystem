# Generated by Django 4.2.6 on 2024-02-17 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('purpose', models.CharField(max_length=200)),
                ('contact', models.CharField(max_length=100)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=200)),
                ('organiser', models.CharField(max_length=100)),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('venue', models.CharField(max_length=200)),
                ('theme', models.CharField(max_length=200)),
                ('total_tickets', models.IntegerField()),
                ('price_per_ticket', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.BooleanField(default=True)),
                ('vendors', models.ManyToManyField(to='evmapp.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_tickets', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('contact_number', models.CharField(max_length=15)),
                ('flat_number', models.CharField(max_length=50)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ticket_id', models.CharField(default=0, max_length=20, unique=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evmapp.event')),
            ],
        ),
    ]
