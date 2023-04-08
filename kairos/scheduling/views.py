from django.shortcuts import render
from .models import *
from .forms import CreateUserForm
from django.contrib import messages
from django.views.generic.base import TemplateView
from openpyxl import Workbook #Library for generating an excel doc
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

from datetime import date,time,timedelta 

# Create your views here.
from django.http import HttpResponse

#---------------get the role--------------#
def getRole(request):
    actualProfile=Profile.objects.get(user=request.user)
    return actualProfile.rol
#---------------get the role--------------#
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
    workSheet['B4'] = 'Fecha del servicio'
    workSheet['B4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['B4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['B4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['C4'] = 'Hora del servicio'
    workSheet['C4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['C4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['C4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['D4'] = 'CVS'
    workSheet['D4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['D4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['D4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['E4'] = 'Número de factura'
    workSheet['E4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['E4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['E4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['F4'] = 'Cédula del cliente'
    workSheet['F4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['F4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['F4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['G4'] = 'Nombre del cliente'
    workSheet['G4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['G4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['G4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['H4'] = 'Teléfono del cliente'
    workSheet['H4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['H4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['H4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['I4'] = 'Servicio prestado'
    workSheet['I4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['I4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['I4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['J4'] = 'Comentarios del servicio'
    workSheet['J4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['J4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['J4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['K4'] = 'Tipo de llanta'
    workSheet['K4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['K4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['K4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['L4'] = 'Cantidad de llantas'
    workSheet['L4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['L4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['L4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['M4'] = '¿Hubo rotación?'
    workSheet['M4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['M4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['M4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['N4'] = 'Cantidad de llantas rotadas'
    workSheet['N4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['N4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['N4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['O4'] = 'Duración del servicio'
    workSheet['O4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['O4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['O4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['P4'] = 'Agendado por'
    workSheet['P4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['P4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['P4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['Q4'] = 'Fecha agendamiento'
    workSheet['Q4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['Q4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['Q4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))
    
    workSheet['R4'] = 'Modificado por'
    workSheet['R4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['R4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['R4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    workSheet['S4'] = 'Fecha de modificación'
    workSheet['S4'].font = Font(name='Arial', size=10, bold=True)
    workSheet['S4'].alignment = Alignment(horizontal="center", vertical="center")
    workSheet['S4'].border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    rowController = 5 #to keep track of the row we will write on
    for q in query:
        #Fill in the data of the table
        workSheet.cell(row=rowController, column=2).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=2).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=2).value = q.date.isoformat()

        workSheet.cell(row=rowController, column=3).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=3).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=3).value = q.hour.isoformat('minutes')

        workSheet.cell(row=rowController, column=4).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=4).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=4).value = q.cvs.name

        workSheet.cell(row=rowController, column=5).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=5).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=5).value = q.bill

        workSheet.cell(row=rowController, column=6).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=6).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=6).value = q.idCustomer

        workSheet.cell(row=rowController, column=7).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=7).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=7).value = q.nameCustomer

        workSheet.cell(row=rowController, column=8).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=8).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=8).value = q.telCustomer

        workSheet.cell(row=rowController, column=9).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=9).font = Font(name='Arial', size=10)
        if(q.done is True):
            workSheet.cell(row=rowController, column=9).value = "Si"
        else:
            workSheet.cell(row=rowController, column=9).value = "No"
        

        workSheet.cell(row=rowController, column=10).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=10).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=10).value = q.comment

        workSheet.cell(row=rowController, column=11).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=11).font = Font(name='Arial', size=10)
        if(q.typeTire == 1):
            workSheet.cell(row=rowController, column=11).value = "Carro"
        elif(q.typeTire == 2):
            workSheet.cell(row=rowController, column=11).value = "Camión"
        elif(q.typeTire == 3):
            workSheet.cell(row=rowController, column=11).value = "Moto"

        workSheet.cell(row=rowController, column=12).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=12).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=12).value = q.quantity

        workSheet.cell(row=rowController, column=13).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=13).font = Font(name='Arial', size=10)
        if(q.rotation is True):
            workSheet.cell(row=rowController, column=13).value = "Si"
        else:
            workSheet.cell(row=rowController, column=13).value = "No"

        workSheet.cell(row=rowController, column=14).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=14).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=14).value = q.quantityRotate

        workSheet.cell(row=rowController, column=15).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=15).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=15).value = str(q.duration) + " min."

        workSheet.cell(row=rowController, column=16).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=16).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=16).value = q.scheduledBy.user.username

        workSheet.cell(row=rowController, column=17).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=17).font = Font(name='Arial', size=10)
        workSheet.cell(row=rowController, column=17).value = str(q.dateScheduled.date().isoformat()) + ", " + str(q.dateScheduled.time().isoformat('minutes'))

        workSheet.cell(row=rowController, column=18).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=18).font = Font(name='Arial', size=10)
        if(q.modifiedBy is None):
            workSheet.cell(row=rowController, column=18).value = ""
        else:
            workSheet.cell(row=rowController, column=18).value = q.modifiedBy.user.username

        workSheet.cell(row=rowController, column=19).alignment = Alignment(horizontal="center", vertical="center")
        workSheet.cell(row=rowController, column=19).font = Font(name='Arial', size=10)
        if(q.dateModified is None):
            workSheet.cell(row=rowController, column=19).value = ""
        else:
            workSheet.cell(row=rowController, column=19).value = str(q.dateModified.date().isoformat()) + ", " + str(q.dateModified.time().isoformat('minutes'))

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

#---------- auxiliar methods for see_schedules-------------------#
def delta2time(delta):
    noon=timedelta(hours=12)
    flagNoon=True
    if(delta>=noon):
        delta-=noon
        flagNoon=False

    hours=delta.seconds//3600
    minutes=delta.seconds//60-60*(delta.seconds//3600)

    if(hours==0):
        hours=12

    if(minutes/10>0):
        hour=str(hours)+':'+str(minutes)
    else:
        hour=str(hours)+':0'+str(minutes)

    if(flagNoon):
        hour+=" am"
    else:
        hour+=" pm"

    return hour

def deltas2line(delta1,delta2):
    li=(delta1.seconds-27000)//60+61
    ls=(delta2.seconds-27000)//60+61
    return(str(li)+"/"+str(ls))

def debugEvent(isFree,delta1,delta2):
    if(isFree):
        print("está libre de "+delta2time(delta1)+" a "+delta2time(delta2))
    else:
        print("está en servicio de "+delta2time(delta1)+" a "+delta2time(delta2))

def fillFree(li,ls,list):
    flagLn=True
    while(li<ls):
        secs=3600-li.seconds%3600

        if(secs==0):
            secs=3600

        if(secs==3600 and (ls-li).seconds < 3600 ):
            secs=(ls-li).seconds

        if(li.seconds+secs>ls.seconds):
            secs=(ls-li).seconds

        increment=timedelta(seconds=secs)

        debugEvent(True,li,li+increment)

        if(flagLn):
            newSC_event=["sc-event free",deltas2line(li,li+increment)]
            flagLn=False
        else:
            newSC_event=["sc-event free ln",deltas2line(li,li+increment)]

        list.append(newSC_event)

        li+=increment

def processData(event):
    info=[]
    #we get date
    months=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    days=["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"]
    date = event['date']

    strDate=days[date.weekday()]+", "+str(date.day)+" de "+months[date.month-1]+", "+str(date.year)
    info.append(strDate)
    #we get cvs
    cvs=CVS.objects.get(id=event['cvs_id'])
    info.append(cvs.name)
    #we get hour
    hour=event['hour']
    info.append(delta2time(timedelta(hours=hour.hour,minutes=hour.minute)))
    #we get duration
    duration=str(event['duration'])+" minutos"
    info.append(duration)
    #we get typeTire
    typeTire=event['typeTire']
    if(typeTire==1):
        typeTire="Automóvil"
    elif(typeTire==2):
        typeTire="Camioneta"
    elif(typeTire==3):
        typeTire="Camión"
    info.append(typeTire)
    #we get quantity
    quantity=str(event['quantity'])+" llantas"
    info.append(quantity)
    #we get rotation
    rotation=event['rotation']
    if(rotation):
        rotation="Sí"
    else:
        rotation="No"
    info.append(rotation)
    #we get quantityRotate
    quantityRotate=str(event['quantityRotate'])+" llantas"
    info.append(quantityRotate)
    #we get bill
    bill=str(event['bill'])
    info.append(bill)
    #we get idCustomer
    idCustomer=str(event['idCustomer'])
    info.append(idCustomer)
    #we get nameCustomer
    info.append(event['nameCustomer'])
    #we get telCustomer
    info.append(event['telCustomer'])
    #we get scheduledBy
    scheduledBy=Profile.objects.get(id=event['scheduledBy_id'])
    scheduledBy=scheduledBy.user.username
    info.append(scheduledBy)
    #we get dateScheduled
    dateScheduled=event['dateScheduled']
    info.append(dateScheduled.strftime("%d/%m/%Y a las %I:%M %p"))
    #we get modifiedBy
    if(event['modifiedBy_id']):#revisar que haya modificado
        modifiedBy=Profile.objects.get(id=event['modifiedBy_id'])
        modifiedBy=modifiedBy.user.username
        info.append(modifiedBy)
    else:
        info.append(" ")
    #we get dateModified
    dateModified=event['dateModified']
    if(dateModified):#revisar que haya modificado
        info.append(dateModified.strftime("%d/%m/%Y a las %I:%M %p"))
    else:
        info.append(" ")

    return info

def see_schedules(request):
    #events' array (freetime and services) for the context
    sc_days=[[],[],[],[],[],[],[]]
    #we start looking for the day of the week
    weekdays=["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"]
    #the first date 
    actualDate=date.today()
    contDay=0
    while(contDay<7):
        #have to avoid the sunday
        if(actualDate.isoweekday()==7):
            increment=timedelta(days=1)
            actualDate+=increment
            continue
        
        #name of de day
        day=weekdays[actualDate.weekday()]
        subtitle=["sc-subtitle","1/31",day+' '+str(actualDate.day)+'/'+str(actualDate.month)]
        sc_days[contDay].append(subtitle)
        #change the style of the previous hours
        li=timedelta(hours=7)
        #every day starts at 07:45am
        ti=timedelta(hours=7,minutes=45)
        newSC_event=["sc-event block",deltas2line(li,ti)]
        sc_days[contDay].append(newSC_event)

        #we get actualDate's agenda
        agenda=Turn.objects.filter(date=actualDate).values()

        for event in agenda:
            beg=timedelta(hours=event['hour'].hour,minutes=event['hour'].minute)
            fillFree(ti,beg,sc_days[contDay])

            #finally we add the service
            finish=timedelta(minutes=event['duration'])
            finish+=beg
            debugEvent(False,beg,finish)

            newSC_event=["sc-event turn",deltas2line(beg,finish),"",delta2time(beg)+" - "+delta2time(finish), processData(event)]
            sc_days[contDay].append(newSC_event)

            ti=finish

        #day ends at...
        # if sturday at 12:00m 
        if(actualDate.isoweekday()==6):
            end=timedelta(hours=12)
        # else at 05:15pm
        else:
            end=timedelta(hours=17,minutes=15)

        if(ti<end):
            fillFree(ti,end,sc_days[contDay])

        #change the style of the last hours
        ls=timedelta(hours=18)
        newSC_event=["sc-event block",deltas2line(end,ls)]
        if(contDay==6):
            newSC_event[1]= str(newSC_event[1])+"; border-bottom-right-radius: 2em"
        sc_days[contDay].append(newSC_event)

        contDay+=1
        actualDate+=timedelta(days=1)
        print("---------end day------------")

    return render(request,template_name="1-2-3-see_schedules.html", context={'sc_days':sc_days,'role':getRole(request)})

def asign_turns(request):
    return render(request,template_name="1-2-asign_turns.html")

def modify_schedules(request):
    return render(request,template_name="1-modify_schedules.html")

def validate_service_provided(request):
    return render(request,template_name="1-validate_service_provided.html")
