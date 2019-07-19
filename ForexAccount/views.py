from django.shortcuts import render
from .models import AccountInfo,SymbolInfo,StrategyInfo
from .ae_module.Account import Account
import random
# Create your views here.

def get_index_page(request):
    # 删除数据库内容
    # all_account = AccountInfo.objects.all()
    # all_account.delete()
    all_symbol = SymbolInfo.objects.all()
    all_symbol.delete()
    all_strategy = StrategyInfo.objects.all()
    all_strategy.delete()
    # 重新随机生成数据库内容
    sym_list_sample=["EURGBP","EURAUD","EURNZD","EURUSD","EURCAD","EURCHF","EURJPY",
                      "GBPAUD","GBPNZD","GBPUSD","GBPCAD","GBPCHF","GBPJPY","AUDNZD",
                      "AUDUSD","AUDCAD","AUDCHF","AUDJPY","NZDUSD","NZDCAD","NZDCHF",
                      "NZDJPY","USDCAD","USDCHF","USDJPY","CADCHF","CADJPY","CHFJPY"]
    ea_list_sample=['1','2','3','4','5','6']

    for index, acc in enumerate(AccountInfo.objects.all()):
        num_s=random.randint(2,10)
        num_ea=random.randint(1,5)
        sym_index=random.sample(range(1,27),num_s)
        ea_index=random.sample(range(0,5),num_ea)
        sym_list = [sym_list_sample[index] for index in sym_index]
        ea_list = [ea_list_sample[index] for index in ea_index]
        for sym in sym_list:
            SymbolInfo(symbol_name=sym,bool_select=True,account=acc).save()
        for stra in ea_list:
            StrategyInfo(strategy_name=stra, account=acc).save()

    all_account=AccountInfo.objects.all()
    # account_name_list=[account.account_name for account in all_account]
    return render(request,'ForexAccount\index.html',{'n_list':all_account})

def get_account_result_page(request):
    all_account=AccountInfo.objects.all()
    current_account=all_account[0]
    forex_account=Account('6801353')
    sym_list=forex_account.get_symbols()
    ea_list=forex_account.get_magic_ID()
    forex_account.set_symbol_select(sym_list)
    forex_account.set_symbol_select(ea_list)
    (s_dict,df_curve)=forex_account.get_total_statics(forex_account.deal_record)
    stats=[key+':'+str(s_dict[key]) for key in s_dict.keys()]

    return render(request,'ForexAccount/account_result.html',{'a_infor':current_account,'s_list':sym_list,'ea_list':ea_list,'stats':stats})