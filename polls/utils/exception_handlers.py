from django.http.response import Http404
from rest_framework.views import exception_handler


# TODO: Improve naming!
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        # "kwargs" will have some details about the request...maybe 🤔.
        kwargs = context["kwargs"]

        # Format error details using the "kwargs" dictionary.
        request_details = ", ".join(
            f"{k.replace('_id', '').capitalize()} ID: {v}"
            for k, v in kwargs.items()
            if kwargs
        )

        response.data[
            "detail"
        ] = f"{exc} {request_details}. Please check the request and try again. 🥅"

    return response
