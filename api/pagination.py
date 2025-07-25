
from rest_framework.pagination import PageNumberPagination

class FastCountPagination(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
       
        if 'page' not in request.query_params:
            return None
        return super().paginate_queryset(queryset, request, view)