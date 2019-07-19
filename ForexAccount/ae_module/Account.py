import datetime
import unittest

import pandas as pd

from ForexAccount.ae_module.SocketMT5 import SocketDealRecord

class Account:
    def __init__(self,account_name='6801353'):
        self.account_name=account_name #  账户名称
        self.deal_record=self.get_deal_record()  # 获取所有的交易记录
        self.symbols=[]  # 当前账户的品种列表
        self.ea_magic=[] # 当前账户的策略列表
        self.symbol_select=[]
        self.ea_select=[]
        self.deal_record_select=[]

    def set_symbol_select(self,sym_select):
        self.symbol_select=sym_select
        
    def set_ea_select(self,ea_select):
        self.ea_select=ea_select

    def get_statics(self):
        deal_record_select={}
        deal_record_select['交易品种']=self.symbol_select
        deal_record_select['策略']=self.ea_select
        df=self.get_deal_record_select(self.deal_record,**deal_record_select)
        self.deal_record_select=df
        statistics, df_fund_data=self.get_total_statics(df)
        return statistics, df_fund_data

    def get_deal_record_select(self,df,**deal_record_select):
        df_deal_record_select = df.copy()
        for i in deal_record_select.keys():
            df_deal_record_select = df_deal_record_select[df_deal_record_select[i].isin(deal_record_select[i])].copy()
        ind = []
        for i in range(len(df_deal_record_select)):
            ind.append(i)

        df_deal_record_select.index = ind
        return df_deal_record_select

    def get_deal_record(self):
        serv = SocketDealRecord('127.0.0.1', 9090)
        # 发送账户号信息，接收交易记录
        msg = serv.recvmsg(bytes(self.account_name, "utf-8"))
        # 关闭服务器
        serv.sock.close()
        a = msg.split("\n")
        l = len(a)
        d = []
        # 每行数据再根据','分割
        for i in range(l - 1):
            s = a[i].split(",")
            d.append(s)
        # 表格信息
        v = ["成交时间", "成交ID", "订单ID", "交易品种", "交易类型", "进/出场", "交易量", "成交价格", "手续费", "库存费", "利润", "策略", "仓位号", "止损", "止盈", "备注"]
        df = pd.DataFrame(data=d, columns=v)
        # 整理表格的数据类型
        df = df.apply(pd.to_numeric, errors='ignore')
        df[['成交时间']] = df[['成交时间']].apply(pd.to_datetime, errors='ignore')
        return df

    def get_symbols(self):
        t=list(self.deal_record.groupby(by = '交易品种').groups.keys())
        t.remove('')
        self.symbols=t
        return t

    def get_magic_ID(self):
        print(self.deal_record.iloc[2])
        t=list(self.deal_record.groupby(by = '策略').groups.keys())
        print(t)
        self.ea_magic=t
        return t

    def get_simple_statics(self):
        pass

    def get_total_statics(self, df, init_capital=10000):
        df = df[df['交易类型'] != 2] # 去除存放资金的数据
        ind = []
        for i in range(len(df)):
            ind.append(i)
        df.index = ind
        l = len(df['成交时间']) # 获取账户信息表格df的长度
        # 获取订单的净利润序列和持仓时间序列
        net_profit = []
        position_time = []
        for p in range(l):
            if (df['进/出场'][p] == 0):
                profit_1 = df['利润'][p] + df['手续费'][p] + df['库存费'][p]
                time_1 = df['成交时间'][p]
                position_ID = df['仓位号'][p]
                for o in range(p + 1, len(df)):
                    if (df['仓位号'][o] == position_ID):
                        profit_2 = df['利润'][o] + df['手续费'][o] + df['库存费'][o]
                        net_profit.append(profit_1 + profit_2)
                        time_2 = df['成交时间'][o]
                        position_time.append(time_2 - time_1)
                        break
        # 获取订单的赢利次数
        win_num = 0
        for i in net_profit:
            if i > 0:
                win_num += 1
        # 获取总的持仓时间
        sum_position_time = datetime.timedelta(0)
        for i in position_time:
            sum_position_time += i
        # 获取第一笔交易到最后一笔交易经过的时间，单位为天，类型是float
        total_time = df['成交时间'][l - 1] - df['成交时间'][0]
        total_time_day = total_time.days + total_time.seconds / 86400
        # 获取成交的净利润序列
        net_profit_list = df['利润'] + df['手续费'] + df['库存费']
        net_profit_list = net_profit_list.values

        capital_list = []  # 资金序列
        max_capital_list = []  # 最高盈利的时间序列
        draw_down_list = []  # 回撤的序列
        draw_down_rate_list = []  # 回撤率序列
        capital_rate_list = []  # 净收益率序列
        max_capital = init_capital  # 最大账户余额

        # 交易分析汇总
        capital = init_capital
        for i in range(len(net_profit_list)):
            capital += net_profit_list[i]
            max_capital = max(capital, max_capital)
            draw_down = capital - max_capital  # 回撤
            draw_down_rate = draw_down / max_capital  # 回撤率
            capital_rate = (capital - init_capital) / init_capital  # 净收益率
            capital_list.append(capital)  # 资金序列
            max_capital_list.append(max_capital)
            draw_down_list.append(draw_down)
            draw_down_rate_list.append(draw_down_rate)
            capital_rate_list.append(capital_rate)

            # 获取累计利润序列
        cumulative_profit = []
        cumulative_profit.append(net_profit_list[0])
        for i in range(1, len(net_profit_list)):
            cumulative_profit.append(cumulative_profit[i - 1] + net_profit_list[i])

        # 计算各种统计指标并存入statistics
        statistics = {}
        statistics['开始时间'] = df['成交时间'][0]
        statistics['结束时间'] = df['成交时间'][l - 1]
        statistics['交易次数'] = len(net_profit)
        statistics['手数'] = sum(df['交易量']) / 2
        statistics['毛利润'] = sum(df['利润']) - df['利润'][0]
        statistics['手续费'] = sum(df['手续费'])
        statistics['库存费'] = sum(df['库存费'])
        statistics['最大亏损'] = min(net_profit)
        statistics['最大赢利'] = max(net_profit)
        statistics['最长持仓时间'] = max(position_time)
        statistics['最短持仓时间'] = min(position_time)
        statistics['平均持仓时间'] = sum_position_time / len(net_profit)
        statistics['交易频率/天'] = len(net_profit) / total_time_day
        statistics['胜率'] = win_num / len(net_profit)
        statistics['净收益'] = sum(net_profit)
        statistics['最大回撤值'] = min(draw_down_list)
        statistics['最大回撤率'] = min(draw_down_rate_list)
        statistics['采收率'] = sum(net_profit) / -min(draw_down_list)
        statistics['最大回撤起点'] = cumulative_profit[draw_down_rate_list.index(min(draw_down_rate_list))] + init_capital

        # 将4种资金曲线图所需的数据存入df_plot中，索引是成交时间
        transaction_time = df['成交时间'].values
        dic = {'资金': capital_list, '收益率': capital_rate_list, '回撤值': draw_down_list, '回撤率': draw_down_rate_list}
        df_fund_data = pd.DataFrame(data=dic, index=transaction_time)

        # 返回统计指标statistics和资金曲线图数据df_plot
        return statistics, df_fund_data

class AccountTestCase(unittest.TestCase):
    def setUp(self):
        self.account_infor=Account('6801353')
        print(self.account_infor.account_name)
        print(self.account_infor.deal_record.head(2))

    def tearDown(self):
        del self.account_infor

    def test_get_total_statics(self):
        d,curve_data=self.account_infor.get_total_statics(self.account_infor.deal_record)
        print(d)
        print(curve_data.head())

    def test_get_statics(self):
        self.account_infor.set_symbol_select(['EURUSD', 'XAUUSD'])
        self.account_infor.set_ea_select([1215, 20190627])
        d, curve_data=self.account_infor.get_statics()
        print(self.account_infor.deal_record_select)
        print(d)
        print(curve_data.head())

    def test_get_symbols(self):
        self.account_infor.get_symbols()
        print(self.account_infor.symbol_select)

    def test_get_magic_ID(self):
        self.account_infor.get_magic_ID()
        print(self.account_infor.ea_select) 

if __name__=='__main__':
    unittest.main()
