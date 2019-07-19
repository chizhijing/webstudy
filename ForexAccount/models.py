from django.db import models

# Create your models here.
class AccountInfo(models.Model):
    # account_id = models.AutoField(primary_key=True)
    account_name=models.TextField()

    def __str__(self):
        return self.account_name

class SymbolInfo(models.Model):
    symbol_name=models.TextField()
    bool_select=models.BooleanField(default=True)
    account=models.ForeignKey(AccountInfo,on_delete=models.CASCADE)

    def __str__(self):
        return self.symbol_name

class StrategyInfo(models.Model):
    strategy_name=models.TextField()
    account = models.ForeignKey(AccountInfo, on_delete=models.CASCADE)

    def __str__(self):
        return  self.strategy_name