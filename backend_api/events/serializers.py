from rest_framework import serializers
from .models import Event
from stores.serializers import StoreListSerializer


class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    store_details = StoreListSerializer(source='store', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'event_type', 'start_date', 'end_date', 'phone_number',
            'store', 'store_details', 'store_location', 'store_phone_number', 'created_by',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def validate(self, data):
        # Ensure start_date is before end_date
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] >= data['end_date']:
                raise serializers.ValidationError("End date must be after start date.")

        # Validate required fields based on event_type
        event_type = data.get('event_type')
        if event_type == 'account_management':
            if not data.get('store'):
                raise serializers.ValidationError("Store is required for Account Management events.")
        elif event_type == 'store_acquisition':
            if not data.get('store_location'):
                raise serializers.ValidationError("Store location is required for Store Acquisition events.")
            if not data.get('store_phone_number'):
                raise serializers.ValidationError("Store phone number is required for Store Acquisition events.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class EventListSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    store_name = serializers.CharField(source='store.name',read_only=True)

    class Meta:
        model=Event
        fields = [
            'id', 'name', 'event_type', 'start_date', 'end_date', 'phone_number','created_by',
            'store_name', 'store_location', 'store_phone_number','created_at', 'is_active'
        ]


class EventDetailSerializers(serializers.ModelSerializer):
    created_by  = serializers.StringRelatedField(read_only=True)
    store_details = StoreListSerializer(source='store',read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'event_type', 'start_date', 'end_date', 'phone_number',
                'store', 'store_details', 'store_location', 'store_phone_number',
                'created_by', 'created_at', 'updated_at']



