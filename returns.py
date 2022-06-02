# -*- coding: utf-8 -*-
import pandas as pd

class Returns:
    
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
        if type(df_dic)!=type(pd.DataFrame()):
            ohlc_data = self.ohlc_data.copy()
        else:
            ohlc_data = df_dic
            
            
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
              print("no closing bid found .... closing the last opening!!")
              l[idx]=0
              break
        ohlc_data[output_column]=l
        if type(df_dic)==type(pd.DataFrame):
            return ohlc_data
        else:
            self.ohlc_data = ohlc_data
      
    def calculateTradeReturns(self, df_dic=None, flag_column='flag', output_column="returns"):
        self.calculateReturn(df_dic, flag_column, output_column)
        
        if type(df_dic)!=type(pd.DataFrame):
            ohlc_data = self.ohlc_data
        else:
            ohlc_data = df_dic
            
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
                    percentage_variation.append(returns)
                    prev=0
                elif (val<0 and prev==0):
                    prev=val
                    
        self.percentage_returns = returns
        return returns #, percentage_variation
