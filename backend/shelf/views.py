from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Shelf


class ShelfBaseView(LoginRequiredMixin):
    model = Shelf
    succes_url = reverse_lazy('shelf-list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ShelfListView(ShelfBaseView, ListView):
    template_name = 'shelves/list.html'
    context_object_name = 'shelves'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shelves = self.get_queryset()
        context['default_shelves'] = shelves.filter(is_default=True)
        context['custom_shelves'] = shelves.filter(is_default=False)
        return context


