from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import csv
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from datetime import date
import calendar
from calendar import HTMLCalendar
from events.models import Event, Venue, MyClubUser
from events.forms import VenueForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request, year = date.today().year, month=date.today().month):
    # usr = request.user
    # ses = request.session
    # path = request.path
    # path_info = request.path_info
    # headers = request.headers
    # assert False
    # t = date.today()
    month = int(month)
    year = int(year)
    if year < 2000 or year > 2099: year = date.today().year
    month_name = calendar.month_name[month]
    title = f'MyClub Event Calendar - {month_name} {year}'
    cal = HTMLCalendar().formatmonth(year, month)
    # return HttpResponse('<h1>%s</h1>%s<p></p>' % (title, cal))
    announcements = [
        {'date':'6-10-2020', 'announcement':'This is the first day of the club'},
        {'date':'8-14-2020', 'announcement':'Club elections will be held'}
    ]
    context = {'title':title, 'cal':cal, 'announcements':announcements}
    return TemplateResponse(request, 'events/index.html', context)

def all_events(request):
    # usr = request.user
    # ses = request.session
    # path = request.path
    # path_info = request.path_info
    # headers = request.headers
    # assert False
    event_list = Event.objects.all()
    return render(request, 'events/event_list.html', {'event_list':event_list})

@login_required(login_url=reverse_lazy('login'))
def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue/?submitted=True')
    else:
        form = VenueForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html', {'form':form, 'submitted':submitted})

# def get_file(request):
#     return FileResponse(open('downloads/test.pdf', 'rb'))
def list_subscribers(request):
    p  = Paginator(MyClubUser.objects.all(), 3)
    page = request.GET.get('page')
    subscribers = p.get_page(page)
    return render(request, 'events/subscribers.html', {'subscribers':subscribers})

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

