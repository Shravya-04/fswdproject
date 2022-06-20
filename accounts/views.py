from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa



import mysql.connector
mydb =mysql.connector.connect(host='localhost',user='root',passwd='Maggie@2025',database='donate',autocommit=True)
cursor=mydb.cursor()


# Create your views here.'
def account(request):
    return render(request,'home.html')

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            print("Logged in")
            return redirect('/homlogin')
        else: 
            return HttpResponse("Wrong Username/password")
            # return render(request,'login.html')    
    else: 
          return render(request,'login.html')

def signup(request):
    if request.method=="POST":
        firstName = request.POST['firstName']
        lastName= request.POST['lastName']
        username= request.POST['username']
        email= request.POST['email']
        password= request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password, first_name=firstName, last_name=lastName)
        print("User created")
        return redirect('/')
    else:    
        return render(request,'signup.html')   

def donate(request):
    if request.method=="POST":
         fullname= request.POST['fullname']
         nickname= request.POST['nickname']
         email= request.POST['email']
         date=request.POST['date']
         month=request.POST['month']
         year=request.POST['year']
         cursor.execute("insert into donate1(fullname,nickname,email,date,month,year)values(%s,%s,%s,%s,%s,%s)",(fullname,nickname,email,date,month,year,))
         return redirect('pdf_view')
    else:
         return render(request,'donate.html')
def pledge(request):
    if request.method=="POST":
        return redirect('/homlogin')
    else:    
        return render(request,'pledge.html')
def connect(request):
    return render(request,'chatbox.html')
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

cursor.execute("select *from donate1 where fullname='%s'")
x=cursor.fetchone()
data = {
	"fullname":x,

	}

#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('accounts/pdf_templates.html', data)
		return HttpResponse(pdf, content_type='application/pdf')    