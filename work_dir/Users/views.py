from allauth.account.decorators import verified_email_required
from allauth.account.forms import LoginForm
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import logout, login
from django.http import JsonResponse

from Notifications.models import Invite, Notification
from Studios.models import Studio
from Users.forms import *
from django.contrib.auth.views import LoginView

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Models.models import Model
from Photographers.models import Photographer
from Project_01.filters import *
from Staff.models import Staff
from chat.models import ChatGroup



# Create your views here.


def home(request):
    return render(request, 'base/home.html')


# class LoginRedirect(LoginView):
#     template_name = 'registration/login_redirect.html'
#     form_class = LoginForm
#     success_url = '/home'

# def get_success_url(self):
#     # Если next передан, перенаправляем на эту страницу
#     next_url = self.request.GET.get('next')
#     if next_url:
#         return next_url
#
#     return super().get_success_url()


# class RegisterUser(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'registration/register.html'
#     success_url = reverse_lazy('models')
#     extra_context = {'title': 'Регистрация'}
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('models')


# def register_user(request, role):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=True)
#             send_email_confirmation(request, user)
#             login(request, user)
#             if role == 'md':
#                 return redirect('create_model')
#             if role == 'ph':
#                 return redirect('create_ph')
#             if role == 'st':
#                 return redirect('create_staff')
#             if role == 'user':
#                 return redirect('models')
#             if role == 'sd':
#                 return redirect('create_studio')
#     else:
#         form = CustomUserCreationForm()
#
#     context = {
#         'form': form,
#         'title': 'Регистрация',
#         'role': role
#     }
#
#     return render(request, 'registration/register.html', context)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = '/home'


def logout_user(request):
    logout(request)
    return redirect('login')


@verified_email_required
def profile(request):
    try:
        studios = Studio.objects.filter(owner=request.user)
    except:
        None
    context = {'user': request.user, 'studios': studios}
    return render(request, 'profile1.html', context)


@verified_email_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})


@verified_email_required
def my_calendar(request):
    return render(request, 'calendar.html')


@verified_email_required
def my_liked(request):
    liked_models = request.user.likes.all()
    context = {
        'liked_models': liked_models
    }
    return render(request, 'liked.html', context)


def get_changes(request):
    user = request.user

    # Определяем наличие новых сообщенйи в проектах
    model_projects = Model.objects.none()
    staff_projects = Staff.objects.none()
    ph_projects = Photographer.objects.none()

    try:
        model_projects = Project_01.objects.filter(members__content_type=ContentType.objects.get_for_model(Model),
                                                   members__object_id=Model.objects.get(owner=request.user).pk,
                                                   members__is_approved=True, members__is_invited=False,
                                                   )
    except:
        pass
    try:
        staff_projects = Project_01.objects.filter(members__content_type=ContentType.objects.get_for_model(Staff),
                                                   members__object_id=Staff.objects.get(owner=request.user).pk,
                                                   members__is_approved=True, members__is_invited=False,
                                                   )
    except:
        pass
    try:
        ph_projects = Project_01.objects.filter(members__content_type=ContentType.objects.get_for_model(Photographer),
                                                members__object_id=Photographer.objects.get(owner=request.user).pk,
                                                members__is_approved=True, members__is_invited=False,
                                                )
    except:
        pass

    participant = model_projects | ph_projects | staff_projects
    project_new_message_status = 0

    for project in participant:
        try:
            chat_room = ChatGroup.objects.get(name=str(project.pk))
        except:
            continue
        messages = chat_room.message_set.all()
        for message in messages:
            message_status = message.statuses.filter(user=user).first()
            if message_status:
                if not message_status.is_read:
                    project_new_message_status = 1
                    break
        if project_new_message_status:
            break

    # Определяем наличие новых сообщений в лс
    personal_new_message_status = 0
    try:
        personal_room_list = user.personal_chat_group.all()
        for room in personal_room_list:
            personal_new_message = room.personalmessage_set.filter(new=True).exclude(author=user)
            if personal_new_message:
                personal_new_message_status = 1
                break
    except:
        None

    invitations = Invite.objects.filter(whom=request.user)
    if invitations:
        invitations = 1
    else:
        invitations = 0

    notifications = Notification.objects.filter(user=request.user)
    if notifications:
        notifications = 1
    else:
        notifications = 0

    return JsonResponse([personal_new_message_status, project_new_message_status, notifications, invitations],
                        safe=False)
