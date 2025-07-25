from django.shortcuts import render
from rest_framework import viewsets , filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category , SubCategory , Product , Comment , Attribute
from rest_framework.permissions import IsAuthenticated
from .persmissions import IsCommentOwner
from .serializer import CategorySerializer , SubCategorySerializer , ProductSerializer , CommentSerializer
from rest_framework.filters import SearchFilter
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Prefetch
from .pagination import FastCountPagination
from django.shortcuts import get_object_or_404


@method_decorator(cache_page(60 * 5), name='dispatch')
class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]


@method_decorator(cache_page(60 * 5), name='dispatch')
class SubCategoryAPIView(viewsets.ModelViewSet):
    queryset = SubCategory.objects.select_related('category').all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]

@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductAPIView(viewsets.ModelViewSet):
  
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated , IsCommentOwner]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    def get_queryset(self):
        return Product.objects.select_related('subcategory', 'owner' ).prefetch_related(
                Prefetch(
                    'attributes',
                    queryset=Attribute.objects.select_related('attribute_key', 'attribute_value'),
                    to_attr='prefetched_attributes' 
                )
            )

    filterset_fields = ['subcategory', 'price']

    search_fields = ['title', 'description']

    ordering_fields = ['price',]



# views.py
@method_decorator(cache_page(60 * 2), name='dispatch')  # 2 daqiqa cache
class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related(
        'owner',
        'product'
    ).prefetch_related(
        'product__subcategory'
    ).only(
        'id', 'comment', 'created_at',
        'owner_id', 'owner__username',
        'product_id', 'product__title',
        'product__subcategory_id'
    ).order_by('-created_at')
    
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentOwner]
    pagination_class = FastCountPagination 

    # views.py
    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
    
        serializer.save(
            owner=self.request.user,
            name=self.request.user.username,
            email=self.request.user.email,
            product=product  
        )


    

