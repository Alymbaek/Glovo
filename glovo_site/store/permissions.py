from rest_framework import permissions


class CheckCourier(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'courier':
            return False
        return True


class CheckReview(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.client.role == 'client'


class CheckOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'ownerUser'


class CheckOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.courier.role == 'courier'

class StoreOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class Couriercheck(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user_courier:
            return True
        return False

class CourierOwn(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user == 'courier':
            return True
        return False


