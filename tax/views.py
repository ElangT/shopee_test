from django.db import transaction

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework import status

from tax.models import Tax
from tax.serializers import TaxSerializer
from tax.utils import TaxHandler


class TaxViewSet(viewsets.GenericViewSet):
    """
    Method Documentation

    list:
    Return a list of all the tax object. Count it's total price, total tax
    and total amount

    create:
    Create a new tax instance.

    retrieve:
    Return a tax object with given id.

    update:
    Update a tax object with given id.

    delete:
    Delete a tax object with given id.

    Parameter

    Name (Char, max 50 character)

    Price (Integer)

    Tax Code (Integer, 1-3)
    1: food
    2: tobacco
    3: entertainment

    """
    permission_classes = (AllowAny,)
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer

    def list(self, request):
        tax = Tax.objects.all()
        serializer = TaxSerializer(tax, many=True)
        data = {
            'data': serializer.data,
            'price_subtotal': sum([i['price'] for i in serializer.data]),
            'tax_subtotal': sum([i['tax'] for i in serializer.data]),
            'grand_total': sum([i['amount'] for i in serializer.data])
        }
        return Response(data)

    @transaction.atomic()
    def create(self, request):
        data = request.data
        tax = self.get_serializer(data=data)
        if tax.is_valid(raise_exception=True):
            tax.save()
            return Response(tax.data,
                            status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        tax = get_object_or_404(self.queryset, pk=pk)
        serializer = TaxSerializer(tax)
        return Response(serializer.data)

    @transaction.atomic()
    def update(self, request, pk=None):
        tax = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(
            tax,
            data=request.data,
            partial=True,
        )
        if(serializer.is_valid(raise_exception=True)):
            tax = serializer.save()
            resp = self.get_serializer(tax).data
            return Response(resp, status=status.HTTP_200_OK)

    @transaction.atomic()
    def delete(self, request, pk=None):
        tax = get_object_or_404(self.queryset, pk=pk)
        tax.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
