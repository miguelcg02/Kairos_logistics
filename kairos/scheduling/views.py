from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def login_page(request):
    if request.method == 'GET':
        return render(request, template_name='login.html')
    
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     user = authenticate(username=username, password=password)

    # if user is not None:
    #     login(request, user)
    #     messages.success(request, f'¡Bienvenido {user.username}, nos encanta tenerte de vuelta!')
    #     return redirect('home')
    # else:
    #     messages.error(request, '¡El usuario y la contraseña no coinciden, por favor vuelva a intentarlo!')
    #     return redirect('login')


    return render(request,template_name="login.html")

def home_manager(request):
    return render(request,template_name="0-manager/home-manager.html")

def home_admin(request):
    return render(request,template_name="1-admin/home-admin.html")

def home_adviser(request):
    return render(request,template_name="2-adviser/home-adviser.html")

def home_operator(request):
    return render(request,template_name="3-operator/home-operator.html")

def block_schedule(request):
    return render(request,template_name="0-1-block_schedule.html")

def create_user(request):
    return render(request,template_name="0-1-create_user.html")

def delete_user(request):
    return render(request,template_name="0-1-delete_user.html")

def reports(request):
    return render(request,template_name="0-reports.html")

def see_schedules(request):
    return render(request,template_name="1-2-3-see_schedules.html")

def asign_turns(request):
    return render(request,template_name="1-2-asign_turns.html")

def modify_schedules(request):
    return render(request,template_name="1-modify_schedules.html")

def validate_service_provided(request):
    return render(request,template_name="1-validate_service_provided.html")
