from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.code
    
    def get_rates(self):
        return ExchangeRate.objects.filter(base_currency=self)
    
    class Meta:
        verbose_name_plural = 'currencies'

class ExchangeRate(models.Model):
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='base_currency')
    target_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='target_currency')
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    date = models.DateField()

    def __str__(self):
        return f'{self.base_currency.code}{self.target_currency.code}'