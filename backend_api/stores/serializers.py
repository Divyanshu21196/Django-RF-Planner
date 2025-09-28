from rest_framework import serializers
from .models import Store

class StoreSerializer(serializers.ModelSerializer):

    created_by = serializers.StringRelatedField(read_only=True)
    created_by_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def validate_name(self, value):
        if Store.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Store with this name already exists.")
        return value

    def validate_phone_number(self, value):
        if not value.strip():
            raise serializers.ValidationError("Phone number cannot be empty or just whitespace.")
        return value

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)



class StoreListSerializer(serializers.ModelSerializer):

    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Store
        fields = ('id', 'name', 'town', 'country', 'phone_number', 'created_at', 'created_by')
        read_only_fields = ('id', 'created_at', 'created_by')

class StoreDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    created_by_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')