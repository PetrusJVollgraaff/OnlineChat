# Generated by Django 5.0.1 on 2024-02-07 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatsystem', '0006_oneononechat_delete_usercontactsbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatgroup',
            name='hashtagid',
            field=models.TextField(default='Hello', editable=False, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usermessages',
            name='option',
            field=models.CharField(default='chat', max_length=16),
        ),
        migrations.AlterField(
            model_name='oneononechat',
            name='hashtagid',
            field=models.TextField(editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='usermessages',
            name='message',
            field=models.TextField(),
        ),
    ]
