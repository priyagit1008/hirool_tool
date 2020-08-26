from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import permissions
from .models import UserPermissions,Actions,Permissions
from django.contrib.contenttypes.models import ContentType
# from rest_framework.decorators import action



class HiroolReadOnly(permissions.BasePermission):

	def has_permission(self, request, view):
		if (request.method in permissions.SAFE_METHODS):
			# print(view.action)
			action_obj = Actions.objects.get(action_name = view.action)
			# print(action_obj.id)
			# print(request.user.id)
			# permission_obj = Permissions.objects.get(permissions = permission)
			if UserPermissions.objects.filter(user=request.user.id,actions=action_obj.id).exists():
				# print(data)
				print("user request ssuccessfull")
				return True
			else:
				print("user request not successfull")
				return False
		return False

class HiroolReadWrite(permissions.BasePermission):

	def has_permission (self, request, view):
		print(self)
		print(view.action)
		action_obj =Actions.objects.get(action_name=view.action)
		print(action_obj.id)
		print(request.user.id)
		if UserPermissions.objects.filter(user=request.user.id,actions=action_obj.id).exists():
			print("user request ssuccessfull")
			return True
		else:
			print("user request not successfull")
			return False


# permission_id=Permissions.objects.all()id)
  # permission_id=Permissions.objects.get