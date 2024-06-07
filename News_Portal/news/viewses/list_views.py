from django.views.generic import ListView
from news.models import Post
from news.filters import NewsFilter
import pytz
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext as _


class PostList(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'news.html'
    context_object_name = 'post'
    paginate_by = 3

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timezones'] = pytz.all_timezones
        context['TIME_ZONE'] = timezone.get_current_timezone_name()
        context['current_time'] = timezone.localtime(timezone.now())
        current_time = timezone.localtime(timezone.now())
        context['time'] = _(current_time.strftime('%H:%M'))  # Локализация времени
        return context


class PostSearchList(ListView):
    model = Post
    ordering = '-published'
    template_name = 'news_search.html'
    context_object_name = 'post_search'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['total_post_search_count'] = self.filterset.qs.count()
        return context
