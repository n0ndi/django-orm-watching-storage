from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_visit_duration, get_humans_in, format_time


def storage_information_view(request):
    non_closed_visits = []
    visits = Visit.objects.filter(leaved_at__isnull=True)
    for visit in visits:
        duration = format_time(get_visit_duration(visit))
        name = get_humans_in(visit)
        visit_params = {
            'who_entered': name,
            'entered_at': visit.entered_at,
            'duration': duration
        }
        non_closed_visits.append(visit_params)
    
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
