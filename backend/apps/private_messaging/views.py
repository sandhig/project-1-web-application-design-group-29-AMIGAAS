from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Conversation, Message

# Hardcode login as user 1
def get_current_user():
    return get_object_or_404(User, id=1)

def get_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return JsonResponse({'id': user.id, 'name': user.name})

def get_user_conversations(request):
    current_user = get_current_user()
    conversations = Conversation.objects.filter(participants=current_user)
    data = {
        'conversations': [
            {
                'id': convo.id,
                'name': convo.get_other_participant_name(current_user),
                'last_message': convo.get_last_message(),
                'is_read': convo.is_read(current_user)
            }
            for convo in conversations
        ]
    }
    return JsonResponse(data)

@csrf_exempt
def start_conversation(request, user_id):
    current_user = get_current_user()
    other_user = get_object_or_404(User, id=user_id)

    conversations = Conversation.objects.filter(participants=current_user).filter(participants=other_user)

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.participants.add(current_user, other_user)

    return JsonResponse({
        'conversation_id': conversation.id,
        'name': other_user.name
    })

def get_conversation_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.order_by('timestamp')
    messages_data = []
    for message in messages:
        messages_data.append({
            'id': message.id,
            'sender_id': message.sender.id,
            'sender_name': message.sender.name,
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
            'read': message.read
        })
    return JsonResponse({'conversation_id': conversation.id, 'messages': messages_data})

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        current_user = get_current_user()
        conversation_id = request.POST.get('conversation_id')
        content = request.POST.get('content')
        conversation = get_object_or_404(Conversation, id=conversation_id)
        message = Message.objects.create(conversation=conversation, sender=current_user, content=content)
        return JsonResponse({'status': 'success', 'message_id': message.id})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def mark_messages_as_read(request, conversation_id):
    if request.method == 'POST':
        current_user = get_current_user()
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if current_user not in conversation.participants.all():
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        messages_to_update = Message.objects.filter(
            conversation=conversation,
            read=False
        ).exclude(sender=current_user)

        messages_to_update.update(read=True)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)