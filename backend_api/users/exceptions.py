from rest_framework.views import exception_handler
from rest_framework.response import Response
from datetime import datetime


def custom_exception_handler(exc, context):
    """
    Custom exception handler for standardized error responses.
    FIX FOR ISSUE #4 - API Response Standards
    """
    response = exception_handler(exc, context)

    if response is not None:
        request = context['request']

        custom_response_data = {
            'success': False,
            'message': get_error_message(response.data),
            'data': None,
            'errors': response.data,
            'status_code': response.status_code,
            'timestamp': datetime.now().isoformat(),
            'path': request.path,
        }

        response.data = custom_response_data

    return response


def get_error_message(data):
    """Extract meaningful error message from response data"""
    if isinstance(data, dict):
        if 'detail' in data:
            return str(data['detail'])
        if 'error' in data:
            return str(data['error'])
        # Get first error message
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                return f"{key}: {value[0]}"
            elif isinstance(value, str):
                return f"{key}: {value}"
    elif isinstance(data, list) and len(data) > 0:
        return str(data[0])

    return "An error occurred"