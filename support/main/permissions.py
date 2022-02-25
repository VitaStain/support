from rest_framework import permissions

from .models import Ticket


class IsOwnerOrIsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        ticket = Ticket.objects.get(pk=view.kwargs['pk'])
        if request.user == ticket.user:
            return True

        return bool(request.user and request.user.is_staff)
