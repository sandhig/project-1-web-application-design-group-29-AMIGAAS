from django.db import models
from apps.profiles.models import Profile

class Conversation(models.Model):
    participants = models.ManyToManyField(Profile, related_name='conversations')

    def __str__(self):
        return f"Conversation IDs: {self.id}"
    
    def get_other_participant_name(self, current_user):
        other_participants = self.participants.exclude(id=current_user.id)
        if other_participants.exists():
            other_profile = other_participants.first()
            if other_profile.user:
                return f"{other_profile.user.first_name} {other_profile.user.last_name}"
        return 'Unknown'

    def get_last_message(self):
        return self.messages.order_by('-timestamp').first()
    
    def is_read(self, current_user):
        if len(self.messages.exclude(sender_id=current_user.id)) > 0:
            return self.messages.exclude(sender_id=current_user.id).order_by('-timestamp').first().read
        else:
            return True

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        if self.sender and self.sender.user:
            return f"{self.sender.user.first_name}: {self.content}"
        return "Unknown Sender"