from datetime import datetime



def user_last_active_middleware(get_response):
    def middleware(request):
        user = request.user
        if user.is_authenticated:
            user.last_active = datetime.now()
            user.save()
        response = get_response(request)
        # Код должен быть выполнен ответа после view
        return response
    return middleware
