__author__ = 'OllyD'
from .forms import UserLoginForm, UserForm
from .models import UserProfile
from .views import UserLoginFormView


# def login_form(self, request):
#     if not request.user.is_authenticated:
#         form_class = UserLoginForm
#         form = self.form_class(None)
#        # context = form
#         return {'form': form}
#     else:
#         return {}

def login_form(request):
    form_login_class = UserLoginForm()
    form_register_class = UserForm()
    if not request.user.is_authenticated:
        return {
            'form_login': form_login_class,
            'form_register': form_register_class
        }
    else:
        return {

        }

def profilepicture(request):
    if request.user.is_authenticated:
        context = UserProfile.objects.get(user=request.user)
        return {'context': context}
    else:
        return {}
