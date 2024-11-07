from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation, Message
from apps.profiles.models import Profile
from apps.profiles.serializers import ProfilesSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from django.db.models import Count

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_conversations(request):
    current_user = request.user.profile
    conversations = Conversation.objects.filter(participants=current_user).annotate(message_count=Count('messages')).filter(message_count__gt=0)
    
    data = {
        'conversations': [
            {
                'id': convo.id,
                'name': convo.get_other_participant_name(current_user),
                'other_user_id': convo.get_other_participant_id(current_user),
                'profile_pic': convo.get_other_participant_photo(current_user),
                'last_message': convo.get_last_message().content if convo.get_last_message() else "No messages",
                'last_message_time': convo.get_last_message().timestamp,
                'last_sender_id': convo.get_last_message().sender.id if convo.get_last_message() and convo.get_last_message().sender else "Unknown",
                'last_sender_name': f"{convo.get_last_message().sender.user.first_name} {convo.get_last_message().sender.user.last_name}" if convo.get_last_message() and convo.get_last_message().sender and convo.get_last_message().sender.user else "Unknown Sender",
                'is_read': convo.is_read(current_user)
            }
            for convo in conversations
        ]
    }
    return JsonResponse(data)

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def start_conversation(request, user_id):
    current_user = request.user.profile
    other_user = get_object_or_404(Profile, user__id=user_id)

    conversations = Conversation.objects.filter(participants=current_user).filter(participants=other_user)

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.participants.add(current_user, other_user)

    return JsonResponse({
        'conversation_id': conversation.id,
        'name': f"{other_user.user.first_name} {other_user.user.last_name}"
    })

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_conversation_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.order_by('timestamp')
    messages_data = [
        {
            'id': message.id,
            'sender_id': message.sender.id,
            'sender_name': f"{message.sender.user.first_name} {message.sender.user.last_name}",
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
            'read': message.read
        }
        for message in messages
    ]
    return JsonResponse({'conversation_id': conversation.id, 'messages': messages_data})

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_message(request):
    current_user = request.user.profile
    conversation_id = request.data.get('conversation_id')
    content = request.data.get('content')

    conversation = get_object_or_404(Conversation, id=conversation_id)
    message = Message.objects.create(conversation=conversation, sender=current_user, content=content)

    return JsonResponse({'status': 'success', 'message_id': message.id})

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_messages_as_read(request, conversation_id):
    current_user = request.user.profile
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if current_user not in conversation.participants.all():
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    messages_to_update = Message.objects.filter(
        conversation=conversation,
        read=False
    ).exclude(sender=current_user)

    messages_to_update.update(read=True)

    return JsonResponse({'status': 'success'})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_unread_messages(request):
    current_user = request.user.profile

    unread_messages = Message.objects.filter(
        conversation__participants=current_user,
        read=False
    ).exclude(sender=current_user)

    unread_message_count = unread_messages.count()

    return JsonResponse({'unread_message_count': unread_message_count})
