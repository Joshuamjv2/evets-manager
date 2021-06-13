from django.urls import path, re_path
from . import views
from .views import demo_views, ListViewDemo, DetailViewDemo, CreateViewDemo, UpdateViewDemo, DeleteViewDemo, MonthArchiveViewDemo


from .models import Event
from django.views.generic.dates import ArchiveIndexView



urlpatterns = [
    path('', views.home, name='home'),
    path('add_venue/', views.add_venue, name='add-venue'),
    # path('events/', views.all_events, name='show-events'),
    path('eventarchive/', ArchiveIndexView.as_view(model=Event, date_field="event_date", allow_future=True)),
    path('<int:year>/<int:month>/', MonthArchiveViewDemo.as_view(), name='event_montharchive'),
    path('events/', ListViewDemo.as_view(), name='show-events'),
    path('event/<int:pk>', DetailViewDemo.as_view(), name='event-detail'),
    path('event/add/', CreateViewDemo.as_view(), name='add-event'),
    path('event/update/<int:pk>', UpdateViewDemo.as_view(), name='update-event'),
    path('event/delete/<int:pk>', DeleteViewDemo.as_view(), name='delete-event'),
    path('gentext/', views.gen_text, name='gen-text-file'),
    path('gencsv/', views.gen_csv, name='gen-csv-file'),
    path('genpdf/', views.gen_pdf, name='gen-pdf-file'),
    path('getsubs/', views.list_subscribers, name='list-subscribers'),
    path('tdemo/', demo_views.template_demo, name='tdemo'),
    path('cdemo/', demo_views.context_demo, name='cdemo'),
    # path('file/', views.get_file, name='pdf_file'),
    # path('<int:year>/<str:month>/', views.home),
    re_path(r"^(?P<year>[0-9]{4})/(?P<month>0?[0-9]|1[0-2])/", views.home, name='home'),
]