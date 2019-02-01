from django.shortcuts import render

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template

# our view
# def contact(request):
#     form_class = ContactForm
#
#     # new logic!
#     if request.method == 'POST':
#         form = form_class(data=request.POST)
#
#         if form.is_valid():
#             contact_name = request.POST.get(
#                 'contact_name'
#             , '')
#             contact_email = request.POST.get(
#                 'contact_email'
#             , '')
#             form_content = request.POST.get('content', '')
#
#             # Email the profile with the
#             # contact information
#             template =
#                 get_template('contact_template.txt')
#             context = {
#                 'contact_name': contact_name,
#                 'contact_email': contact_email,
#                 'form_content': form_content,
#             }
#             content = template.render(context)
#
#             email = EmailMessage(
#                 "New contact form submission",
#                 content,
#                 "Your website" +'',
#                 ['youremail@gmail.com'],
#                 headers = {'Reply-To': contact_email }
#             )
#             email.send()
#             return redirect('contact')
#
#     return render(request, 'contact.html', {
#         'form': form_class,
#     })

def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            contact_email = form.cleaned_data['contact_email']
            contact_name = form.cleaned_data['contact_name']
            message = form.cleaned_data['message']


            # Email the profile with the
            # contact information
            template = get_template('contacts/contact_template.txt')
            context = {
            'contact_name': contact_name,
            'contact_email': contact_email,
            'subject': subject,
            'message': message,
            }
            content = template.render(context)
            try:
                email = EmailMessage(
                    "New contact form submission",
                    content,
                    "Your website" + '',
                    ['rkvemuri2006@gmail.com'],
                    headers={'Reply-To': contact_email}
                )

                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')

    return render(request, 'contacts/email.html', {'form': form})
    #         try:
    #             send_mail(subject, message, from_email, from_email,to_email)
    #         except BadHeaderError:
    #             return HttpResponse('Invalid header found.')
    #         return redirect('success')
    # return render(request, "contacts/email.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')
