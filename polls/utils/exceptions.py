from django.http.response import Http404
from rest_framework.views import exception_handler


def generate_404_text(ctx):
    # "kwargs" will have some details about the request...maybe 🤔.
    kwargs = ctx["kwargs"]

    # Format error details using the "kwargs" dictionary.
    return ", ".join(
        f"{k.replace('_id', '').capitalize()} ID: {v}"
        for k, v in kwargs.items()
        if kwargs
    )


def handle_exception(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        response.data = {"detail": f"{exc} {generate_404_text(context)}"}

    return response
