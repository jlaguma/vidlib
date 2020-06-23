from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import urllib
import requests

from .models import Section, Video
from .forms import VideoForm, SearchForm

YOUTUBE_API_KEY = 'put_your_api_key_in_here'


def home(request):
    recent_sections = Section.objects.all().order_by('-id')[:3]
    return render(request, 'sections/home.html',
                  {'recent_sections': recent_sections})


@login_required
def dashboard(request):
    sections = Section.objects.filter(user=request.user)
    return render(request, 'sections/dashboard.html', {'sections': sections})


@login_required
def add_video(request, pk):
    form = VideoForm()
    search_form = SearchForm()
    section = Section.objects.get(pk=pk)
    if not section.user == request.user:
        raise Http404
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = Video()
            video.section = section
            video.url = form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(
                    f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ video_id[0] }&key={ YOUTUBE_API_KEY }'
                )
                json = response.json()
                title = json['items'][0]['snippet']['title']
                video.title = title
                video.save()
                return redirect('details_section', pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Needs to be a YouTube URL')

    return render(request, 'sections/add_video.html', {
        'form': form,
        'search_form': search_form,
        'section': section
    })


@login_required
def video_search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(
            search_form.cleaned_data['search_term'])
        response = requests.get(
            f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={ encoded_search_term }&key={ YOUTUBE_API_KEY }'
        )
        return JsonResponse(response.json())
    return JsonResponse({'error': 'Not able to validate form'})


class DeleteVideo(LoginRequiredMixin, generic.DeleteView):
    model = Video
    template_name = 'sections/delete_video.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.section.user == self.request.user:
            raise Http404
        return video


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get(
            'username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreateSection(LoginRequiredMixin, generic.CreateView):
    model = Section
    fields = ['title']
    template_name = 'sections/create_section.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateSection, self).form_valid(form)
        return redirect('dashboard')


class DetailSection(generic.DetailView):
    model = Section
    template_name = 'sections/details_section.html'


class UpdateSection(LoginRequiredMixin, generic.UpdateView):
    model = Section
    template_name = 'sections/update_section.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        section = super(UpdateSection, self).get_object()
        if not section.user == self.request.user:
            raise Http404
        return section


class DeleteSection(LoginRequiredMixin, generic.DeleteView):
    model = Section
    template_name = 'sections/delete_section.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        section = super(DeleteSection, self).get_object()
        if not section.user == self.request.user:
            raise Http404
        return section
