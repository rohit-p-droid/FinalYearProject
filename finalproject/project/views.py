from django.shortcuts import render, HttpResponse
from django.contrib import messages
import razorpay
from django.conf import settings
from project.models import Monuments

# Create your views here.

def index(request):
    messages.success(request, "this is test message")
    return render(request, 'index.html')

def about(request):
    return HttpResponse('about page here...')

def adminLogin(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        passwd = request.POST.get('password')
        if uname == "admin" and passwd == "admin":
            monumentsData = Monuments.objects.all()
            data = {
                'monumentsData' :monumentsData
            }
            return render(request, 'viewMonuments.html', data)
        
    return render(request, 'adminLogin.html')

def addMonument(request):
    if request.method == "POST":
        city = request.POST.get('city')
        monument = request.POST.get('monument')
        indPrice = request.POST.get('indprice')
        foreignPrice = request.POST.get('foreignprice')
        monuments = Monuments(city=city, monument=monument, indPrice=indPrice, foreignPrice=foreignPrice)
        monuments.save()
        #messages.success(request, 'Monument added successfully!!')

    return render(request, 'addMonuments.html')

def viewMonuments(request):
    monumentsData = Monuments.objects.all()
    data = {
        'monumentsData' :monumentsData
    }
    return render(request, 'viewMonuments.html', data)

def bookTicket(request):
    monumentsData = Monuments.objects.all()
    data = {
        'monumentsData' :monumentsData
    }
    return render(request, 'bookTicket.html', data)

def getMonument(request):
    if request.method == "POST":
        city = request.POST.get("monument")
    cityMonuments = Monuments.objects.filter(city=city).values()
    #  mydata = Member.objects.filter(firstname='Emil').values()
    data = {
        'cityMonuments' :cityMonuments
    }

    return render(request, 'bookTicket.html', data)

def selectCity(request):
    monumentsData = Monuments.objects.all()
    data = {
        'monumentsData' :monumentsData
    }
    # if request.method == "POST":
    #     city = request.POST.get('city')
    #     cityMonuments = Monuments.objects.filter(city='chopda').values()
    #     data = {
    #         cityMonuments: 'cityMonuments'
    #     }
    #     return render(request, 'selectMonument.html', data)

    return render(request, 'selectCity.html', data)

def selectMonument(request):
    if request.method == "POST":
        city = request.POST.get("city")
       
    cityMonuments = Monuments.objects.filter(city=city).values()
    data = {
        'cityMonuments' :cityMonuments
    }

    return render(request, 'selectMonument.html', data) 


def booking(request):
    if request.method == "POST":
        monument = request.POST.get("mon")
    infoMonuments = Monuments.objects.filter(monument=monument).values()
    data = {
        'infoMonuments' :infoMonuments
    }
    return render(request, 'booking.html', data)

def ticketDetail(request):
    if request.method == "POST":
        global email
        email = request.POST.get("email")
        global id
        id = request.POST.get("id")
        if id.isnumeric():
            pass
        else:
            id = id[:-1]
        global count
        count = request.POST.get("count")
        global citizen
        citizen = request.POST.get("citizen")
        global date
        date = request.POST.get("date")
        global time
        time = request.POST.get("time")

        if citizen.isnumeric():
            price = int(citizen) * int(count)
        else:
            citizen = citizen[:-1]
            price = int(citizen) * int(count)
        
        client = razorpay.Client(auth = (settings.KEY, settings.SECRET))
        payment = client.order.create({'amount': price*100, 'currency': 'INR', 'payment_capture': 1})
        paymentData = {
            'money':price,
            'payment': payment
        }
        return render(request, "payment.html", paymentData)
    
def payment(request):
    order_id = request.GET.get('order_id')

    # ticket = Ticket(id=1, monumentId=id, totalPrice=totalPrice, time=time, date=date, transactionId=order_id, email=email)
    # ticket.save()

    print(order_id)
    info = {
        'email':email,
        'monId':id,
        'count':count,
        'citizen':citizen,
        'date':date,
        'time':time
    }
    print(info)
    return HttpResponse("Payment Success")

    


    




