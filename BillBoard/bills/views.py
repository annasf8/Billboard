from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from .models import Bill, Click
from .forms import ClickForm, BillForm
from .filters import BillFilter
from django.views.generic.edit import FormMixin


class BillList(ListView):
    model = Bill
    ordering = '-time_create'
    template_name = 'bills.html'
    context_object_name = 'bills'


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = BillFilter(self.request.GET, queryset)
        return self.filterset.qs

    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    # Добавляем в контекст объект фильтрации.
    #    context['filterset'] = self.filterset
    #    return context

class BillDetail(FormMixin, DetailView):
    model = Bill
    template_name = 'bill.html'
    form_class = BillForm
    context_object_name = 'bill'

    def get_success_url(self):
        return reverse('bill', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        comments = Click.objects.filter(accepted=True, bill_id=self.kwargs['pk']).order_by('time_create')
        context['comments'] = comments

        return context

    def send(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            bill = form.save(commit=False)
            bill.click = self.object
            bill.user = self.request.user
            bill.send_notification_email()
            bill.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class BillDetailUser(LoginRequiredMixin, DetailView):
    model = Bill
    template_name = 'bill_user.html'
    context_object_name = 'bill_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Click.objects.filter(accepted=True, bill_id=self.kwargs['pk']).order_by('time_create')
        context['comments'] = comments

        return context

class BillCreate(LoginRequiredMixin, CreateView):
    model = Bill
    form_class = BillForm
    template_name = 'bill_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        current_user = self.request.user
        self.object.user = current_user
        return super().form_valid(form)

class BillUpdate(LoginRequiredMixin, UpdateView):
    form_class = BillForm
    model = Bill
    template_name = 'bill_edit.html'
    success_url = reverse_lazy('user_bills')

class BillDelete(LoginRequiredMixin, DeleteView):
    model = Bill
    template_name = 'bill_delete.html'
    success_url = reverse_lazy('user_bills')

class ClickList(ListView):
    model = Click
    template_name = 'clicks.html'
    ordering = '-time_create'
    context_object_name = 'clicks'

class ClickDetail(DetailView):
    model = Click
    template_name = 'click.html'
    context_object_name = 'click'

class ClickCreate(LoginRequiredMixin, CreateView):
    model = Click
    form_class = ClickForm
    template_name = 'click_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.bill = Bill.objects.get(pk=self.kwargs['pk'])
        current_user = self.request.user
        self.object.user = current_user
        return super().form_valid(form)


class ClickDelete(LoginRequiredMixin, DeleteView):
    model = Click
    template_name = 'click_delete.html'
    success_url = reverse_lazy('user_clicks')

@login_required
def user_bills(request):
    current_user = request.user
    bills = Bill.objects.filter(user=current_user).order_by('-time_create')
    return render(request, 'user_bills.html', {'bills': bills})


@login_required
def user_clicks(request):
    current_user = request.user
    bills = Bill.objects.filter(user=current_user).order_by('-time_create')
    selected_bill_id = request.GET.get('bill')

    clicks = Click.objects.filter(bill__user = current_user).order_by('-time_create')
    if selected_bill_id:
        clicks = clicks.filter(bill__id=selected_bill_id)

    if request.method == 'GET':
        selected_bill_id = request.GET.get('bill')
        if selected_bill_id:
            bills = bills.filter(bill__id=selected_bill_id)

    return render(request, 'user_bills.html', {'bills': bills, 'clicks': clicks, 'selected_bill_id': selected_bill_id})


@login_required
def accept_click(request, pk):
    click = get_object_or_404(Click, pk=pk)
    click.accepted = True
    click.save()
    click.send_accepted_email()
    return HttpResponseRedirect(reverse('user_clicks'))

# Create your views here.
