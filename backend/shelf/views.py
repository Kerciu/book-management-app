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


