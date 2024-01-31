# Generated by Django 3.2.18 on 2023-05-04 01:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Otpdetails',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('link_string', models.CharField(blank=True, max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]