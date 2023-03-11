from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )



def get_visit_duration(visit):
    leaved_at = timezone.localtime(visit.leaved_at)
    entered = visit.entered_at
    delta = leaved_at - entered
    return delta

def is_visit_strange(delta):
    return delta.total_seconds() > 3600

def format_time(delta):
    return (f"{int(delta.total_seconds()  // 3600)}:{int((delta.total_seconds()  % 3600) // 60)}:{int(delta.total_seconds() % 60)}")

def get_humans_in(visit):
    return visit.passcard.owner_name