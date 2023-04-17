from django.shortcuts import render,redirect
from .models import *
from .forms import CreateUserForm
from django.contrib import messages

from datetime import date,time,timedelta,datetime

# Create your views here.
from django.http import HttpResponse

#---------------get the role--------------#
def getRole(request):
    actualProfile=Profile.objects.get(user=request.user)
    return actualProfile.rol
#-----------------------------------------#
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

def reports(request):
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
        hour+=" AM"
    else:
        hour+=" PM"

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
    date = event.date

    strDate=days[date.weekday()]+", "+str(date.day)+" de "+months[date.month-1]+", "+str(date.year)
    info.append(strDate)
    #we get cvs
    info.append(event.cvs.name)
    #we get hour
    hour=event.hour
    info.append(hour.strftime("%I:%M %p"))
    #we get duration
    duration=str(event.duration)+" minutos"
    info.append(duration)
    #we get typeTire
    typeTire=event.typeTire
    if(typeTire==1):
        typeTire="Automóvil"
    elif(typeTire==2):
        typeTire="Camioneta"
    elif(typeTire==3):
        typeTire="Camión"
    info.append(typeTire)
    #we get quantity
    quantity=str(event.quantity)+" llantas"
    info.append(quantity)
    #we get rotation
    rotation=event.rotation
    if(rotation):
        rotation="Sí"
    else:
        rotation="No"
    info.append(rotation)
    #we get quantityRotate
    quantityRotate=str(event.quantityRotate)+" llantas"
    info.append(quantityRotate)
    #we get bill
    bill=str(event.bill)
    info.append(bill)
    #we get idCustomer
    idCustomer=str(event.idCustomer)
    info.append(idCustomer)
    #we get nameCustomer
    info.append(event.nameCustomer)
    #we get telCustomer
    info.append(event.telCustomer)
    #we get scheduledBy
    scheduledBy=event.scheduledBy.user.username
    info.append(scheduledBy)
    #we get dateScheduled
    dateScheduled=event.dateScheduled
    info.append(dateScheduled.strftime("%d/%m/%Y a las %I:%M %p"))
    #we get modifiedBy
    if(event.modifiedBy):#revisar que haya modificado
        modifiedBy=event.modifiedBy.user.username
        info.append(modifiedBy)
    else:
        info.append(" ")
    #we get dateModified
    dateModified=event.dateModified
    if(dateModified):#revisar que haya modificado
        info.append(dateModified.strftime("%d/%m/%Y a las %I:%M %p"))
    else:
        info.append(" ")

    return info

def toSee_schedules(cvsName):
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
        agenda=Turn.objects.filter(date=actualDate).filter(cvs__name=cvsName).order_by("hour")

        for event in agenda:
            beg=timedelta(hours=event.hour.hour,minutes=event.hour.minute)
            fillFree(ti,beg,sc_days[contDay])

            #finally we add the service
            finish=timedelta(minutes=event.duration)
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

    return sc_days

def listCVS(cvsName):
    cvsQuery= CVS.objects.all().order_by("name")

    listNames=[]

    for cvs in cvsQuery:
        listNames.append(cvs.name)

    if(cvsName):
        listNames.remove(cvsName)

    return listNames

def see_schedules(request):
    if(request.method=='POST'):
        cvsName=request.POST.get('cvsName')
        #events' array (freetime and services) for the context
        sc_days=toSee_schedules(cvsName)
        #cvs' names for the combo box
        listCVSs=listCVS(cvsName)
        return render(request,template_name="1-2-3-see_schedules.html", context={'cvsName':cvsName,'sc_days':sc_days,'listCVSs':listCVSs,'role':getRole(request)})
    else:
        #cvs' names for the combo box
        listCVSs=listCVS('')
        return render(request,template_name="1-2-3-see_schedules.html", context={'listCVSs':listCVSs,'role':getRole(request)})
    
def asign_turns(request):
    if(request.method=='POST'):
        if(request.POST.get('cvsName')):
            cvsName=request.POST.get('cvsName')
        else:
            cvsName=request.POST.get('sc-select')
        #events' array (freetime and services) for the context
        sc_days=toSee_schedules(cvsName)
        #cvs' names for the combo box
        listCVSs=listCVS(cvsName)
        return render(request,template_name="1-2-asign_turns.html", context={'cvsName':cvsName,'sc_days':sc_days,'listCVSs':listCVSs,'role':getRole(request)})
    else:
        #cvs' names for the combo box
        listCVSs=listCVS('')
        return render(request,template_name="1-2-asign_turns.html",context={'listCVSs':listCVSs,'role':getRole(request)})   

#---------- auxiliar methods for time_turns-------------------#
def valQuantity(request,quantity):
    problems=False
    #quantity must be an integer
    if(quantity%1>0):
        problems=True
        messages.error(request,"La cantidad de llantas del servicio no puede ser fraccionaria")
    #quantity must be a positive integer
    if(quantity<=0):
        problems=True
        messages.error(request,"La cantidad de llantas del servicio debe ser mayor que 0")

    return problems

def valQuantityRotate(request,quantityRotate,quantity):
    problems=False
    #quantity must be an integer
    if(quantityRotate%1>0):
        problems=True
        messages.error(request,"La cantidad de llantas a rotar no puede ser fraccionaria")
    #quantity must be a positive integer
    if(quantityRotate<=0):
        problems=True
        messages.error(request,"La cantidad de llantas a rotar debe ser mayor que 0")
    #politics says, rotating wheels must be lower or equal than service wheels
    if(quantityRotate>quantity):
        problems=True
        messages.error(request,"La cantidad de llantas a rotar debe ser menor o igual a las llantas del servicio")

    return problems

def calculateTime(typeTire,quantity,rotation,quantityRotate):
    timeService=45
    #how to calculate

    #always add 5 minutes for the rest after service
    timeService+=5

    return timeService

def valDuration(request,duration):
    problems=False
    #quantity must be an integer
    if(duration%1>0):
        problems=True
        messages.error(request,"La duración no puede ser fraccionaria")
    #quantity must be a positive integer
    if(duration<=0):
        problems=True
        messages.error(request,"La duración debe ser mayor que 0")

    return problems

def time_turns(request):
    if(request.method=='POST'):
        cvsName=request.POST.get('cvsName')
        typeTire=int(request.POST.get('typeTire'))
        quantity=float(request.POST.get('quantity'))
        flag1=valQuantity(request,quantity)
        if(request.POST.get('rotation')):
            rotation="True"
            quantityRotate=float(request.POST.get('quantityRotate'))
            flag2=valQuantityRotate(request,quantityRotate,quantity)
        else:
            rotation=""
            quantityRotate=0
            flag2=False

        #events' array (freetime and services) for the context
        sc_days=toSee_schedules(cvsName)
        #cvs' names for the combo box
        listCVSs=listCVS(cvsName)
        
        #debug
        print("valores:",cvsName,"|",typeTire,"|",quantity,"|",rotation,"|",quantityRotate)

        #validation
        if(flag1 or flag2):
            return render(request,template_name="1-2-asign_turns.html", context={'cvsName':cvsName,'sc_days':sc_days,'listCVSs':listCVSs,'role':getRole(request)})
        else:
            #fixing some fields before sending
            quantity=int(quantity)
            quantityRotate=int(quantityRotate)

            #validating duration
            if(request.POST.get('duration')):
                duration=float(request.POST.get('duration'))
                flag3=valDuration(request,duration)
                if(flag3):
                    duration=calculateTime(typeTire,quantity,rotation,quantityRotate)
                    
                    return render(request,template_name="1-2-time_turns.html", context={'cvsName':cvsName,'sc_days':sc_days,'listCVSs':listCVSs,'typeTire':typeTire,'quantity':quantity,'rotation':rotation,'quantityRotate':quantityRotate,'duration':duration,'role':getRole(request)})
                else:
                    duration=int(duration)
            else:
                duration=calculateTime(typeTire,quantity,rotation,quantityRotate)

            return render(request,template_name="1-2-time_turns.html", context={'cvsName':cvsName,'sc_days':sc_days,'listCVSs':listCVSs,'typeTire':typeTire,'quantity':quantity,'rotation':rotation,'quantityRotate':quantityRotate,'duration':duration,'role':getRole(request)})
    else:
        #cvs' names for the combo box
        listCVSs=listCVS('')
        return render(request,template_name="1-2-time_turns.html",context={'listCVSs':listCVSs,'role':getRole(request)})   
    
def select_turns(request):
    if(request.method=='POST'):
        cvsName=request.POST.get('cvsName')
        typeTire=int(request.POST.get('typeTire'))
        quantity=int(request.POST.get('quantity'))
        rotation=request.POST.get('rotation')
        quantityRotate=int(request.POST.get('quantityRotate'))
        duration=int(request.POST.get('duration'))
        #events' array (freetime and services) for the context
        sc_days=toSee_schedules(cvsName)
        return render(request,template_name="1-2-select_turns.html", context={'cvsName':cvsName,'sc_days':sc_days,'typeTire':typeTire,'quantity':quantity,'rotation':rotation,'quantityRotate':quantityRotate,'duration':duration,'role':getRole(request)})
    else:
        return render(request,template_name="1-2-select_turns.html",context={'role':getRole(request)})

#---------- auxiliar methods for confirm asignment-------------------#
def valDateHour(request,dateF,hour,duration):
    problems=False
    dateTurns=Turn.objects.filter(date=dateF).order_by('hour')
    actualTurns=[]
    for turn in dateTurns:
        beg=timedelta(hours=turn.hour.hour,minutes=turn.hour.minute)
        end=beg+timedelta(minutes=turn.duration)
        actualTurns.append([beg,end])

    begHour=timedelta(hours=hour.hour,minutes=hour.minute)
    endHour=begHour+timedelta(minutes=duration)

    #turn must not be earlier than 7:45 nor later than 17:15
    if(begHour<timedelta(hours=7,minutes=45)):
        problems=True
        messages.error(request,"El servicio no puede comenzar antes del horario laboral (7:45am)")
    if(endHour>timedelta(hours=17,minutes=15)):
        problems=True
        messages.error(request,"El servicio no puede terminar luego del horario laboral (5:15pm)")

    #beg hour is crashing 
    if(len(actualTurns)):
        for turn in actualTurns:
            if(begHour<turn[1]):
                if(begHour>turn[0]):
                    problems=True
                    messages.error(request,"El servicio choca con el servicio de las "+delta2time(turn[0]))

                break
        #end hour is crashing 
        actualTurns.reverse()
        for turn in actualTurns:
            if(endHour>turn[0]):
                if(endHour<turn[1]):
                    problems=True
                    messages.error(request,"El servicio choca con el servicio de las "+delta2time(turn[0]))

                break
        #it is something in the middle
        for turn in actualTurns:
            if(endHour>turn[1] and begHour<turn[0]):
                problems=True
                messages.error(request,"El servicio choca con el servicio de las "+delta2time(turn[0]))

                break

        return problems

def valBill(request,bill):
    problems=False
    #quantity must be an integer
    if(bill%1>0):
        problems=True
        messages.error(request,"El número de factura no puede ser fraccionaria")
    #quantity must be a positive integer
    if(bill<=0):
        problems=True
        messages.error(request,"El número de factura debe ser mayor que 0")
    #tamaño?
    return problems

def valId(request,id):
    problems=False
    #quantity must be an integer
    if(id%1>0):
        problems=True
        messages.error(request,"El id del cliente no puede ser fraccionaria")
    #quantity must be a positive integer
    if(id<=0):
        problems=True
        messages.error(request,"El id del cliente no puede ser 0")

    return problems

def confirm_turns(request):
    if(request.method=='POST'):
        cvsName=request.POST.get('cvsName')
        typeTire=int(request.POST.get('typeTire'))
        quantity=int(request.POST.get('quantity'))
        rotation=request.POST.get('rotation')
        quantityRotate=int(request.POST.get('quantityRotate'))
        duration=int(request.POST.get('duration'))
        dateF=date.fromisoformat(request.POST.get('date'))
        hour=time.fromisoformat(request.POST.get('hour'))
        flag1=valDateHour(request,dateF,hour,duration)
        bill=float(request.POST.get('bill'))
        flag2=valBill(request,bill)
        idCustomer=float(request.POST.get('idCustomer'))
        flag3=valId(request,idCustomer)
        nameCustomer=request.POST.get('nameCustomer')
        telCustomer=request.POST.get('telCustomer')

        if(flag1 or  flag2 or flag3):
            return render(request,template_name="1-2-select_turns.html", context={'cvsName':cvsName,'typeTire':typeTire,'quantity':quantity,'rotation':rotation,'quantityRotate':quantityRotate,'duration':duration,'role':getRole(request)})
        else:
            bill=int(bill)
            idCustomer=int(idCustomer)
            newTurn=Turn(
                cvs = CVS.objects.get(name=cvsName),
                typeTire = typeTire,
                quantity = quantity,
                rotation = bool(rotation),
                quantityRotate = quantityRotate,
                duration = duration,
                date = dateF,
                hour = hour,
                bill = bill,
                idCustomer = idCustomer,
                nameCustomer = nameCustomer,
                telCustomer = telCustomer,
                scheduledBy = Profile.objects.get(user=request.user),
                # dateScheduled = datetime.now(),
                modifiedBy = Profile.objects.get(user=request.user),
                dateModified = datetime.now(),
                done = False,
                # comment = ""
            )
            newTurn.save()
            messages.success(request,"Se ha agendado correctamente el turno con id: "+str(newTurn.id)+" en CVS: "+cvsName+" el día "+dateF.strftime("%d/%m/%Y")+" a las "+hour.strftime("%I:%M %p"))

            return redirect('see_schedules')

def modify_schedules(request):
    return render(request,template_name="1-modify_schedules.html")

def validate_service_provided(request):
    return render(request,template_name="1-validate_service_provided.html")
