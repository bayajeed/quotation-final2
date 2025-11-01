from rest_framework import serializers
from .models import (
    QuotationTemplate, QuotationTemplateItem, Quotation,
    QuotationGroup, QuotationItem, Item, ItemGroup, Unit
)


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'name')


class ItemGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemGroup
        fields = ('id', 'name')


class ItemSerializer(serializers.ModelSerializer):
    group = ItemGroupSerializer()
    unit = UnitSerializer()

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'unit_price', 'group', 'unit')


class QuotationTemplateItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = QuotationTemplateItem
        fields = ('id', 'item', 'qty', 'unit_price')


class QuotationTemplateSerializer(serializers.ModelSerializer):
    items = QuotationTemplateItemSerializer(many=True, read_only=True)

    class Meta:
        model = QuotationTemplate
        fields = ('id', 'name', 'items')


class QuotationItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = QuotationItem
        fields = ('id', 'item', 'qty', 'unit_price', 'total_price')


class QuotationGroupSerializer(serializers.ModelSerializer):
    items = QuotationItemSerializer(many=True, read_only=True)

    class Meta:
        model = QuotationGroup
        fields = ('id', 'name', 'items')


class QuotationSerializer(serializers.ModelSerializer):
    groups = QuotationGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Quotation
        fields = ('id', 'title', 'client_name', 'created_at', 'groups')