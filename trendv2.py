"""
this strategy is used to minimize (almost none) the losses and make strong profit in the right time
https://youtu.be/t-k899KCHJA
"""

from decimal import *

class Trend:
    getcontext().prec = 5
    brokerage = float(Decimal(999) / Decimal(1000))
    transactions = []

    def __init__(self,op_count,money,head,increase,percent,ratio):
        self.op_count = op_count
        self.money = money
        self.head = head
        self.increase = increase
        self.percent = percent
        self.ratio = ratio

    #calculating the transactions per increase
    def get_transactions(self):
        money_list = list()
        if isinstance(self.increase,float):
            money_list = [self.money*(self.increase**i) for i in range(self.op_count)]
        else:
            money_list = [self.money*(self.increase[i]) for i in range(self.op_count)]

        self.transactions = list(map(lambda x: x * self.brokerage, money_list))
        print(self.transactions)
        print(sum(money_list))
        return sum(money_list)

    #deciding the wheter it exited with long or short
    def get_tail(self):
        types = ["long","short"]
        types.remove(self.head)
        return self.head if self.op_count%2==1 else types[0]

    def get_shorts(self):
        start = 0 if self.head == "short" else 1
        return sum([self.transactions[i] for i in range(start,len(self.transactions),2)])

    def get_longs(self):
        start = 0 if self.head == "long" else 1
        return sum([self.transactions[i] for i in range(start,len(self.transactions),2)])

    #calculating the total transactions with percentages
    def get_positions(self):
        final_long, final_short = 0, 0
        """
        t4 = float(100 + Decimal(self.percent) * Decimal(self.ratio) +  Decimal(self.percent) / Decimal(2))
        t3 = float(100 + Decimal(self.percent) / Decimal(2))
        t2 = float(100 - Decimal(self.percent) / Decimal(2))
        t1 = float(100 - Decimal(self.percent) * Decimal(self.ratio) - Decimal(self.percent) / Decimal(2))
        """
        
        t4 = 100 + self.percent*self.ratio
        t3 = 100
        t2 = 100 - self.percent
        t1 = 100 - self.percent*(self.ratio+1)
        print(t4,t3,t2,t1)
        
        tail = self.get_tail()
        shorts = self.get_shorts()
        longs = self.get_longs()
        print(shorts,"\n",longs)
        
        if tail == "long":
            final_long = longs * (100+(self.percent*self.ratio))/(100)
            final_short = shorts * (100-((100*self.percent*(self.ratio+1))/(100+self.percent*self.ratio)))/(100)
            
        elif tail == "short":
            final_long = longs * (100-self.percent*(self.ratio+1))/(100)
            final_short = shorts * (100+(self.percent*self.ratio))/(100)
        
        
        print(final_long,"\n",final_short,"\n",self.brokerage,"\n",final_long+final_short)

        return (final_long + final_short) * self.brokerage

    #calculating profit also including commissons
    def get_profit(self):
        required = self.get_transactions()
        total_money = self.get_positions()
        profit = total_money - required
        profit_percent = profit / required * 100
        print(f"{required = }&  {total_money = }&  {profit = }&  {profit_percent = }%\n\n")
        return [profit,profit_percent]


#example of using historical data of luna
count = [6,3,1,4,1,6]
money = [100 for i in range(6)]
head = ["short","long","long","long","short","long"]
increase = [2.0 for i in range(6)]
#increase = [[1,3,10,50,100,350] for i in range(6)]
percent = [3,3,3,3,3,3]
ratio = [2,3,4,3,4,3]


for i in range(len(count)):
    print(i+1)
    trend = Trend(count[i],money[i],head[i],increase[i],percent[i],ratio[i])
    trend.get_profit()









