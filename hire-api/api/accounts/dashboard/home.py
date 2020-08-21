from .models import User




def home(request):
    user_count = User.objects.count()
    # employee_count = Employee.objects.count()
    return render(request,'index.html',{
        'user_count' : user_count,
        'employee_count' : employee_count,
    })