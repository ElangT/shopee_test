from django.db import models


TAX_CODE = {
    1: 'food',
    2: 'tobacco',
    3: 'entertainment'
}


class Tax(models.Model):
    name = models.CharField(max_length=50)
    tax_code = models.IntegerField()
    price = models.PositiveIntegerField()
