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
from .models import Event, Venue, MyClubUser
from .forms import VenueForm

def gen_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="bart.txt"'
    lines = [
        "I will not expose the ignorance of the factory.\n",
        "I will not conduct my own fire drills.\n",
        "I will not prescribe the medication.\n"
    ]
    response.writelines(lines)
    return response

def gen_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venues.csv"'
    writer = csv.writer(response)
    venues = Venue.venues.all()
    writer.writerow(['Venue Name', 'Address', 'Phone', 'Email'])
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.email_address])
    return response

def gen_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica-Oblique", 14)
    lines = [
        "I will not expose the stupidity of your friends.\n",
        "I hate the way things are and I have to change my life for the best.\n",
        "I will be the best developer in the world one day.\n",
        "Companies will scramble for me.\n",
        "Then I will build my own company.\n",
        "And my company will build many people's lives.\n",
        "And I will be a happy man with a happy family.\n",
    ]
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='bart.pdf')


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