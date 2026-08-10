from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import QuoteRequest
from datetime import datetime

# Create your views here.

def index(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "hero_quote":
            full_name = request.POST.get("full_name")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            service_type = request.POST.get("service_type")
            pickup = request.POST.get("pickup_location")
            dropoff = request.POST.get("dropoff_location")
            move_size = request.POST.get("move_size")
            move_date_raw = request.POST.get("move_date")
            move_time_raw = request.POST.get("move_time")

            # 1. Save entry to Database
            QuoteRequest.objects.create(
                full_name=full_name,
                phone=phone,
                email=email,
                service_type=service_type,
                pickup_location=pickup,
                dropoff_location=dropoff,
                move_size=move_size,
                move_date=move_date_raw if move_date_raw else None,
                move_time=move_time_raw if move_time_raw else None,
            )

            # Format Date and Time safely for HTML emails
            formatted_date = "N/A"
            if move_date_raw:
                try:
                    formatted_date = datetime.strptime(move_date_raw, "%Y-%m-%d").strftime("%B %d, %Y")
                except ValueError:
                    formatted_date = move_date_raw

            formatted_time = "N/A"
            if move_time_raw:
                try:
                    formatted_time = datetime.strptime(move_time_raw, "%H:%M").strftime("%I:%M %p")
                except ValueError:
                    formatted_time = move_time_raw

            # 2. HTML Email for Admin Notification
            admin_html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden;">
                <div style="background-color: #0F4C2A; padding: 20px; text-align: center;">
                    <h2 style="color: #FFFFFF; margin: 0; font-size: 20px;">New Quote Request (10% OFF Claim)</h2>
                </div>
                <div style="padding: 24px; background-color: #FFFFFF;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px 0; font-weight: bold;">Customer Name:</td><td>{full_name}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">Phone Number:</td><td><a href="tel:{phone}" style="color: #0F4C2A;">{phone}</a></td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">Email Address:</td><td>{email}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">Service Required:</td><td>{service_type}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">Pickup Location:</td><td>{pickup}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">Dropoff Location:</td><td>{dropoff}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">Move Size:</td><td>{move_size}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">Scheduled Date:</td><td>{formatted_date}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">Scheduled Time:</td><td>{formatted_time}</td></tr>
                    </table>
                </div>
                <div style="background-color: #F0F6F2; padding: 15px; text-align: center; font-size: 12px; color: #555;">
                    Chitwan Removal & Logistics • 22 Clarence Street, Lidcombe
                </div>
            </div>
            """

            # 3. HTML Email for Customer Confirmation
            customer_html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden;">
                <div style="background-color: #0F4C2A; padding: 24px; text-align: center;">
                    <h1 style="color: #FFFFFF; margin: 0; font-size: 22px;">Chitwan Removal & Logistics</h1>
                    <p style="color: #F2A900; margin: 5px 0 0 0; font-weight: bold;">Quote Request Received (10% Discount Applied)</p>
                </div>
                <div style="padding: 24px; background-color: #FFFFFF; line-height: 1.6; color: #333333;">
                    <p>Hi <strong>{full_name}</strong>,</p>
                    <p>Thank you for choosing Chitwan Removal & Logistics. We have successfully logged your moving inquiry with a <strong>10% online booking discount</strong>.</p>
                    
                    <div style="background-color: #F0F6F2; padding: 16px; border-radius: 6px; margin: 20px 0; border-left: 4px solid #0F4C2A;">
                        <h3 style="margin-top: 0; color: #0F4C2A; font-size: 16px;">Booking Summary</h3>
                        <p style="margin: 4px 0;"><strong>Service:</strong> {service_type}</p>
                        <p style="margin: 4px 0;"><strong>Pickup:</strong> {pickup}</p>
                        <p style="margin: 4px 0;"><strong>Dropoff:</strong> {dropoff}</p>
                        <p style="margin: 4px 0;"><strong>Move Size:</strong> {move_size}</p>
                        <p style="margin: 4px 0;"><strong>Preferred Date:</strong> {formatted_date}</p>
                        <p style="margin: 4px 0;"><strong>Preferred Time:</strong> {formatted_time}</p>
                    </div>

                    <p>Our dispatch operations team based at <strong>22 Clarence Street, Lidcombe</strong> is preparing your customized price estimate and will contact you shortly.</p>
                    <p style="margin-bottom: 0;">Need immediate assistance? Call us directly at <a href="tel:0470266582" style="color: #0F4C2A; font-weight: bold;">0470 266 582</a>.</p>
                </div>
                <div style="background-color: #1A1A1A; color: #FFFFFF; padding: 16px; text-align: center; font-size: 12px;">
                    Chitwan Removal & Logistics | 22 Clarence Street, Lidcombe<br>
                    Phone: 0470 266 582 | Email: cnsgroup30@gmail.com
                </div>
            </div>
            """

            try:
                # Send email to Admin
                send_mail(
                    subject=f"[Quote Request] New Inquiry from {full_name}",
                    message=f"New Quote Request from {full_name}. Please view in HTML.",
                    from_email="cnsgroup30@gmail.com",
                    recipient_list=["cnsgroup30@gmail.com"],
                    html_message=admin_html,
                    fail_silently=False,
                )

                # Send email to Customer
                send_mail(
                    subject="We Received Your Quote Request - Chitwan Removal & Logistics",
                    message=f"Hi {full_name}, thank you for your quote request. We will contact you shortly.",
                    from_email="cnsgroup30@gmail.com",
                    recipient_list=[email],
                    html_message=customer_html,
                    fail_silently=False,
                )

                messages.success(
                    request,
                    "Your quote request has been submitted successfully! Check your email for confirmation.",
                )
            except Exception:
                messages.warning(
                    request,
                    "Your quote request was saved, but there was an issue sending the confirmation email.",
                )

            return redirect("index")

    return render(request, "main/index.html")

def about(request):
    return render(request,"main/about.html")

def services(request):
    return render(request,"main/services.html")

def appliances(request):
    return render(request,"main/appliances.html")

def contact(request):
    return render(request,"main/contact.html")