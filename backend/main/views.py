from django.http import JsonResponse
from django.middleware.csrf import get_token


# https://github.com/graphql-python/graphene-django/issues/593
def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})
