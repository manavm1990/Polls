from rest_framework.exceptions import NotFound


class ResourceNotFoundException(NotFound):
    def __init__(self, model_name="unknown model", requested_id="unknown 🆔"):
        detail = f"{model_name} with ID {requested_id} not found."
        super().__init__(detail=detail)
