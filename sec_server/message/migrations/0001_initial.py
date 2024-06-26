# Generated by Django 3.2.18 on 2023-05-04 09:01

from django.db import migrations, models
import django.db.models.deletion
import message.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('thread', '0001_initial'),
        ('member', '0003_alter_groupmember_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='message.message')),
                ('recieved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recieved_messages', to='member.groupmember')),
                ('sent_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='member.groupmember')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_set', to='thread.messagethread')),
            ],
        ),
        migrations.CreateModel(
            name='MessageAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=message.models.get_upload_path)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='message.message')),
            ],
        ),
    ]
