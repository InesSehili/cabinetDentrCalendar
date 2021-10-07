from django.db import models
from django.urls import reverse
from rdvs.models import Rdv


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    rdv = models.ForeignKey(Rdv, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def get_html_url(self):
        if(self.rdv):
            url = reverse('modifier_rdv', args=(self.id,))
        else:
            url = reverse('cal:event_edit', args=(self.id,))


        

        return f'<a  href="{url}"> {self.title} </a>'
