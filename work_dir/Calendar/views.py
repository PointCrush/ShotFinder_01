import datetime
import calendar

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Calendar.forms import EventForm
from .models import Event


@login_required
def calendar_view(request, owner,  year=None, month=None):
    event_list = Event.objects.filter(owner=owner)

    date_day_list = []
    date_free_day_list = []
    for event in event_list:
        event_date = event.date
        if event_date not in date_day_list and event_date.year == year \
                and event_date.month == month and event.event:

            date_day_list.append(event_date.day)

        elif event_date not in date_free_day_list and event_date.year == year \
                and event_date.month == month and not event.event:

            date_free_day_list.append(event_date.day)

    if not year or not month:
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        return redirect('calendar_ym', owner=owner, year=year, month=month)
    else:
        year = int(year)
        month = int(month)

    if request.method == 'POST':
        date_value = request.POST.get('date')
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.owner = request.user
            event.date = date_value
            event.save()
            return redirect('calendar_ym', owner=owner, year=year, month=month)
    else:
        event_form = EventForm()

    weeks = calendar.monthcalendar(year, month)
    previous_month = datetime.date(year, month, 1) - datetime.timedelta(days=1)
    last_day_of_month = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    next_month = last_day_of_month + datetime.timedelta(days=1)
    next_year = year + 1
    previous_year = year - 1

    month_name = calendar.month_name[month]

    context = {
        'weeks': weeks,
        'month_name': month_name,
        'year': year,
        'next_year': next_year,
        'previous_year': previous_year,
        'month': month,
        'previous_month': previous_month.month,
        'next_month': next_month.month,
        'event_form': event_form,
        'event_list': event_list,
        'date_day_list': date_day_list,
        'date_free_day_list': date_free_day_list,
        'owner': owner,
    }
    return render(request, 'calendar.html', context)
