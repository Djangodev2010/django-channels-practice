from django.db import models
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.TextField(max_length=555)
    is_seen = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username + ', ' + self.notification

    def save(self, *args, **kwargs):

        super(Notification, self).save(*args, **kwargs)
        channel_layer = get_channel_layer()
        notification_objs = Notification.objects.filter(is_seen=False).count()
        data = {
            'count': notification_objs,
            'current_notification': self.notification
        }

        async_to_sync(channel_layer.group_send)(
            'test_consumer_group', {
                'type': 'send_notification',
                'value': json.dumps(data)
            }
        )
