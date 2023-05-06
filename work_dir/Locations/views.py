from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_filters.views import FilterView

from Locations.filters import LocationFilter
from Locations.forms import *
from Locations.models import Location, LocationImage


# Create your views here.


class AllLocationList(FilterView):
    model = Location
    template_name = 'Locations/template/locations_list.html'
    filterset_class = LocationFilter
    extra_context = {
    }


@verified_email_required
def locations_detail(request, loc_pk):
    location = Location.objects.get(pk=loc_pk)
    context = {
        'location': location,
    }
    return render(request, 'Locations/template/location_detail.html', context)


@verified_email_required
def create_location(request):
    if request.method == 'POST':
        create_form = LocationCreationForm(request.POST)
        if create_form.is_valid():
            location = create_form.save(commit=False)
            location.owner = request.user
            location.save()
            return redirect('upload_image_location', loc_pk=location.pk)
    else:
        create_form = LocationCreationForm()
    context = {
        'create_form': create_form,
    }
    return render(request, 'Locations/template/create_form.html', context)


@verified_email_required
def upload_image_location(request, loc_pk):
    location = Location.objects.get(pk=loc_pk)
    if request.method == 'POST':
        upload_form = UploadImageForm(request.POST, request.FILES)
        if upload_form.is_valid():
            images = request.FILES.getlist('images')
            for image in images:
                LocationImage.objects.create(location=location,
                                             image=image)
            return redirect('locations_detail', loc_pk=loc_pk)
    else:
        upload_form = UploadImageForm()
    context = {
        'upload_form': upload_form,
    }
    return render(request, 'Locations/template/upload_image_form.html', context)


@verified_email_required
def edit_location(request, loc_pk):
    model = Location.objects.get(pk=loc_pk)
    if model.owner == request.user:
        if request.method == 'POST':
            form = LocationCreationForm(request.POST, instance=model)
            if form.is_valid():
                form.save()
                return redirect('locations_detail', loc_pk=loc_pk)
        else:
            form = LocationCreationForm(instance=model)
        return render(request, 'Photographers/templates/edit_ph.html', {'form': form})
    else:
        return render(request, 'data_dir/template/access_error.html')


def delete_location(request, loc_pk):
    location = Location.objects.get(pk=loc_pk)
    if request.user == location.owner:
        location.delete()
        return redirect('all_locations')
    else:
        return render('data_dir/template/access_error.html')


def my_locations(request):
    locations = Location.objects.filter(owner=request.user)
    return render(request, 'Locations/template/my_locations.html', {'locations': locations})
