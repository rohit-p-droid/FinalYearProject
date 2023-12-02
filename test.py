import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Email credentials and server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'your_email@gmail.com'
password = 'your_password'

# Email content
from_email = 'your_email@gmail.com'
to_email = 'recipient_email@example.com'
subject = 'Email With QR Code Attachment'
body = 'Please find the attached QR code.'

# Create a multipart message
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = subject

# Attach the email body
msg.attach(MIMEText(body, 'plain'))

# Attach the QR code image
with open('path_to_qr_code_image.png', 'rb') as qr_file:
    qr_img = MIMEImage(qr_file.read())
    qr_img.add_header('Content-ID', '<qr_code>')
    qr_img.add_header('Content-Disposition', 'attachment; filename="qr_code.png"')
    msg.attach(qr_img)

# Send the email
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(username, password)  # Log in to the SMTP server
        server.send_message(msg)  # Send the email
        print('Email sent successfully!')
except Exception as e:
    print(f'Failed to send email: {e}')






import qrcode
from io import BytesIO
from django.core.mail import EmailMessage
from django.http import HttpResponse

def send_qr_code_email(request):
    # Text to be converted into QR code
    qr_text = 'Your text here'

    # Generate QR code
    qr_img = qrcode.make(qr_text)
    img_buffer = BytesIO()
    qr_img.save(img_buffer)
    img_buffer.seek(0)

    # Email details
    email = EmailMessage(
        subject='Your QR Code',
        body='Please find the attached QR code.',
        from_email='from@example.com',
        to=['to@example.com'],
    )

    # Attach the QR code
    email.attach('qr_code.png', img_buffer.getvalue(), 'image/png')

    # Send the email
    try:
        email.send()
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse(f'Failed to send email: {e}')

# Add the view to your urls.py and call it from your Django project as needed.

