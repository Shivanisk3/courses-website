from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from users.forms import add_course_form, add_content_form
from users.models import Section, register_table, add_course, cart, Order, Content
from django.db.models import Q
from datetime import datetime
from django.core.mail import EmailMessage
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

def home(request):
	context = {}
	all_courses = add_course.objects.all()
	context["courses"] = all_courses
	top = [1,2,3,4]
	context["top"] = top
	if "user_id" in request.COOKIES:
		uid = request.COOKIES["user_id"]
		usr = get_object_or_404(User,id=uid)
		login(request,usr)
		if usr.is_active:
			return HttpResponseRedirect("/profile")
	if request.method == "POST":
		pass
	#em = EmailMessage("Greetings","Hello everyone", to=["email@gmail.com"])
	#em.send()
		#un = request.POST["username"]
		#em = request.POST["email_address"]
		#pw = request.POST["password"]
		#print("username=" + un,em,pw)

		#data = Reg(username=un,email_address=em,password=pw)
		#data.save()
		#return render(request, "users/section.html")
		#if data.is_valid():
		#	data.save()
		#	return render(request, "users/section.html")
	#	if data.is_valid():
	#		data.save()
	#		res = "thank you {}".format(un)
	#	    return render(request,"users/section.html",{"status":res})
	#	    return HttpResponse("<h1 style='color:green;'>Dear {} Data Saved Successfully!</h1>".format(un))
	#	username = request.POST.get('username')
	#	email_address = request.POST.get('email_address')
	#	form = RegForm(username=username,email_address=email_address)
	#	form = RegForm(request.POST)
	#	if form.is_valid():
	#		form.save()
	#		return redirect('home')
		#form = RegForm(request.POST)
	    #if form.is_valid():
	    #    form.save()
		#    return redirect('home')
	#	models.form.objects.create(
	#	username = request.POST.get['username'],
	#	email_address = request.POST.get['email_address']
	#	)
	#	print(username)

	#	return redirect('home')
	#	form = RegForm(request.POST)
	#	if form.is_valid():
	#		form.save()
	#		email = form.cleaned_data.get('email_address')
	#		messages.success(request, f'Hi {email}, account created')
	#		return redirect('home')
	
	#else:
	#	form = RegForm()
	#data = register_table.objects.get(user__id=request.user.id)	
	return render(request, 'users/home.html',context)


def register(request):
	if request.method == "POST":
	    form = UserRegisterForm(request.POST)
	    #con = request.POST["contact"]
	    #print(con)
	    if form.is_valid():
	    	user = form.save()
	    	user.refresh_from_db()
	    	user.register_table.contact_number = form.cleaned_data.get('contact_number')
	    	user.save()
	    	#usr = User.objects.create_user()
	    	#last_name = form.cleaned_data.get('last_name')
	    	#reg = register_table(user=usr, contact_number=con)
	    	#reg.save()
	    	username = form.cleaned_data.get('username')
	    	messages.success(request, f'Hi {username}, your account was created successfully')
	    	return redirect('home')
	else:
	    form = UserRegisterForm()
	return render(request, 'users/register.html', {'form':form})


def user_login(request):
	if request.method=="POST":
		un = request.POST["username"]
		pwd = request.POST["password"]
		print(un,pwd)
		user = authenticate(username=un,password=pwd)
		
		if user:
			login(request,user)
			if user.is_superuser:
				return HttpResponseRedirect("/admin")
			#if user.is_staff:
			#	return HttpResponseRedirect("/tutor_profile")
			#if user.is_active:
			else:
				res = HttpResponseRedirect("/")
				if "rememberme" in request.POST:
					res.set_cookie("user_id",user.id)
					res.set_cookie("date_login",datetime.now())
				return res

		else:
			return render(request,'users/login.html')
	return render(request,'users/login.html')

@login_required
def user_logout(request):
	logout(request)
	res = HttpResponseRedirect("/")
	res.delete_cookie("user_id")
	res.delete_cookie("date_login")
	return res


#@staff_member_required
#def tut_profile(request):
#	return HttpResponse("<h1>hi tutor</h1>")

@login_required()
def profile(request):

	#if User.is_superuser:
	#	return HttpResponseRedirect("/admin")
	#elif User.is_staff:
	#	return HttpResponse("<h1>Welcome tutor</h1>")
	context = {}
	ch = register_table.objects.filter(user__id=request.user.id)
	if len(ch)>0:
		data = register_table.objects.get(user__id=request.user.id)
		context["data"] = data
	return render(request, 'users/profile.html',context)
	#return HttpResponse("called")

@login_required()
def tut_profile(request):
	return render(request, 'users/tut_profile.html')

def edit_profile(request):
	context = {}
	try:
		data = register_table.objects.get(user__id=request.user.id)
	except register_table.DoesNotExist:
		data = None
	context["data"]=data
	if request.method=="POST":
		fn = request.POST["fname"]
		ln = request.POST["lname"]
		em = request.POST["email"]
		con = request.POST["contact"]
		occ = request.POST["occ"]
		abt = request.POST["about"]

		usr = User.objects.get(id=request.user.id)
		usr.first_name = fn
		usr.last_name = ln
		usr.email = em
		usr.save()

		data.contact_number = con
		data.occupation = occ
		data.about = abt
		data.save()

		if "image" in request.FILES:
			img = request.FILES["image"]
			data.profile_pic = img
			data.save()

		context["status"] = "Changes Saved Successfully"
	return render(request,"users/edit_profile.html",context)

def all_sections(request):
	context = {}
	all_courses = add_course.objects.all()
	context["courses"] = all_courses
	secs = Section.objects.all()
	context["section"] = secs
	top = [1,2,3,4]
	context["top"] = top
	return render(request, 'users/section.html',context)

def course(request):
	return render(request, 'users/coursepage.html')

def change_password(request):
	context={}
	ch = register_table.objects.filter(user__id=request.user.id)
	if len(ch)>0:
		data = register_table.objects.get(user__id=request.user.id)
		context["data"] = data
	if request.method=="POST":
		current = request.POST["cpwd"]
		new_pas = request.POST["npwd"]

		user = User.objects.get(id=request.user.id)
		un = user.username
		check = user.check_password(current)
		if check==True:
			user.set_password(new_pas)
			user.save()
			context["msz"] = "Password Changed Successfully!"
			context["col"] = "alert-success"
			user = User.objects.get(username=un)
			login(request,user)
		else:
			context["msz"] = "Incorrect Current Password"
			context["col"] = "alert-danger"
	return render(request,"users/change_password.html",context)

def add_course_view(request):
	context={}
	ch = register_table.objects.filter(user__id=request.user.id)
	if len(ch)>0:
		data = register_table.objects.get(user__id=request.user.id)
		context["data"] = data
	form = add_course_form()
	if request.method == "POST":
		form = add_course_form(request.POST,request.FILES)
		if form.is_valid():
			data = form.save(commit=False)
			login_user = User.objects.get(username=request.user.username)
			data.tutor = login_user
			data.save()
			context["status"] = "{} added successfully".format(data.course_name)
	context["form"] = form
	return render(request,"users/add_course.html",context)

def my_courses(request):
	context = {}
	ch = register_table.objects.filter(user__id=request.user.id)
	if len(ch)>0:
		data = register_table.objects.get(user__id=request.user.id)
		context["data"] = data
	all = add_course.objects.filter(tutor__id=request.user.id)
	context["courses"] = all
	return render(request,"users/my_courses.html",context)

def single_course(request):
	context = {}
	id = request.GET["pid"]
	obj = add_course.objects.get(id=id)
	context["course"] = obj

	cont = Content.objects.filter(course__id=id).order_by("module_no","chapter_no")
	conten = Content.objects.filter(course__id=id).order_by("chapter_no")
	mod = Content.objects.filter(course__id=id).order_by("module_no").values("module_no").distinct()
	#mod2 = Content.objects.filter(course__id=id).values("module_no").annotate(dcount=Count("module_no")).order_by("module_no")
	#print(mod2)
	cont1 = Content.objects.filter(Q(course__id=id)&Q(module_no=1)).order_by("chapter_no")
	context["content"] = cont
	context["modules"] = cont1
	mods = len(mod)
	context["some"] = mod
	return render(request,"users/single_course.html",context)

def update_course(request):
	context = {}
	secs = Section.objects.all().order_by("sec_name")
	context["section"] = secs

	pid = request.GET["pid"]
	course = get_object_or_404(add_course,id=pid)
	context["course"] = course

	if request.method=="POST":
		pn = request.POST["pname"]
		ct_id = request.POST["pcat"]
		pr = request.POST["pp"]
		sp = request.POST["sp"]
		des = request.POST["des"]

		sec_obj = Section.objects.get(id=ct_id)

		course.course_name =pn
		course.course_section =sec_obj
		course.course_price =pr
		course.sale_price =sp
		course.details =des
		if "pimg" in request.FILES:
			img = request.FILES["pimg"]
			course.course_image = img
		course.save()
		context["status"] = "Changes saved successfully"
		context["id"] = pid

	return render(request,"users/update_course.html",context)

def delete_course(request):
	context={}
	if "pid" in request.GET:
		pid = request.GET["pid"]
		prd = get_object_or_404(add_course, id=pid)
		context["course"] = prd

		if "action" in request.GET:
			prd.delete()
			context["status"] = str(prd.course_name)+" deleted successfully"
	return render(request,"users/delete_course.html",context)


def all_courses(request):
	context = {}
	all_courses = add_course.objects.all().order_by("course_name")
	context["courses"] = all_courses

	if "qry" in request.GET:
		q = request.GET["qry"]
		#p = request.GET["price"]
		prd = add_course.objects.filter(Q(course_name__contains=q)|Q(course_section__sec_name__contains=q))
		#prd = add_course.objects.filter(Q(course_name__icontains=q)&Q(sale_price__lt=p))
		context["courses"] = prd
		context["abcd"] = "search"

	if "sec" in request.GET:
		cid = request.GET["sec"]
		prd = add_course.objects.filter(course_section__id=cid)
		context["courses"] = prd
		context["abcd"] = "search"

	return render(request,"users/all_courses.html",context)

def add_to_cart(request):
	context={}
	ch = register_table.objects.filter(user__id=request.user.id)
	if len(ch)>0:
		data = register_table.objects.get(user__id=request.user.id)
		context["data"] = data
	items = cart.objects.filter(user__id=request.user.id,status=False)
	context["items"] = items
	if request.user.is_authenticated:
		if request.method=="POST":
			pid = request.POST["pid"]
			is_exist = cart.objects.filter(course__id=pid,user__id=request.user.id,status=False)
			if len(is_exist)>0:
				context["msz"] = "Item already exists in your cart"
				context["cls"] = "alert alert-warning"
			else:
				course = get_object_or_404(add_course,id=pid)
				usr = get_object_or_404(User,id=request.user.id)
				c = cart(user=usr,course=course)
				c.save()
				context["msz"] = "{} added in your cart".format(course.course_name)
				context["cls"] = "alert alert-success"


	else:
		context["status"] = "Please Login to view your cart"
	return render(request,"users/cart.html",context)

def get_cart_data(request):
	items = cart.objects.filter(user__id=request.user.id, status=False)
	sale,total=0,0
	for i in items:
		sale += float(i.course.sale_price)
		total += float(i.course.course_price)

	res = {
	     "total":total, "offer":sale,
	}
	return JsonResponse(res)

def del_cart(request):
	if "delete_cart" in request.GET:
		id = request.GET["delete_cart"]
		cart_obj = get_object_or_404(cart,id=id)
		cart_obj.delete()
		return HttpResponse(1)


def process_payment(request):
	items = cart.objects.filter(user_id__id=request.user.id,status=False)
	courses =""
	amt=0
	inv = "INV-"
	cart_ids = ""
	p_ids = ""
	for j in items:
		courses += str(j.course.course_name)+"\n"
		p_ids += str(j.course.id)+","
		amt += float(j.course.sale_price)
		inv += str(j.id)
		cart_ids += str(j.id)+","
	paypal_dict = {
	'business': settings.PAYPAL_RECEIVER_EMAIL,
	'amount': str(amt),
	'item_name': courses,
	'invoice': inv,
	'notify_url': 'http://{}{}'.format("127.0.0.1:8000", reverse('paypal-ipn')),
	'return_url': 'http://{}{}'.format("127.0.0.1:8000",reverse('payment_done')),
	'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",reverse('payment_cancelled')),

	}
	usr = User.objects.get(username=request.user.username)
	ordr = Order(cust_id=usr,cart_ids=cart_ids,course_ids=p_ids)
	ordr.save()
	ordr.invoice_id = str(ordr.id)+inv
	ordr.save()
	request.session["order_id"] = ordr.id

	form = PayPalPaymentsForm(initial=paypal_dict)
	return render(request, 'users/process_payment.html', {'form': form})

def payment_done(request):
	if "order_id" in request.session:
		order_id = request.session["order_id"]
		ord_obj = get_object_or_404(Order,id=order_id)
		ord_obj.status = True
		ord_obj.save()

		for i in ord_obj.cart_ids.split(",")[:-1]:
			#print(i)
			cart_object = cart.objects.get(id=i)
			cart_object.status = True
			cart_object.save()
	return render(request,"users/payment_success.html")

def payment_cancelled(request):
	return render(request,"users/payment_failed.html")

def order_history(request):
	context = {}
	ch = register_table.objects.filter(user__id=request.user.id)
	if len(ch)>0:
		data = register_table.objects.get(user__id=request.user.id)
		context["data"] = data

	all_orders = []
	orders = Order.objects.filter(cust_id__id=request.user.id).order_by("-id")
	#for i in orders:
	#	print(i.cart_ids)
	for order in orders:
		courses = []
		for id in order.course_ids.split(",")[:-1]:
			crs = get_object_or_404(add_course, id=id)
			courses.append(crs)
		ordr = {
		"order_id":order.id,
		"courses":courses,
		"invoice":order.invoice_id,
		"status":order.status,
		"date":order.processed_on,
		}
		all_orders.append(ordr)
	context["order_history"] = all_orders

	return render(request,"users/order_history.html",context)



def add_content_view(request):
	context={}
	ch = register_table.objects.filter(user__id=request.user.id)
	if len(ch)>0:
		data = register_table.objects.get(user__id=request.user.id)
		context["data"] = data
	id = request.GET["pid"]
	obj = add_course.objects.get(id=id)
	context["course"] = obj
	print(obj)
	form = add_content_form()
	if request.method == "POST":
		form = add_content_form(request.POST,request.FILES)
		if form.is_valid():
			data = form.save(commit=False)
			login_user = User.objects.get(username=request.user.username)
			data.tutor = login_user
			data.course = obj
			data.save()
			context["status"] = "added successfully"
	context["form"] = form
	return render(request,"users/add_content.html",context)


def content_view(request):
	context = {}
	id = request.GET["pid"]
	obj = add_course.objects.get(id=id)
	context["course"] = obj
	ch = register_table.objects.filter(user__id=request.user.id)
	if len(ch)>0:
		data = register_table.objects.get(user__id=request.user.id)
		context["data"] = data
	form = add_content_form()
	if request.method == "POST":
		form = add_content_form(request.POST,request.FILES)
		if form.is_valid():
			data = form.save(commit=False)
			login_user = User.objects.get(username=request.user.username)
			data.tutor = login_user
			data.course = obj
			data.save()
			context["status"] = "added successfully"
	context["form"] = form
	
	cont = Content.objects.filter(course__id=id).order_by("module_no","chapter_no")
	conten = Content.objects.filter(course__id=id).order_by("chapter_no")
	mod = Content.objects.filter(course__id=id).order_by("module_no").values("module_no").distinct()
	#mod2 = Content.objects.filter(course__id=id).values("module_no").annotate(dcount=Count("module_no")).order_by("module_no")
	#print(mod2)
	cont1 = Content.objects.filter(Q(course__id=id)&Q(module_no=1)).order_by("chapter_no")
	context["content"] = cont
	context["modules"] = cont1
	mods = len(mod)
	context["some"] = mod
	for co in cont:
		print(co.module_no)
		print(co.tutor.id)
		#tut = int(co.tutor.id)
	obj2 = add_course.objects.filter(id=id)
	for cors in obj2:
		print(cors.tutor.id)
		tut = cors.tutor.id
	context["tut"] = tut
	return render(request,"users/content.html",context)


def del_content(request):
	if "delete_content" in request.GET:
		id = request.GET["delete_content"]
		cont_obj = get_object_or_404(Content,id=id)
		cont_obj.delete()
		return HttpResponse(1)

def workshops(request):
	return render(request, 'users/workshop.html')

def about(request):
	return render(request, 'users/about.html')
