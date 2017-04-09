from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
#from profiles.models import Userprofile
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, DetailView, ListView, FormView
from .forms import UserLoginForm, UserForm, UserEditForm, UserRegisterForm
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from videos.models import VideoModel
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

User = get_user_model()



class UserRegisterFormView(FormView):
    template_name = 'base.html'
    form_class = UserRegisterForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('accounts:home')


    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        login(self.request, new_user)
        return super(UserRegisterFormView, self).form_valid(form)

    # def get_context_data(self, *args, **kwargs):
    #     context = super(UserRegisterFormView, self, *args, **kwargs)
    #     if self.form.is_valid():
    #         context['valid'] = True


class UserLoginFormView(View):
    form_class = UserLoginForm
    template_name = "base.html"

    def get(self, request):
        if not request.user.is_authenticated:
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect("accounts:home")

    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("accounts:home")

        #else:
            #if not user or not user.is_active:

            #return redirect("accounts:login")

class UserDetailView(DetailView):
    template_name = "accounts/profile_detail.html"
    queryset = User.objects.all()

    def get_object(self):

        user = get_object_or_404(User, username__iexact=self.kwargs.get("username"))
        return user

    def get_context_data(self, *args, **kwargs):
        #user = super(UserDetailView, self).get_object(self, *args, **kwargs)
        user = UserDetailView.get_object(self)
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        context['all_videos'] = VideoModel.objects.filter(user=user)
        return context

class ProfileListView(ListView):
    template_name = 'accounts/profile_list.html'
    context_object_name = 'all_profiles'
    # paginate_by = 10

    def get_queryset(self):
        return UserProfile.objects.all()

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object(queryset=Publisher.objects.all())
    #     return super(PublisherDetail, self).get(request, *args, **kwargs)


class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    template_name = "accounts/profile_edit.html"
    model = UserProfile
    fields = ['first_name', 'last_name', 'user_img', 'bio', 'profile_banner']
    context_object_name = 'someuser'


    #form_class = UserEditForm
   # success_url = 'http://127.0.0.1:8002'


    def get_object(self, *args, **kwargs):
        #user = get_object_or_404(User, username__iexact=self.kwargs.get("username")):
            user = UserProfile.objects.get(user=self.request.user.pk)
            return user


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:home")
        else:
            return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super(ProfileUpdateView, self).get_context_data(**kwargs)
    #     context['second_model'] = UserEditForm#whatever you would like
    #     return context
    # def form_valid(self, form):
    #
    #     return self.render_to_response(self.get_context_data(form=form))


def home(request):
    return render(request, "base.html", {})

def logout_view(request):
    logout(request)
    return redirect('accounts:home')


class UserFormView(FormView):
    form_class = UserRegisterForm
    template_name = 'base.html'

    # display blank form
    def get(self, request):
        if not request.user.is_authenticated:
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('accounts:home')

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        return super(UserFormView, self).form_valid(form)

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # clearned (normalized) data

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # userprofile = UserProfile(user=user)
            # userprofile.save()

            #returns User objects if credentials are correct

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect("accounts:home")

        return render(request, self.template_name, {'form': form})