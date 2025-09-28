from rest_framework import viewsets,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer,EventListSerializer,EventDetailSerializers
from users.permissions import IsOwnerReadOnly


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related('created_by','store').all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action == 'retreive':
            return EventDetailSerializers
        return EventSerializer

    def get_permissions(self):
        """
        Instantiates and return the list of permissions that  this view requires

        """
        if self.action in ['update','partial_update','destroy']:
            permission_classes = [permissions.IsAuthenticated,IsOwnerReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes ]

    @action(detail=False,methods=['get'])
    def my_event(self,request):
        """
            Get event created by user
        """

        events = self.queryset.filter(created_by=request.user)
        serializer = EventListSerializer(events,many=True)
        return Response(serializer.data)

    @action(detail=False,methods=['get'])
    def by_type(self,request):
        """
        Filter event by type
        """
        event_type = request.query_params.get('type')
        if event_type not in ['account_management','store_acquisition']:
            return Response({'error':'Invalid event type'},status=400)

        events = self.queryset.filter(event_type = event_type)
        serializer = EventListSerializer(events,Many=True)
        return Response(serializer.data)

