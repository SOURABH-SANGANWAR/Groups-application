# Generated by Django 3.2.18 on 2023-05-04 01:50

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('permissions', '0001_initial'),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email_id', models.EmailField(blank=True, max_length=254, null=True)),
                ('username', models.CharField(blank=True, max_length=254, null=True)),
                ('is_banned', models.BooleanField(default=False)),
                ('is_pending', models.BooleanField(default=False)),
                ('is_invited', models.BooleanField(default=False)),
                ('profile_picture', models.CharField(blank=True, max_length=254, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_members', to='group.group')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_members', to='permissions.rolepermission')),
            ],
        ),
    ]
