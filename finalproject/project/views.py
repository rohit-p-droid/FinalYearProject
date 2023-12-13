from django.shortcuts import render, HttpResponse
from django.contrib import messages
import razorpay
from django.conf import settings
from project.models import Monuments
from project.models import Tikect
from django.core.mail import send_mail

from django.core.mail import EmailMessage
from django.http import HttpResponse
from io import BytesIO
import qrcode

import cv2
from pyzbar.pyzbar import decode
import time

# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage

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
        price = request.POST.get('price')
        image = request.POST.get('image')
        monuments = Monuments(city=city, monument=monument, price=price, image=image)
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
    monumentsData = Monuments.objects.values('city').distinct()
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

# def selectCity(request):
#     monumentsData = Monuments.objects.all()
#     data = {
#         'monumentsData' :monumentsData
#     }

#     return render(request, 'selectCity.html', data)

# def selectMonument(request):
#     if request.method == "POST":
#         city = request.POST.get("city")
       
#     cityMonuments = Monuments.objects.filter(city=city).values()
#     data = {
#         'cityMonuments' :cityMonuments
#     }

#     return render(request, 'selectMonument.html', data) 


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
        global price
        price = request.POST.get("price")
        global gender
        gender = request.POST.get("gender")
        global date
        date = request.POST.get("date")
        global shift
        shift = request.POST.get("time")

        if price.isnumeric():
            price = int(price) * int(count)
        else:
            price = price[:-1]
            price = int(price) * int(count)
        
        client = razorpay.Client(auth = (settings.KEY, settings.SECRET))
        payment = client.order.create({'amount': price*100, 'currency': 'INR', 'payment_capture': 1})
        paymentData = {
            'money':price,
            'payment': payment
        }
        return render(request, "payment.html", paymentData)
    
def payment(request):
    order_id = request.GET.get('order_id')

    ticket = Tikect(email=email, monumentId=id, count=count, price=price, date=date, shift=shift, trasactionId=order_id, gender=gender)
    ticket.save()

    mail = email

    qr = order_id + id
    qr_img = qrcode.make(qr)
    img_buffer = BytesIO()
    qr_img.save(img_buffer)
    img_buffer.seek(0)
    gmail = EmailMessage(
        subject = 'Your Ticket is here',
        body = 'Here is your ticket for unintrupeted entry please find below attachment',
        from_email = 'ticketlessentrysystem@gmail.com',
        to = [mail],
    )
    gmail.attach('Ticket.png', img_buffer.getvalue(), 'image/png')

    try:
        gmail.send()
        return render(request, "success.html")
    except Exception as e:
        return HttpResponse(f'Failed: {e}')

def success(request):
    return render(request, 'success.html')


def verify(request):
    ticketData = Tikect.objects.all()
    cam = cv2.VideoCapture(0)
    cam.set(0, 640)
    cam.set(0, 480)

    camera = True
    code = ""
    while camera == True:
        success, frame = cam.read()

        for i in decode(frame):
            # print(i.type)
            code = i.data.decode('utf-8')
            time.sleep(2)   

            #cv2.imshow("OurQr_Code_Scanner", fram+e)
            cv2.waitKey(3)
            print("success = ", code)
            camera = False
        
            for ticket in ticketData:
                print("Code=",code)
                print("get=", ticket.trasactionId + str(ticket.monumentId))
                if code == (ticket.trasactionId + str(ticket.monumentId)) and ticket.scanned == False:
                    ticket.scanned = True
                    ticket.save()
                    ticketsData = {
                        'Tickets':ticket
                    }
                    return render(request, "entrySuccess.html", ticketsData)

            return render(request, "entryFailed.html")

        # return render(request, 'verify.html')

def regenerateTicket(request):
    if request.method == "POST":
        email = request.POST.get("email")
        transactionId = request.POST.get("transactionId")
        tickets = Tikect.objects.all()
        for ticket in tickets:
            if ticket.email == email and ticket.trasactionId == transactionId and ticket.scanned == False:
                qr = transactionId + str(ticket.monumentId)
                qr_img = qrcode.make(qr)
                img_buffer = BytesIO()
                qr_img.save(img_buffer)
                img_buffer.seek(0)
                gmail = EmailMessage(
                    subject = 'Your Ticket is here',
                    body = 'Here is your ticket for unintrupeted entry please find below attachment',
                    from_email = 'ticketlessentrysystem@gmail.com',
                    to = [email],
                )
                gmail.attach('Ticket.png', img_buffer.getvalue(), 'image/png')

                try:
                    gmail.send()
                    return render(request, "success.html")
                except Exception as e:
                    return HttpResponse(f'Failed: {e}')

    return render(request, "regenerateTicket.html")
    
def viewTicket(request):
    tickets = Tikect.objects.all()
    ticketsData = {
        'Tickets':tickets
    }
    return render(request, 'viewTickets.html', ticketsData)

def crowd(request):
    return render(request, 'crowd.html')

    


    




