from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import LoginForm, RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required, user_passes_test



#---------------------------------------------------NEW-----------------------------------------------------



def home(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'index.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})

#---------------------------------------------------NEW-----------------------------------------------------
def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'dashboard.html', {'posts': posts})

@user_passes_test(is_admin)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@user_passes_test(is_admin)
def edit_post(request, pk):  # Make sure this parameter is named pk
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})


@user_passes_test(is_admin)
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Use pk instead of post_id
    post.delete()
    return redirect('admin_dashboard')
#--------------------------------------------------------login-register-part-----------------------------------



class RegisterView(FormView):
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']


        form.save()
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm

    def get_success_url(self):
        # Check if user is staff/admin
        if self.request.user.is_staff:
            return reverse_lazy('admin_dashboard')
        else:
            return reverse_lazy('home')  # Make sure you have a URL named 'home'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)
