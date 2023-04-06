from django.urls import path
from .views import *


urlpatterns = [
    path('<int:owner>/', calendar_view, name='calendar'),
    path('<int:owner>/<int:year>/<int:month>/', calendar_view, name='calendar_ym'),
    # path('save_note/', save_note_view, name='save_note'),
    # path('load_notes/', load_notes_view, name='load_notes'),
    # path('api/events/', events, name='events'),
    # path('api/add_event/', add_event, name='add_event'),
    # path('api/add_note/<int:event_id>/', add_note, name='add_note'),
]