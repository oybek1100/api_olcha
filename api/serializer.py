from rest_framework.serializers import ModelSerializer
from .models import Category , SubCategory , Product , Comment , Attribute
from rest_framework.serializers import ModelSerializer, CharField , IntegerField
from rest_framework.fields import SerializerMethodField

class AttributeSerializer(ModelSerializer):
    attribute_key = CharField(source='attribute_key.key_name')
    attribute_value = CharField(source='attribute_value.value_name')

    class Meta:
        model = Attribute
        fields = ['id', 'attribute_key', 'attribute_value']

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
     


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
      
    

class ProductSerializer(ModelSerializer):
    dynamic_attributes =SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'quantity',
            'subcategory', 'owner', 'dynamic_attributes'
        ]

    def get_fields(self):
        fields = super().get_fields()
        view = self.context.get('view', None)
        if view and not getattr(view, 'action', None) == 'retrieve':
            fields.pop('dynamic_attributes', None)
        return fields

    def get_dynamic_attributes(self, obj):
        return {
            attr.attribute_key.key_name: attr.attribute_value.value_name
            for attr in obj.prefetched_attributes
        }

       
# serializers.py
class CommentSerializer(ModelSerializer):
    owner = CharField(source='owner.username', read_only=True)
    product = CharField(source='product.title', read_only=True)
    product_id = IntegerField(write_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_at', 'owner', 'product' , 'product_id']
        read_only_fields = ['created_at']