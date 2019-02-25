from rest_framework import serializers
from tax.models import Tax, TAX_CODE
from tax.utils import TaxHandler


class TaxSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    tax_code = serializers.IntegerField()
    price = serializers.IntegerField(min_value=0)

    def validate(self, data):
        if data['tax_code'] not in TAX_CODE:
            raise serializers.ValidationError("tax code must be either" +
                                              ", ".
                                              join([str(x) for x in TAX_CODE]))
        return data

    def create(self, validated_data):
        return Tax.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.tax_code = validated_data.get('tax_code', instance.tax_code)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

    def to_representation(self, obj):
        field = super().to_representation(obj)
        tax_handler = TaxHandler(field['tax_code'], field['price'])
        field['type'] = tax_handler.tax_type()
        field['tax'] = tax_handler.count_tax()
        field['amount'] = tax_handler.count_amount()
        field['refundable'] = tax_handler.is_refundable()
        return field
