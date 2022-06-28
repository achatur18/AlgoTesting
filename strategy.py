# -*- coding: utf-8 -*-

class Strategy:
    def compareStrategies(self,data,  strategies=[]):
        data=self.ohlc_data
        for strategy in strategies:
            self.drop_na()
            self.implementStrategy(strategy=strategy)
            
            flag_column='flag'
            self.drop_na()
            data[flag_column] = data[flag_column].shift(1)
            data.fillna(0, inplace=True)
            
            self.calculateTradeReturns(flag_column=flag_column, output_column='return_flag')
            print("Returns on {}: {}".format(str(strategy.__name__), self.percentage_returns))
            print("Accuracy of bids on strategy", self.calculateAccuracy("return_flag"))
            print("#"*30)
