from django.http import HttpResponseForbidden


def user_can_join_chat(function):
    def wrapper(request, *args, **kwargs):
        room_name = kwargs['room_name']

        user = request.user
        can_join = False

        if user.is_authenticated:
            can_join = user.chatgroup_set.filter(name=room_name).exists()

        if not can_join:
            return HttpResponseForbidden("You don't have permission to join this chat room.")

        return function(request, *args, **kwargs)

    return wrapper
