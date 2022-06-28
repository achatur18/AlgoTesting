# -*- coding: utf-8 -*-
import pandas as pd

class Returns:
    def calculateReturnFromSignal(self, df, signal_col, price_col):
        ohlc_data=df.copy(deep=True)
        buy=[]
        sell=[]
        
        for i, row in ohlc_data.iterrows():
            if row[signal_col]=='BUY':
                buy.append(row[price_col])
            elif row[signal_col]=='SELL':
                sell.append(row[price_col])

        returns=[]
        pos_trades=0
        for i in range(len(sell)):
            if i >=len(buy): break
            returns.append(sell[i]/buy[i])
            if returns[-1]>1: pos_trades+=1
        
        for i in range(1, len(returns)):
            returns[i]*=returns[i-1]
        return returns[-1], len(returns), pos_trades
    
    def createSignalFromMetaLabels(self, df, col, buyThres, sellThres):
        ohlc_data = df.copy(deep=True)
        l=[]
        prev=""
        
        for i, row in ohlc_data.iterrows():
          if row[col]>=buyThres and prev=='':
              l.append("BUY")
              prev="BUY"
          elif row[col]<=sellThres and prev=='':
              l.append("HOLD")
              
          elif row[col]>=buyThres and prev=='BUY':
              l.append("HOLD")
          elif row[col]<=sellThres and prev=='BUY':
              l.append("SELL")
              prev="SELL"
              
          elif row[col]>=buyThres and prev=='SELL':
              l.append("BUY")
              prev="BUY"
          elif row[col]<=sellThres and prev=='SELL':
              l.append("HOLD")
              
          else:
              l.append("HOLD")
        return l
    
    def calculateMetaLabelReturn(self, df, col, buyThres=0.15, sellThres=0.05):
        df = df.copy(deep=True)
        df['signal'] = self.createSignalFromMetaLabels( df, col, buyThres=buyThres, sellThres=sellThres)
        returns, nooftrades, pos_trades = self.calculateReturnFromSignal(df, "signal", "Adj Close")
        dic = {}
        dic['returns']=returns
        dic['signal']=df['signal']
        dic['nooftrades']=nooftrades
        dic['pos_trades']=pos_trades
        return dic
    
    def calculateInvestmentReturns(self, df_dic=None, type="max_du"):  # type=complete/max_du
        #if type(df_dic)!=type(pd.DataFrame()):
        try:
            df_dic==None
            ohlc_data = self.ohlc_data
        except:
            ohlc_data = df_dic
            
        if type=="complete":
            for key in ohlc_data.keys():
                price = list(ohlc_data["Adj Close"])
                return price[-1]/price[0] #, price[-1], price[0]
            
        elif type=="max_du":
            for key in ohlc_data.keys():
                price = ohlc_data["Adj Close"]
                return self.max_du(price)

    def calculateReturn(self, df_dic=None, flag_column='flag', output_column="returns"):
        ohlc_data = df_dic.copy(deep=True)
            
        l=[]
        prev=""
        # ohlc_data['returns']=0
        for i, row in ohlc_data.iterrows():
          if row[flag_column]=='BUY' and prev=='SELL':
            l.append(-1*row["Adj Close"])
            prev='BUY'
          elif row[flag_column]=='SELL' and prev=='BUY':
            l.append(row["Adj Close"])
            prev='SELL'
          elif row[flag_column]=='SELL' and prev=='':
            l.append(0)
            prev='SELL'
          elif row[flag_column]=='BUY' and prev=='':
            l.append(-1*row["Adj Close"])
            prev='BUY'
          else:
            l.append(0)

            # Check if last non zero value in list is +ve or -ve
        for idx, i in enumerate(l[::-1]):
            if(i!=0 and i>0):
                break
            if(i!=0 and i<0):
#                 print("no closing bid found .... selling the holdings!!")
#                 l[-1]=ohlc_data['Adj Close'][-1]
              print("no closing bid found .... closing the last opening!!")
              l[idx]=0
              break
        ohlc_data[output_column]=l
        return ohlc_data
      
    def calculateTradeReturns(self, df_dic=None, flag_column='flag', output_column="returns"):
        ohlc_data = self.calculateReturn(df_dic, flag_column, output_column)
        
            
        for key in ohlc_data.keys():
            buy_sells = ohlc_data[output_column]
            
            returns=1
            percentage_variation=[]
            prev = 0
            for val in buy_sells:
                if val>0:
                    if prev==0:
                        print("found sell before buy!! .... skipping this.")
                        continue
                    returns*=val/abs(prev)
                    percentage_variation.append(val/abs(prev))
                    prev=0
                elif (val<0 and prev==0):
                    prev=val
                    
        return returns , percentage_variation
