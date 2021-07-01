#from helpers import results_to_df
import bt 
import pandas as pd 


    
def results_to_df(results_list):
    df_list = [] #list of completed dataframes
    
    for x in results_list:
        string_res = x.to_csv(sep=',') #This creates string of results stats 
        df = pd.DataFrame([x.split(',') for x in string_res.split('\n')]) # Takes the string and creates a dataframe 
        nan_value = float("NaN") 
        df.replace("", nan_value, inplace=True) #lot of empty collumns in dataframe, this makes the empty go to null("NaN")
        df.dropna(how='all', axis=1, inplace=True) #delete null collumns
        df = df.dropna()

        df_list.append(df)
    
    return df_list


asset_1 = 'spy'
asset_2 = 'agg'
asset_3 = 'btc-usd'

data = bt.get(asset_1 + ',' + asset_2 + ',' + asset_3, start = '2016-12-31')


#####################################################################################################
################# STRATEGY FOR SPY AND TRADITIONAL 
#####################################################################################################
stock_dic_spy = {asset_1: 1}

stock_dic_trad = {asset_1: .60, asset_2: .4} 
        
       
strategy_spy = bt.Strategy("SP500Only", 
                    [ 
                    bt.algos.SelectAll(), 
                    bt.algos.WeighSpecified(**stock_dic_spy),
                    bt.algos.RunMonthly(),
                    bt.algos.Rebalance()]) #Creating strategy

strategy_trad = bt.Strategy("TraditionalOnly", 
                    [ 
                    bt.algos.SelectAll(), 
                    bt.algos.WeighSpecified(**stock_dic_trad),
                    bt.algos.RunMonthly(),
                    bt.algos.Rebalance()]) #Creating strategy


test = bt.Backtest(strategy_spy, data)
results_spy = bt.run(test)

test = bt.Backtest(strategy_trad, data)
results_trad = bt.run(test)



#Add line chart data to the dataframe
result_final = pd.DataFrame()

temp = results_trad._get_series(None).rebase()
result_final = pd.concat([result_final, temp], axis = 1) #result dataframe

temp = results_spy._get_series(None).rebase()
result_final = pd.concat([result_final, temp], axis = 1) #result dataframe




#Get Stats Data

results_df = results_to_df([results_trad])

print(results_df[0])

trad_return = results_df[0][1][20]
trad_risk = results_df[0][1][25]
trad_sortino = results_df[0][1][7]
trad_sharpe = results_df[0][1][6]

results_df = results_to_df([results_spy])

spy_return = results_df[0][1][20]
spy_risk = results_df[0][1][25]
spy_sortino = results_df[0][1][7]
spy_sharpe = results_df[0][1][6]







asset_3 = 'btcusd'

asset_1_alloc = .60
asset_2_alloc = .40
asset_3_alloc = 0

stats_df = pd.DataFrame(columns= ['AnnReturn', 'AnnRisk', 'SharpeRatio', 'SortinoRatio', 'ReturnTraditional', 'ReturnSP500', 'RiskTraditional',	'RiskSP500', 'SharpeTraditional', 'SharpeSP500', 'SortinoTraditional', 'SortinoSP500'])


counter = 1
for i in range(21):

    stock_dic_trad = {asset_1: asset_1_alloc, asset_2: asset_2_alloc, asset_3: asset_3_alloc} 
    
    strategy = bt.Strategy("d" + str(counter), 
                        [ 
                        bt.algos.SelectAll(), 
                        bt.algos.WeighSpecified(**stock_dic_trad),
                        bt.algos.RunMonthly(),
                        bt.algos.Rebalance()]) #Creating strategy

    test = bt.Backtest(strategy, data)
    results = bt.run(test)

    temp = results._get_series(None).rebase()
    result_final = pd.concat([result_final, temp], axis = 1) #result dataframe

    results_df = results_to_df([results])

    d_return = results_df[0][1][20]
    d_risk = results_df[0][1][25]
    d_sortino = results_df[0][1][7]
    d_sharpe = results_df[0][1][6]

    next_row = {
        'AnnReturn': d_return, 
        'AnnRisk': d_risk, 
        'SharpeRatio': d_sharpe, 
        'SortinoRatio': d_sortino, 
        'ReturnTraditional': trad_return, 
        'ReturnSP500': spy_return, 
        'RiskTraditional': trad_risk, 
        'RiskSP500': spy_risk, 
        'SharpeTraditional': trad_sharpe, 
        'SharpeSP500': spy_sharpe, 
        'SortinoTraditional': trad_sortino, 
        'SortinoSP500': spy_sortino
    }

    row_to_add = pd.Series(next_row)

    stats_df = stats_df.append(row_to_add, ignore_index= True)


    counter += 1
    asset_1_alloc -= .05
    asset_3_alloc += .05


print(stats_df)
print(result_final)