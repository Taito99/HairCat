# Generated by Django 5.0.5 on 2024-05-08 18:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_chat_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.AddField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(default='f0f492ef-ed67-4f41-a81c-f5ef73726030', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chat'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='chats', to=settings.AUTH_USER_MODEL),
        ),
    ]
