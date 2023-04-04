from django.shortcuts import render
from .models import *
from .forms import CreateUserForm
from django.contrib import messages

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
