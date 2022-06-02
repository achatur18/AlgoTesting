# -*- coding: utf-8 -*-

class Plot:
    def coloured_plot(self, df, col, color_dict, s_=0, e_=-1, signal_size=4):  
        if s_==0:
            s_=-len(df)+1
            
        df['rank']=range(len(df))
        CLR=[color_dict[x] if x in color_dict.keys() else "#000000" for x in df[col]]
        s=[4]*len(df)
        for idx, val in enumerate(df[col]):
            if val!='HOLD':
                s[idx]=signal_size
        
        df[s_:e_].plot.scatter(x='rank', y="Adj Close",s=s[s_:e_], color = CLR[s_:e_])
        #df[s_:e_].plot.scatter(x='rank', y="Adj Close",s=4, color = [color_dict[x] for x in df[col]][s_:e_])

    