from django.shortcuts import render, redirect # Standard view rendering
from .forms import PersonForm, ContactForm # Pulling in form information
from django.views.generic import View # Standard View class
from django.contrib import messages # for success and other message
from django.core.mail import send_mail # to access send_mail function
from django.conf import settings # pulling email settings


# Create your views here.
class Home(View):
    '''This View collects member registration data and saves it in the Person's Model
        via the PersonForm ModelForm'''
    def get(self, request):
        form = PersonForm()

    #if request.user.is_authenticated(): # you can show different content based on auth
    #    context = {'user': request.user, 'email': request.user.email}
        return render(request, "dsx/home.html", {'form': form})

    def post(self, request):
        form = PersonForm(request.POST)
        if form.is_valid():
            #form_inst = form.save(commit=False)
            #do some customization to the fields here
            form.save()

            messages.success(request, "Registration Success!")
            return redirect("Home") #maybe put conditional if user is authenticated

        return render(request, "dsx/home.html", {'form': form})


class ContactPage(View):
    '''This View collects form data and also sends the user an email
        django email docs https://docs.djangoproject.com/en/1.10/topics/email/
        Might need to look at Captcha for sending a lot of emails
    '''
    def get(self, request):
        form = ContactForm()
        return render(request, "dsx/contact.html", {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            message = form_data['message']
            subject = 'Site contact form'
            from_email = settings.EMAIL_HOST_USER
            to_email = [form_data['email']]
            # message=render_to_string(
            #     "chet/email/resolved_report.txt", {'report': form_submit, 'submitter': report.submitter}),
            # send_mail(
            #     subject,
            #     message,
            #     from_email,
            #     to_email,
            #     fail_silently=False
            # )

            messages.success(request, "Contact Form Submitted, check your email")
            return redirect("Home")
        return redirect("Contact")

