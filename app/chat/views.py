from rest_framework import viewsets, permissions
from .models import Chat
from .serializers import ChatSerializer

class ChatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chat.objects.all().order_by('-created_at')
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]