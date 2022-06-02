# -*- coding: utf-8 -*-

class Metrics:
    
    def CAGR(self, DF):
        "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
        df = DF.copy()
        df["cum_return"] = (1 + df["mon_ret"]).cumprod()
        n = len(df)/12
        CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
        return CAGR

    def volatility(self, DF):
        "function to calculate annualized volatility of a trading strategy"
        df = DF.copy()
        vol = df["mon_ret"].std() * np.sqrt(12)
        return vol

    def sharpe(self, DF,rf):
        "function to calculate sharpe ratio ; rf is the risk free rate"
        df = DF.copy()
        sr = (self.CAGR(df) - rf)/self.volatility(df)
        return sr
        

    def max_dd(self, DF):
        "function to calculate max drawdown"
        df = DF.copy()
        df["cum_return"] = (1 + df["mon_ret"]).cumprod()
        df["cum_roll_max"] = df["cum_return"].cummax()
        df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
        df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
        max_dd = df["drawdown_pct"].max()
        return max_dd
        
    def calculateAccuracy(self, column_name, df_dic=None):  # type=complete/max_du
    
        try:
            df_dic==None
            ohlc_data = self.ohlc_data
        except:
            ohlc_data = df_dic
            
            
        for key in ohlc_data.keys():
            pos=0
            neg=0
            bookings = list(ohlc_data[column_name])
            bookings = [i for i in bookings if i!=0]
            range_=len(bookings)
            if len(bookings)%2==1:
                range_=range_-1
            for i in range(0, range_, 2):
                if i+1==len(bookings):
                    print("couldn't find closing bid: Ignoring the last opening.")
                returns = bookings[i]+bookings[i+1]
                if returns>0:
                    pos+=1
                elif returns<=0:
                    neg+=1
            if (pos+neg)==0:
                print("No buying bid found!")
                return None
            return pos/(pos+neg), pos, (pos+neg)
        
        
      #  return ohlc_data
    def max_du(self, l):
        "function to calculate max drawdown"
        l=list(l)
        min_l=[]
        max_l=[]
        min_=100000000000
        max_=-100000000000
        for val in l:
            min_=min(min_, val)
            min_l.append(min_)
            
        for val in l[::-1]:
            max_=max(max_, val)
            max_l.append(max_)
            
        max_l=max_l[::-1]
        max_du=-1000
        
        for i in range(len(min_l)):
            max_du=max(max_du, max_l[i]/min_l[i])
        return max_du
      