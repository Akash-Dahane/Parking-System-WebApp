from django.shortcuts import render,redirect
from .models import ParkingInfo,ParkingSpot
from datetime import datetime,timedelta
from django.contrib.auth.models import User,auth
from django.contrib import messages

# Create your views here.
def index(request):
    total=ParkingSpot.objects.all().count()
    vacant= ParkingSpot.objects.filter(isoccupied=False).count()
    return render(request,'index.html',{'total':total,'vacant':vacant,'booked':(total-vacant)})

def home(request):
    uid=request.user
    hasbooking=ParkingInfo.objects.filter(userid=uid.id,isactive=True)
    if hasbooking.exists():
        return render(request,'parkinginfo.html',{'vehicleid':hasbooking[0].vehicleid,'slotid':hasbooking[0].slotid.id,'stime':hasbooking[0].stime,'etime':hasbooking[0].etime})
    else:
        freespots= ParkingSpot.objects.filter(isoccupied=False)
        occupiedspots=ParkingInfo.objects.filter(isactive=True)
        return render(request,'home.html',{'freespots':freespots,'occupiedspots':occupiedspots})
def book(request):
    if request.method=='POST':
        slotid=request.POST['slotid']
        slot=ParkingSpot.objects.get(id=slotid)
        slot.isoccupied=True
        slot.save()
        uid= request.POST['userid']
        userid=User.objects.get(id=uid)

        hourss=int(request.POST['hours'])
        dateobj=datetime.now() + timedelta(minutes=10)
        etimeobj=dateobj+timedelta(hours=hourss,minutes=10)

        #finaltime=dateobj.strftime("%d/%m/%Y %H:%M:%S")
        vehicleid= request.POST['vehicleid']
        details=ParkingInfo(userid=userid,slotid=slot,stime=dateobj,etime=etimeobj,vehicleid=vehicleid,isactive=True)
        details.save()
        return redirect('home')
    else:
        return redirect('home')

def vacate(request):
    if request.method=='POST':
        uid =request.user
        slotid=request.POST['slotid']
        print(slotid)
        undoslot=ParkingSpot.objects.get(id=slotid)
        undoslot.isoccupied=False
        undoslot.save()
        undoinfo=ParkingInfo.objects.get(slotid=undoslot,isactive=True)
        undoinfo.isactive=False
        undoinfo.etime=datetime.now()+timedelta(minutes=10)
        undoinfo.save()
        return redirect('home')
    else:
        return redirect('home')
    
def parkhistory(request):
    uid=request.user
    histry=ParkingInfo.objects.filter(userid=uid).order_by('-id')
    return render(request,'uhistory.html',{'histry':histry})

def update(request):
    
    if request.method == 'POST':
        uid =request.user
        email=request.POST['email1']
        if email is None:
            messages.info(request,'email field cannot be empty...')
            return redirect('update')
        match=User.objects.filter(email=email)
        print(match)
        print(email)
        if uid.email==email:
            messages.info(request,'email is same')
            return redirect('update')
        elif match.exists():
            messages.info(request,'email taken')
            return redirect('update')
        else:
            updating=User.objects.get(id=uid.id)
            updating.email=email
            updating.save()
            messages.info(request,'contact details were updated successfully...')
            return redirect('home')
    else:
        return render(request,'conupdt.html')


def extendtime(request):
    if request.method=='POST':
        uid =request.user
        slotid=request.POST['slotid']
        hourss=int(request.POST['hours'])
        print(slotid)
        extndslot=ParkingSpot.objects.get(id=slotid)
        exinfo=ParkingInfo.objects.get(slotid=extndslot,isactive=True)
        exinfo.etime+=timedelta(hours=hourss)
        exinfo.save()
        return redirect('home')
    else:
        return redirect('home')          
            
            
            


    