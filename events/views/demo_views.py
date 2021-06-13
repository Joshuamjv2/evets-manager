from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.base import TemplateView

from django.core.paginator import Paginator
from django.core import serializers
import io

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import csv

from django.template.response import TemplateResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, datetime


from events.models import Event, Venue, MyClubUser
from events.forms import EventForm


# from events.forms import VenueForm

from django.template import RequestContext, Template

class MonthArchiveViewDemo(MonthArchiveView):
    queryset = Event.events.all()
    date_field = "event_date"
    context_object_name = "event_list"
    allow_future = True
    month_format = '%m'

class ListViewDemo(ListView):
    model = Event
    context_object_name = 'all_events'

class DetailViewDemo(DetailView):
    model = Event
    context_object_name = 'event'

class TemplateViewDemo(TemplateView):
    template_name = 'events/cbv_demo.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Testing the template view demo"
        return context

class CreateViewDemo(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Event
    # fields = ['name', 'event_date', 'description']
    success_url = reverse_lazy('show-events')
    form_class = EventForm

class UpdateViewDemo(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Event
    # fields = fields = ['name', 'event_date', 'description']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('show-events')
    form_class = EventForm

class DeleteViewDemo(LoginRequiredMixin ,DeleteView):
    login_url = reverse_lazy('login')
    model = Event
    context_object_name = 'event'
    success_url = reverse_lazy('show-events')

def context_demo(request):
    template = Template('{{user}}<br>{{perms}}<br>{{request}}<br>{{messages}}')
    con = RequestContext(request)
    return HttpResponse(template.render(con))

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

def template_demo(request):
    empty_list = []
    color_list = ['red', 'green', 'yellow', 'blue']
    somevar = 5
    anothervar = 21
    today = datetime.now()
    past = datetime(1985, 11, 5)
    future = datetime(2035, 11, 5)
    best_bands = [
        {'name':'The Angels', 'country':'Australia'},
        {'name':'AC/CD', 'country':'Australia'},
        {'name':'Nirvana', 'country':'USA'},
        {'name':'The Offspring', 'country':'USA'},
        {'name':'Iron Maiden', 'country':'UK'},
        {'name':'Rammstein', 'country':'Germany'},
    ]
    aussie_bands = ['Australia', ['The Angels', 'AC/DC', 'The Living End']]
    venues_js = serializers.serialize('json', Venue.venues.all())
    context = {
        'somevar':somevar,
        'anothervar':anothervar,
        'empty_list':empty_list,
        'color_list':color_list,
        'best_bands':best_bands,
        'today':today,
        'past':past,
        'future':future,
        'aussie_bands':aussie_bands,
        'venues':venues_js
        }
    return render(request, 'events/template_demo.html', context)