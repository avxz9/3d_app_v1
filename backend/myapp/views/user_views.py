from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User, Group

from ..serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        if not request.user.groups.filter(name="admin").exists():
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if not request.user.groups.filter(name="admin").exists():
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        if not request.user.groups.filter(name="admin").exists():
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user == request.user:
            return Response({"detail": "You cannot delete yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.groups.filter(name="admin").exists():
            return Response({"detail": "You cannot delete another admin."}, status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        if not request.user.groups.filter(name="admin").exists():
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        new_role = request.data.get("role")

        if user == request.user:
            return Response({"detail": "You cannot change your own role."}, status=status.HTTP_400_BAD_REQUEST)

        if user.groups.filter(name="admin").exists() and new_role != "admin":
            return Response({"detail": "You cannot change the role of another admin."}, status=status.HTTP_403_FORBIDDEN)

        user.groups.clear()
        group = Group.objects.get(name=new_role)
        user.groups.add(group)
        user.save()

        return Response({"message": "Role updated successfully."})
