from django.shortcuts import render , redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , UpdateView, DeleteView , FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import task
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task')


class RegisterUser(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterUser,self).form_valid(form)

    def get(self, *arg , **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterUser,self).get(*args, **kwargs) 

class Tasklist(LoginRequiredMixin,ListView):
    model = task
    context_object_name = 'TitleTask'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['TitleTask'] = context['TitleTask'].filter(user=self.request.user)
        context['count'] = context['TitleTask'].filter(complete=False).count()

        #How to search task
        input_search = self.request.GET.get('search-area') or ''
        if input_search:
            context['TitleTask'] = context['TitleTask'].filter(title__startswith=input_search)

        context['input_search'] = input_search


        return context


class TaskDetail(LoginRequiredMixin,DetailView):
    model = task
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = task
    fields = ['title','description']
    success_url = reverse_lazy('task')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate , self).form_valid(form)

class TaskEdit(LoginRequiredMixin,UpdateView):
    model = task
    fields = '__all__'
    success_url = reverse_lazy('task')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = task
    # context_object_name = 'task'
    success_url = reverse_lazy('task')
