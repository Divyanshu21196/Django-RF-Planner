from rest_framework import permissions, viewsets
from .models import Store
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import StoreSerializer, StoreListSerializer, StoreDetailSerializer
from users.permissions import IsOwnerReadOnly

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return StoreListSerializer
        elif self.action == 'retrieve':
            return StoreDetailSerializer
        return StoreSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes =  [permissions.IsAuthenticated,IsOwnerReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_stores(self, request):
        user = request.user
        stores = Store.objects.filter(created_by=user)
        page = self.paginate_queryset(stores)
        if page is not None:
            serializer = StoreListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StoreListSerializer(stores, many=True)
        return Response(serializer.data)