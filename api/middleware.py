import json
from django.http import JsonResponse

class ModifyProductDetailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith('/api/products/') and request.method == 'GET' and response.status_code == 200:
            try:
                data = json.loads(response.content)
                if isinstance(data, dict) and 'attributes' in data:
                    new_attrs = {}
                    for attr in data['attributes']:
                        key = attr['attribute_key']
                        value = attr['attribute_value']
                        new_attrs[key] = value
                    data['attributes'] = new_attrs
                    return JsonResponse(data)
            except Exception as e:
                print(f"Middleware error: {e}")

        return response