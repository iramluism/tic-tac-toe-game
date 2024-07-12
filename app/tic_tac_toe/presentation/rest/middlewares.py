import logging

from django.http.response import JsonResponse
from tic_tac_toe.domain.exceptions import DomainException
from tic_tac_toe.presentation.rest import errors

logger = logging.getLogger(__name__)


def error_handler_middleware(get_response):
    def middleware(request):
        try:
            response = get_response(request)
        except DomainException as exc:
            logger.error(f"DOMAIN ERROR: {exc.message} ({exc.code})")

            status_code = errors.get_status_code(exc.error_code)

            response = JsonResponse(
                data={
                    "message": exc.message,
                    "code": exc.code,
                },
                status=status_code,
            )

        return response

    return middleware
