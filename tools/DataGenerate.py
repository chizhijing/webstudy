import os
import django
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyWeb.settings')
django.setup()
from ForexAccount.models import AccountInfo,SymbolInfo,StrategyInfo

def select_data():
    all_acc=AccountInfo.objects.all()
    for index,a in enumerate(all_acc):
        print(index,a)
    return all_acc

def del_data():
    all_acc = select_data()
    if len(all_acc)>0:
        all_acc[0].delete()
    select_data()

def del_all_data():
    all_account=AccountInfo.objects.all()
    all_account.delete()
    all_symbol=SymbolInfo.objects.all()
    all_symbol.delete()
    all_strategy=StrategyInfo.objects.all()
    all_strategy.delete()

def add_data():
    account_list=['6803096','6801353']
    for n in account_list:
        AccountInfo(account_name=n).save()
    symbol_list=['XAUUSD','USDJPY']
    for acc in AccountInfo.objects.all():
        for s in symbol_list:
            SymbolInfo(symbol_name=s,bool_select=True,account=acc).save()

    strategy_list=[['111','222'],['44','5','8']]
    for index,acc in enumerate(AccountInfo.objects.all()):
        for stra in strategy_list[index]:
            StrategyInfo(strategy_name=stra,account=acc).save()


if __name__=='__main__':
    # del_all_data()
    # add_data()
    # select_data()
    sym_list_sample = ["EURGBP", "EURAUD", "EURNZD", "EURUSD", "EURCAD", "EURCHF", "EURJPY",
                       "GBPAUD", "GBPNZD", "GBPUSD", "GBPCAD", "GBPCHF", "GBPJPY", "AUDNZD",
                       "AUDUSD", "AUDCAD", "AUDCHF", "AUDJPY", "NZDUSD", "NZDCAD", "NZDCHF",
                       "NZDJPY", "USDCAD", "USDCHF", "USDJPY", "CADCHF", "CADJPY", "CHFJPY"]
    ea_list_sample = ['1', '2', '3', '4', '5', '6']

    for index, acc in enumerate(AccountInfo.objects.all()):
        num_s = random.randint(2, 10)
        num_ea = random.randint(1, 5)
        sym_index = random.sample(range(0, 27), num_s)
        ea_index = random.sample(range(0, 5), num_ea)
        sym_list = [sym_list_sample[index] for index in sym_index]
        ea_list = [ea_list_sample[index] for index in ea_index]
        print(acc.account_name,num_s, num_ea, sym_index,ea_index)
        print(acc.account_name, sym_list,ea_list)

