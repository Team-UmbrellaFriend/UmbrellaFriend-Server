#users/permissions.py
from rest_framework import permissions

# 프로필의 주인(로그인한 유저)만 수정하도록 권한 허가
class CustomReadOnly(permissions.BasePermission):
    # GET : 누구나 / PUT, PATCH : 해당 유저만
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # 데이터에 영향을 미치지 않는 메서드 (GET)
            return True
        return obj.user == request.user # PUT/PATCH