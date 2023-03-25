from django.shortcuts import render
from .models import *
from .forms import CreateUserForm
from django.contrib import messages
from django.views.generic.base import TemplateView
from openpyxl import Workbook #Library for generating an excel doc
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

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
    form = CreateUserForm()
    if request.method == "POST":
        if form.is_valid():
            rol = request.POST.get('rol') #Revisar que el name sea rol
            form.save()
            Actual_user = User.objects.get(username= request.POST["username"])
            newProfile = Profile(user = Actual_user, rol=rol)
            newProfile.save()
            messages.success(request, '¡El usuario fue creado exitosamente!')
            return render(request,template_name="0-1-create_user.html")
        else:
            messages.error(request, 'Error al crear el usuario, por favor verique la información')
            return render(request,template_name="0-1-create_user.html", context={'form': form})

    return render(request,template_name="0-1-create_user.html", context={'form': form})

def delete_user(request):
    return render(request,template_name="0-1-delete_user.html")

def createReport(request):
    query = Turn.objects.all()
    workBook = Workbook()
    workSheet = workBook.active
    workSheet.title = 'Hoja1' #Change name of first sheet

    
    #Title of the doc
    workSheet['A2'] = 'REPORTE MONTAJE Y BALANCEO'
    workSheet['A2'].font = Font(name='Arial', size=12, bold=True, color='F79646')
    workSheet['A2'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet.merge_cells('A2:E2')

    #Create first row of the table with the data
    workSheet['B4'] = 'Nombre'
    workSheet['B4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['B4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['B4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['C4'] = 'Llantas'
    workSheet['C4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['C4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['C4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['D4'] = 'Realizado'
    workSheet['D4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['D4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['D4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['E4'] = 'Duración'
    workSheet['E4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['E4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['E4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    rowController = 5 #to keep track of the row we will write on
    for q in query:
        #Fill in the data of the table
        workSheet.cell(row=rowController, column=2).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=2).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=2).value = q.nameCustomer

        workSheet.cell(row=rowController, column=3).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=3).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=3).value = q.quantity

        workSheet.cell(row=rowController, column=4).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=4).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=4).value = q.done

        workSheet.cell(row=rowController, column=5).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=5).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=5).value = q.duration

        rowController += 1

    name = "Reporte.xlsx"
    response = HttpResponse(content_type="application/ms-excel")
    content = "attachment; filename = {0}".format(name)
    response["Content-Disposition"] = content
    workBook.save(response)
    return response
    

def reports(request):
    #createReport(request)
    return render(request,template_name="0-reports.html")

def see_schedules(request):
    return render(request,template_name="1-2-3-see_schedules.html")

def asign_turns(request):
    return render(request,template_name="1-2-asign_turns.html")

def modify_schedules(request):
    return render(request,template_name="1-modify_schedules.html")

def validate_service_provided(request):
    return render(request,template_name="1-validate_service_provided.html")
