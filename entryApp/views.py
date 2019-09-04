# from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.contrib import messages 
from django.shortcuts import render, redirect, get_object_or_404
# from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login

from django.http import HttpResponse
from django.template import loader
from django.views.generic import View

# from django.template.loader import get_template
# from django.http import HttpResponse
import datetime

# from django.contrib.auth.decorators import user_passes_test

from django.views.generic import View

# from Entries.utils import render_to_pdf 

# from django.template.loader import get_template

from entryApp.forms import UserCreationForm, ChangeForm
from entryApp.models import Profile
# from .pdfUtils import render_to_pdf

from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string

from weasyprint import HTML


import csv
from django.http import HttpResponse

def html_to_csv_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="entries.csv"'
    profile = Profile.objects.all()
    template = loader.get_template('record.html')
    response.write(template.render({'profile': profile}))
    return response



def html_to_pdf_view(request):
	profile = Profile.objects.all()
	html_string = render_to_string('record.html', {'profile': profile})
	html = HTML(string=html_string)
	html.write_pdf(target='/tmp/entries.pdf');
	fs = FileSystemStorage('/tmp')
	with fs.open('entries.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="entries.pdf"'
		return response
	return response
    


def welcome_page(request):
	if request.user.is_authenticated:
		title = 'Welcome'
		queryset = Profile.objects.all()

	else:

		title = 'Unauthenticated User'
		queryset = Profile.objects.all()

	context = {
		"title": title,
		"queryset": queryset,
	}
	return render(request, 'welcome.html', context)



def home_page_home(request):

	if request.method == "POST":
		form = UserCreationForm(request.POST or None)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.save()
			username = request.POST['username']
			password = request.POST['password1']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				url = redirect('welcome')
				return url
	else:
		form = UserCreationForm()
	context = {
		"form": form,
	}
	return render(request, 'home.html', context)

def update_record(request, id):
	instance = get_object_or_404(Profile, id=id)
	template_name = 'update_record.html'
	form = ChangeForm(request.POST or None, instance=instance)
	if request.method == 'POST':
		if form.is_valid():
			form = form.save(commit=False)
			form.save()
			messages.success(request, "Successfully updated", fail_silently=True)
			return redirect('super')
	context = {
		"instance": instance,
		"form": form,
	}
	return render(request, template_name, context)


def delete_record(request, id):
	
	instance = get_object_or_404(Profile, id=id)
	instance.delete()
	title = 'Delete User'
	messages.success(request, "Successfully deleted", fail_silently=True)
	return redirect('super')
	
	# context = {
	# 	"instance": instance,
	# }
	
	# return render(request, 'delete_record.html', context)


from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def admin_function(request):
	title = 'EDIT, DELETE, VIEW RECORD'
	# template = get_template('record.html')

	queryset = Profile.objects.all()
	paginator = Paginator(queryset, 10)

	page = request.GET.get('page')

	try:
		profile = paginator.page(page)
	except PageNotAnInteger:
		profile = paginator.page(1)
	except EmptyPage:
		profile = paginator.page(paginator.num_pages)

	context = {
		"title": title,
		"queryset": queryset,
		"profile": profile
	}

	return render(request, 'record.html', context)

@staff_member_required
def super_admin_list(request):
	title = 'EDIT, DELETE AND VIEW RECORDS'
	queryset = Profile.objects.all()
	paginator = Paginator(queryset, 10)

	page = request.GET.get('page')

	try:
		profile = paginator.page(page)
	except PageNotAnInteger:
		profile = paginator.page(1)
	except EmptyPage:
		profile = paginator.page(paginator.num_pages)

	context = {
		"title": title,
		"queryset": queryset,
		"profile": profile,
	}

	return render(request, 'super_admin_list.html', context)

def record_detail(request, id):
	instance = get_object_or_404(Profile, id=id)
	title = "USER DETAILS"
	template_name = 'record_detail.html'
	context = {
		"instance": instance,
		"title": title,
	}

	return render(request, template_name, context)


# def get_pdf(request):
# 	results = Profile.objects.all()
#     #Retrieve data or whatever you need
# 	return render_to_pdf(
# 		'pdf.html',
#         {
#             # 'pagesize':'A5',
#             'mylist': results,
#         }
#     )

   
# def pdf_download(request):
#     data = dict()
#     data["name"] = "Data Entries"
#     data["DOB"] = "As it stands {}".format(datetime.datetime.now())

#     template = get_template("super_admin_list.html")
#     html = template.render(data)
#     pdf = pdfkit.from_string(html, False)

#     filename = "Entries.pdf"

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
#     return response


# class GeneratePDF(View):

# 	def get(self, request, *args, **kwargs):

# 		results = Profile.objects.all()
# 		template = get_template('super_admin_list.html')
# 		context = {
# 			"results": results
# 		}

# 		pdf = render_to_pdf('super_admin_list.html', context)

# 		if pdf:

# 			response = HttpResponse(pdf, content_type='application/pdf')
# 			filename = "Entries_%s.pdf" %("12341231")
# 			content = "inline; filename='%s'" %(filename)
# 			download = request.GET.get("download")

# 			if download:

# 				content = "attachment; filename='%s'" %(filename)

# 			response['Content-Disposition'] = content
# 			return response

# 		return HttpResponse("Not found")














