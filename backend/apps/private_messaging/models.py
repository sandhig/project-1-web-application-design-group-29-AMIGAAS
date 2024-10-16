from django.db import models

# Mock user model for now
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')

    def __str__(self):
        return f"Conversation with {', '.join([user.name for user in self.participants.all()])}"
    
    def get_other_participant_name(self, current_user):
        other_participants = self.participants.exclude(id=current_user.id)
        if other_participants.exists():
            return other_participants.first().name
        return 'Unknown'

    def get_last_message(self):
        return self.messages.order_by('-timestamp').first().content
    
    def is_read(self, current_user):
        if len(self.messages.exclude(sender_id=current_user.id)) > 0:
            return self.messages.exclude(sender_id=current_user.id).order_by('-timestamp').first().read
        else:
            return True

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.name}: {self.content}"
