# delivery_receipt/views.py

from django.shortcuts import render, redirect

from django.views import View
from django.views.generic.edit import FormView
from .forms import DeliveryReceiptForm, ItemForm, SignUpForm, SignInForm
from django.contrib.auth import authenticate,login,logout
from .models import DeliveryReceipt, Item
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas 
from django.core.mail import EmailMessage
from django.http import FileResponse
from reportlab.lib.units import inch
import io
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Item
from io import BytesIO



class ManageItemsView(View):
    template_name = 'manage_items.html'

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request. Displays the list of items and the form to add a new item.
        """
        form = ItemForm()
        items = Item.objects.all()
        context = {
            'form': form,
            'items': items,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request. Adds a new item to the database if the form is valid.
        """
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_items')  # Redirect to the same page after adding the item
        items = Item.objects.all()
        context = {
            'form': form,
            'items': items,
        }
        return render(request, self.template_name, context)

def render_to_pdf(template_src, context_dict={}):
    """
    Utility function to render a template into a PDF file.
    """
    from django.template.loader import get_template
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pisa_status = pisa.CreatePDF(
        html, dest=result
    )
    if pisa_status.err:
        return None
    return result.getvalue()  # Return raw PDF bytes

def generate_items_pdf(request):
    """
    View to generate and return the PDF for items.
    """
    items = Item.objects.all()
    context = {
        'items': items,
    }
    pdf = render_to_pdf('items_pdf_template.html', context)
    
    if pdf:
        # Wrap the raw PDF bytes in a BytesIO object

        response = HttpResponse(pdf, content_type='application/pdf')
        
        response['Content-Disposition'] = 'inline; filename="items.pdf"'
        
        return response

    
    return HttpResponse('Failed to generate PDF.')

def send_items_email(request):
    """
    View to generate a PDF of items and send it via email.
    """
    items = Item.objects.all()

    context = {
        'items': items,
    }
    pdf = render_to_pdf('items_pdf_template.html', context)  # Generate the PDF
    if pdf:
        # Email settings
        
        subject = 'Delivery Receipt'
        
        message = 'Please find attached the delivery receipt.'
        
        recipient_list = ['recipient@example.com']  # Replace with actual recipient email
        
        sender_email = 'your_email@example.com'  # Replace with your sender email

        # Create the email
        email = EmailMessage(subject, message, sender_email, recipient_list)

        # Attach the PDF
        email.attach('delivery_receipt.pdf', pdf, 'application/pdf')

        # Send the email
        email.send()
        return HttpResponse('Email sent successfully!')
    return HttpResponse('Failed to generate PDF for email.')

class SignUpView(View):

    template_name="signup.html"

    form_class=SignUpForm

    def get(self,request,*arg,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_data=request.POST 

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("signin")

        print("account creation failed")

        return render(request,self.template_name,{"form":form_instance})

class SignInView(View):

    template_name="signin.html"

    form_class=SignInForm


    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_data=request.POST 

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_obj=authenticate(request,username=uname,password=pwd)

            if user_obj:

                login(request,user_obj)


                return redirect("create_receipt")


        return render(request,self.template_name,{"form":form_instance})

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    
class CreateDeliveryReceiptView(FormView):

    template_name = 'create_receipt.html'

    form_class=ItemForm


    def get(self,request,*args,**kwargs):

        search_text=request.GET.get("filter")

        form_instance=self.form_class

        qs=Item.objects.all()        

        return render(request,self.template_name,{"data":qs,"form":form_instance })
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            Item.objects.create(**data,receipt=request.user)

            return redirect("create_receipt")
        
        return render(request,self.template_name,{"form":form_instance})

