from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import exception_handler


def generate_404_text(context: dict) -> str:
    """
    Generate a detailed message for 404 Not Found errors based on the context provided.

    Args:
        context (dict): A dictionary containing the context of the request.

    Returns:
        str: A formatted string with request details.
    """
    # "kwargs" will have some details about the request...maybe 🤔.
    kwargs = context["kwargs"]

    # Format error details using the "kwargs" dictionary.
    return ", ".join(
        f"{k.replace('_id', '').capitalize()} ID: {v}"
        for k, v in kwargs.items()
        if kwargs
    )


def handle_exception(exc: Exception, context: dict) -> Response:
    """
    Custom exception handler to modify the default behavior of exception handling in the API.

    Args:
        exc (Exception): The exception to be handled.
        context (dict): A dictionary containing the context of the request.

    Returns:
        Response: A modified Response object if applicable, None otherwise.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        response.data = {"detail": f"{exc} {generate_404_text(context)}"}

    return response
