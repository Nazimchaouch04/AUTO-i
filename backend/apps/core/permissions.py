from rest_framework.permissions import BasePermission


class IsPlanPro(BasePermission):
    message = "Cette fonctionnalité est réservée au plan Pro."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            return request.user.subscription.plan.name in ('pro', 'business')
        except Exception:
            return False


class IsPlanBusiness(BasePermission):
    message = "Cette fonctionnalité est réservée au plan Business."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            return request.user.subscription.plan.name == 'business'
        except Exception:
            return False
