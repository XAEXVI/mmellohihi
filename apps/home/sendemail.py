#!/usr/bin/env python3
import smtplib
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

def send_email(sender_email, receiver_email, subject, body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'mmellodesignsite@gmail.com'  # Replace with your Gmail email address
    smtp_password = 'Mmellosite12345678'  # Replace with the App Password generated for "Mail"

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send the email: {e}")
        return False

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_type, _ = cgi.parse_header(self.headers.get('content-type'))
        if content_type == 'application/x-www-form-urlencoded':
            content_length = int(self.headers.get('Content-Length'))
            form_data = self.rfile.read(content_length).decode('utf-8')
            form_data = dict(item.split("=") for item in form_data.split("&"))

            full_name = form_data.get("full_name", "")
            email = form_data.get("email", "")
            message = form_data.get("message", "")

            if full_name and email and message:
                sender_email = email  # Use the client's email as the sender
                receiver_email = "mmellodesignsite@gmail.com"  # Replace with the recipient email address
                subject = f"New Contact Form Submission from {full_name}"
                body = f"Full Name: {full_name}\nEmail: {email}\nMessage: {message}"

                if send_email(sender_email, receiver_email, subject, body):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write("Message sent successfully!".encode())
                else:
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write("Failed to send the message.".encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Invalid form data.".encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("Invalid request.".encode())
