from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from .models import Hall, Video
from django.contrib.auth import authenticate, login
from .forms import VideoForm, SearchForm
from django.forms import formset_factory
import urllib
from django.forms.utils import ErrorList

YOUTUBE_API_KEY = 'AIzaSyDlGDPW5nhKL07Y--Z3-zCi1asdP7XXcws'

# Create your views here.



def home(request):
    return render(request, 'halls/home.html', {})


def dashboard(request):
    return render(request, 'halls/dashboard.html', {})


def add_video(request, pk):

    form = VideoForm()
    search_form = SearchForm()
    hall = Hall.objects.get(pk=pk)
    if not hall.user == request.user:
        raise Http404

    if request.method == 'POST':
        filed_form = VideoForm(request.POST)
        if filed_form.is_valid():
            video = Video()
            video.hall = hall
            video.url = filed_form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:

                video.title =
                video.youtube_id = video_id[0]


                video.save()


    return render(request, 'halls/add_video.html', {'form': form, 'search_form': search_form, 'hall': hall})






class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view



#def create_hall(request):

class CreateHall(CreateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateHall, self).form_valid(form)
        return redirect('home')



class DetailHall(DetailView):
    model = Hall
    template_name = 'halls/detail_hall.html'


class UpdateHall(UpdateView):
    model = Hall
    template_name = 'halls/update_hall.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')


class DeleteHall(DeleteView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    success_url = reverse_lazy('dashboard')





