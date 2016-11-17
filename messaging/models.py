from registration.models import *
from datetime import datetime


class MessageManager(models.Manager):
    def createMessage(self, sender, recipient, subject, content):
        message = self.create(sender=sender, recipient=recipient, subject=subject, content=content)
        return message


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', default=None)
    recipient = models.ForeignKey(User, related_name='recipient', default=None)
    subject = models.CharField('Subject', max_length=100)
    content = models.CharField('Content', max_length=1000)

    pubdate = models.DateTimeField('Created', default=datetime.now)
    count = models.IntegerField('Count', default=1)
    read = models.BooleanField('Read', default=False)
    link = models.CharField('Link', max_length=100)

    sender_hidden = models.BooleanField('sender_hidden', default=False)
    recipient_hidden = models.BooleanField('recipient_hidden', default=False)

    objects = MessageManager()

    def __str__(self):
        return 'Subject: ' + self.subject