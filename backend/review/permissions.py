from rest_framework.permissions import BasePermission


class IsCommentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsReviewOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
