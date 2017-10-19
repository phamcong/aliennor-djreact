import os
import datetime
from django.utils.timezone import now
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import FormView
from django.template import loader
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from django.utils.decorators import method_decorator

from .models import EcoCase, ESM, Vote
from .forms import EcoCaseForm, LoginForm, SignupForm
from .mixins import FormUserNeededMixin, UserOwnerMixin
from ecocases.variables import *
import logging
import json

from pprint import pprint


uploaded_image_path = "../media/ecocases/"
# Create your views here.

esms = [
    "Innover par la création de valeur en prenant en compte l'ensemble des parties prenantes",
    'Innover par le biomimétisme',
    'Innover par la prise en compte des éco-usages et les utilisateurs finaux',
    "Innover par les services et l'économie de fonctionnalité",
    'Innover par de nouveaux modes de financement',
    'Innover par le bouclage de flux (matières, informations…)  et les circuits courts',
    'Innover par les matériaux et production',
    "Innover par la gestion du transfert d'impact et l'effet rebond"
]


class IndexView(generic.ListView):
    '''
        Display five lastest ecocases by pub_date.
    '''
    template_name = 'ecocases/index.html'
    context_object_name = 'ecocase_list'

    def get_queryset(self):
        """Return the last five added ecocase. """
        return EcoCase.objects.order_by('-timestamp')


class DetailView(generic.DetailView):
    '''
        Display ecocase by id
    '''
    model = EcoCase
    template_name = 'ecocases/detail.html'


class CreateView(FormUserNeededMixin, FormView):
    form_class = EcoCaseForm
    template_name = 'ecocases/create.html'
    success_url = reverse_lazy('ecocases:index')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        images = request.FILES.getlist('images')

        if form.is_valid():
            image_url_list = []

            for count, image in enumerate(images):
                uploaded_image = ecocase_image_fs.save(image.name, image)
                image_url_list.append(uploaded_image_path + uploaded_image)

            ecocase = EcoCase(title=form.cleaned_data['title'],
                              promise=form.cleaned_data['promise'],
                              usage=form.cleaned_data['usage'],
                              organization=form.cleaned_data['organization'],
                              economic_transaction=form.cleaned_data['economic_transaction'],
                              reference=form.cleaned_data['reference'],
                              direct_environmental_gain=form.cleaned_data['direct_environmental_gain'],
                              indirect_environmental_gain=form.cleaned_data['indirect_environmental_gain'],
                              proven_cas_or_project=form.cleaned_data['proven_cas_or_project'],
                              image_urls=';'.join(image_url_list),
                              timestamp=datetime.datetime.now(),
                              user=request.user,
                              )
            ecocase.save()

            for key, value in esm_dict.items():
                ecocase.esm_set.create(
                    type=key,
                )

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UpdateView(UserOwnerMixin, generic.UpdateView):
    queryset = EcoCase.objects.all()
    form_class = EcoCaseForm
    template_name = 'ecocases/update.html'
    # success_url = reverse_lazy('ecocases:index')

    def get_success_url(self, **kwargs):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        images = self.request.FILES.getlist('images')

        image_url_list = []
        for count, image in enumerate(images):
            print('image name: ', image.name)
            uploaded_image = ecocase_image_fs.save(image.name, image)
            image_url_list.append(uploaded_image_path + uploaded_image)

        self.object.image_urls = self.object.image_urls + \
            ';' + ';'.join(image_url_list)

        self.object.save()
        return HttpResponseRedirect(self.object.get_absolute_url())

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateView, self).dispatch(request, *args, **kwargs)


class DeleteView(generic.DeleteView):
    model = EcoCase
    template_name = 'ecocases/confirm_delete.html'
    success_url = reverse_lazy('ecocases:index')


def vote(request, id):
    ecocase = get_object_or_404(EcoCase, pk=id)
    user = request.user
    if(request.POST.get('vote_button')):
        if request.user.id != None:
            print("user:", request.user.id)
            for esm in ecocase.esm_set.all():
                votes = Vote.objects.filter(esm=esm, user=user)
                vote_point = int(request.POST.get(
                    'dropdown' + str(esm.id)))
                if votes.count() == 0:
                    esm.vote_set.create(
                        user=user,
                        vote_point=vote_point
                    )
                else:
                    vote = votes[0]
                    vote.vote_point = vote_point
                    vote.save()
                esm.save()
        return HttpResponseRedirect(reverse('ecocases:detail', args=(ecocase.id,)))
    else:
        return render(request, 'ecocases/vote.html', {
            'ecocase': ecocase,
            'error_message': "Something wrongs, please check your voting.",
        })


def profile(request, username):
    user = User.objects.get(username=username)
    ecocases = EcoCase.objects.filter(user=user)
    return render(request, 'user/profile.html',
                  {'username': username, 'ecocases': ecocases})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('ecocases:profile', args=(user.username, )))
    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('ecocases:index'))


def new_login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('ecocases:profile', args=(user.username, )))
    return render(request, 'login.html', {'form': form})


def new_logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('ecocases:index'))


def mechanism_list(request):
    return render(request, 'mechanisms/index.html', {'esm_dict': esm_dict, 'esm_link': esm_link})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'registration/activation_email_sent.html')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'registration/activation_email_checked.html')
    else:
        return render(request, 'registration/activation_link_invalid.html')


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "ecocases/upload_csv.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("ecocases:upload_csv"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (
                csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("ecocases:upload_csv"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            print('title:', fields[0])
            data_dict = {}
            data_dict["name"] = fields[0]
            data_dict["start_date_time"] = fields[1]
            data_dict["end_date_time"] = fields[2]
            data_dict["notes"] = fields[3]

            try:
                form = EventForm(data_dict)
                if form.is_valid():
                    form.save()
                else:
                    logging.getLogger("error_logger").error(
                        form.errors.as_json())
            except Exception as e:
                logging.getLogger("error_logger").error(form.errors.as_json())
                pass

    except Exception as e:
        logging.getLogger("error_logger").error(
            "Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("ecocases:upload_csv"))


def upload_json(request):
    data = {}
    if "GET" == request.method:
        return render(request, "ecocases/upload_json.html", data)
    # if not GET, then proceed
    try:
        print("upload successfully")
        json_file = request.FILES["json_file"]
        if not json_file.name.endswith('.json'):
            messages.error(request, 'File is not json type')
            return HttpResponseRedirect(reverse("ecocases:upload_json"))

        # if file is too large, return
        if json_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (
                json_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("ecocases:upload_json"))

        file_data = json.load(json_file)

        for obj in file_data:
            data_dict = {}
            data_dict["title"] = obj["title"]
            data_dict["promise"] = obj["promise"]
            data_dict["usage"] = obj["usage"]
            data_dict["organization"] = obj["organization"]
            data_dict["economic_transaction"] = obj["economic_transaction"]
            data_dict["timestamp"] = now

            try:
                form = EcoCaseForm(data_dict)
                if form.is_valid():
                    new_ecocase = form.save(commit=False)
                    new_ecocase.user = request.user
                    new_ecocase.save()

                    # add esm voting
                    for key, values in esm_dict.items():
                        print("new_case:", new_ecocase.id)
                        new_esm = ESM(ecocase=new_ecocase, type=int(key))

                        new_esm.save()
                        print("new_esm", new_esm.id)
                        if obj["esm" + str(key)] == "":
                            vote_point = 0
                        else:
                            vote_point = int(obj["esm" + str(key)])
                        new_vote = Vote(
                            user=request.user,
                            esm=new_esm,
                            vote_point=vote_point
                        )
                        print("new_vote:", new_vote.id)
                        new_vote.save()
                        print(new_vote)
                        new_esm.save()
                else:
                    logging.getLogger("error_logger").error(
                        form.errors.as_json())
            except Exception as e:
                logging.getLogger("error_logger").error(form.errors.as_json())
                pass

    except Exception as e:
        logging.getLogger("error_logger").error(
            "Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("ecocases:index"))
