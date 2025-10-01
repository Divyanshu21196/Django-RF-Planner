from rest_framework.renderers import JSONRenderer

class StandardJSONRenderer(JSONRenderer):
    """
    Standard JSON renderer that wraps all responses in a consistent format.
    FIX FOR ISSUE #4 - API Response Standards
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {}

        if renderer_context:
            response = renderer_context['response']
            request = renderer_context['request']

            # Standard response format
            if 200 <= response.status_code < 300:
                response_dict = {
                    'success': True,
                    'message': 'Request successful',
                    'data': data,
                    'status_code': response.status_code,
                    'timestamp': self.get_timestamp(),
                    'path': request.path,
                }
            else:
                # Error response format
                response_dict = {
                    'success': False,
                    'message': self.get_error_message(data),
                    'data': None,
                    'errors': data,
                    'status_code': response.status_code,
                    'timestamp': self.get_timestamp(),
                    'path': request.path,
                }
        else:
            # Fallback
            response_dict = data

        return super().render(response_dict, accepted_media_type, renderer_context)

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

    def get_error_message(self, data):
        if isinstance(data, dict):
            if 'detail' in data:
                return str(data['detail'])
            if 'error' in data:
                return str(data['error'])
            # Get first error message
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0:
                    return f"{key}: {value[0]}"
        return "An error occurred"