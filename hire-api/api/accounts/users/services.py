from .models import User,UserPermissions,Permissions,Actions,UserRole

class UserServices:

    def get_queryset(self,filter_data):
        return User.objects.filter(**filter_data)

    def get_user_dropdown_queryset(self,filter_data):
        return User.objects.filter(**filter_data).distinct()
            
    def get_user(self,id):
        return User.objects.get(id = id)
        

    def update_user(self,id):
        return User.objects.get(id = id)
    

    def update_pass(self,id):
        return User.objects.get(id=id)
        
    def email_service(self,email):
        return User.objects.get(email=email,is_active=True)
    
    def dashboard_service(self,email):
        return User.objects.count()
        


class UserRoleService:
    def get_userall(self):
        return UserRole.objects.all()

    def get_userpermission_service(self,id):
        return UserRole.objects.get(id = id)




###########################################################################


class userpermissions_service:
    """docstring for ClassName"""
    def get_queryset(self):
        return UserPermissions.objects.all()

    def get_userpermission_service(self,id):
        return UserPermissions.objects.get(id = id)

class permission_service:
    """docstring for permission_service"""
    def get_queryset(self):
        return Permissions.objects.all()




class action_service:
    """docstring for ClassName"""
    def get_queryset(self):
        return Actions.objects.all()    