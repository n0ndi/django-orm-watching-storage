from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import format_time, is_visit_strange, get_visit_duration
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in visits:
        time = get_visit_duration(visit)
        this_passcard_visits.append(
            {
                'entered_at': visit.entered_at,
                'duration': format_time(time),
                'is_strange': is_visit_strange(time)
            }
        )
        
      
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
