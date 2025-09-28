from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer, UserUpdateSerializer, UserListSerializer, UserDetailSerializer
from .permissions import IsOwnerOrSuperUser, IsSuperUser


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperUser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        return UserListSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsSuperUser]
        elif self.action in ['list']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrSuperUser()]

        return [permission() for permission in self.permission_classes]

    def get_object(self):
        if self.action in ['update','partial_update'] and not self.request.user.is_super_user:
            return self.request.user
        return super().get_object()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        user = request.user
        partial = request.method == 'PATCH'
        serializer = UserUpdateSerializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
