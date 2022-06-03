from rest_framework.permissions import BasePermission


class IsIndustry(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_industry


class IsFarmer(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_industry
