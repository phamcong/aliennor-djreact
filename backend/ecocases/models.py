from django.db import models
import datetime
from django.utils import timezone
from django.forms import TextInput, Textarea
from django.core.files.storage import FileSystemStorage
from tinymce import models as tinymce_models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django import template
from django.utils.timezone import now
from ecocases.variables import *

# Create your models here.

register = template.Library()
default_user = User.objects.get(username='admin')


def make_upload_path(instance, filename):
    file_root, file_ext = os.path.splitext(filename)
    dir


class EcoCase(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)

    title = models.CharField(max_length=200)

    promise = tinymce_models.HTMLField()
    usage = tinymce_models.HTMLField()
    organization = tinymce_models.HTMLField()
    economic_transaction = tinymce_models.HTMLField(default='')

    reference = models.CharField(max_length=100, blank=True, null=True)
    direct_environmental_gain = models.NullBooleanField(null=True)
    indirect_environmental_gain = models.NullBooleanField(null=True)
    attractiveness_price = models.NullBooleanField(null=True)
    proven_cas_or_project = models.CharField(
        max_length=20, choices=case_type_choices, default='project')

    image_urls = models.CharField(
        max_length=2000, default='',  blank=True, null=True)
    images = models.FileField(upload_to='ecocases/',  blank=True, null=True)

    timestamp = models.DateTimeField(default=now, null=True)

    def __str__(self):
        return self.title

    def image_url_list(self):
        if self.image_urls != None:
            return self.image_urls.split(';')
        else:
            return ""

    def first_image_url(self):
        if self.image_urls != None:
            return self.image_urls.split(';')[0]
        else:
            return ""

    def get_absolute_url(self):
        return reverse('ecocases:detail', args=[str(self.id)])

    def get_short_title(self):
        if len(self.title) < 60:
            return self.title
        else:
            return (self.title[:60] + '..')


class ESM(models.Model):
    ecocase = models.ForeignKey(EcoCase, on_delete=models.CASCADE)
    type = models.IntegerField(default=1)

    def __str__(self):
        return esm_dict[str(self.type)]

    def get_title(self):
        return esm_dict[str(self.type)]

    def get_vote_point_total(self):
        vote_point_total = 0
        for vote in self.vote_set.all():
            vote_point_total += vote.vote_point
        return vote_point_total

    def vote_point_options(self):
        return vote_point_options


class Vote(models.Model):
    esm = models.ForeignKey(ESM, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=default_user.id)
    vote_point = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(16), MinValueValidator(0)]
    )

    def __str__(self):
        return 'ESM' + str(self.esm.type) + '_' + str(self.user) + ':' + str(self.vote_point)
