"""
plots various seasonal analyses for a given symbol

    - plotSeasonalReturns_intraday: 3x3 grid of barplots for analyzing intraday seasonal returns
    - plotSeasonalReturns_overview: 1x3 grid of barplots for a quick overview of seasonality in a symbol 
"""
import matplotlib
import math
import sys 

import datetime as dt
import interface_localDB as db
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import utils as ut

from matplotlib.dates import date2num

dbname_stock = '/workbench/historicalData/venv/saveHistoricalData/historicalData_index.db'

"""
Plots seasonal returns in a 3x3 grid
"""
def plotSeasonalReturns_intraday(seasonalReturns, intervals, symbols, titles, target = 'close'):
    # create a grid of symbols & intervals to draw the plots into 
    # col x rows : interval x symbol 
    title = 'Intraday Seasonal Returns for %s' % symbols[0]
    numCols = 3
    numRows = 3

    # setup figure and axes
    fig, axes = plt.subplots(nrows=numRows, ncols=numCols, figsize=(numCols*6, numRows*4.2))

    # set title for figure
    fig.suptitle(title)
    # bar plot for ALL history: i.e. seasonalReturns[0]
    sns.barplot(x=seasonalReturns[0].index, y='pctChange_std', data=seasonalReturns[0], ax=axes[0,0], color='grey', alpha=0.5)
    sns.barplot(x=seasonalReturns[0].index, y='pctChange_mean', data=seasonalReturns[0], ax=axes[0,0].twinx(), color='red')
    axes[0,0].set_title(titles[0]) # set title for subplot
    axes[0,0].set_xlabel('') # hide x axis title
    
    
    # bar plot for last 60 days: i.e. seasonalReturns[1]
    sns.barplot(x=seasonalReturns[1].index, y='pctChange_std', data=seasonalReturns[1], ax=axes[0,1], color='grey', alpha=0.5)
    sns.barplot(x=seasonalReturns[1].index, y='pctChange_mean', data=seasonalReturns[1], ax=axes[0,1].twinx(), color='red')
    axes[0,1].set_title(titles[1]) # set title for subplot
    axes[0,1].set_xlabel('') # hide x axis title

    #bar plot for last 90 days: i.e. seasonalReturns[2]
    sns.barplot(x=seasonalReturns[2].index, y='pctChange_std', data=seasonalReturns[2], ax=axes[0,2], color='grey', alpha=0.5)
    sns.barplot(x=seasonalReturns[2].index, y='pctChange_mean', data=seasonalReturns[2], ax=axes[0,2].twinx(), color='red')
    axes[0,2].set_title(titles[2]) # set title for subplot
    axes[0,2].set_xlabel('') # hide x axis title

    # bar plot of last 30 days: i.e. seasonalReturns[3]
    sns.barplot(x=seasonalReturns[3].index, y='pctChange_std', data=seasonalReturns[3], ax=axes[1,0], color='grey', alpha=0.5)
    sns.barplot(x=seasonalReturns[3].index, y='pctChange_mean', data=seasonalReturns[3], ax=axes[1,0].twinx(), color='red')
    axes[1,0].set_title(titles[3]) # set title for subplot
    axes[1,0].set_xlabel('') # hide x axis title

    # bar plof of prev 30 days: i.e. seasonalReturns[4]
    sns.barplot(x=seasonalReturns[4].index, y='pctChange_std', data=seasonalReturns[4], ax=axes[1,1], color='grey', alpha=0.5)
    sns.barplot(x=seasonalReturns[4].index, y='pctChange_mean', data=seasonalReturns[4], ax=axes[1,1].twinx(), color='red')
    axes[1,1].set_title(titles[4]) # set title for subplot
    axes[1,1].set_xlabel('') # hide x axis title

    # bar plot of prev 60 days: i.e. seasonalReturns[5]
    sns.barplot(x=seasonalReturns[5].index, y='pctChange_std', data=seasonalReturns[5], ax=axes[1,2], color='grey', alpha=0.5)
    sns.barplot(x=seasonalReturns[5].index, y='pctChange_mean', data=seasonalReturns[5], ax=axes[1,2].twinx(), color='red')
    axes[1,2].set_title(titles[5]) # set title for subplot
    axes[1,2].set_xlabel('') # hide x axis title

    sns.heatmap(seasonalReturns[6].pivot_table(index=seasonalReturns[6]['date'].dt.time, columns=seasonalReturns[6]['date'].dt.date, values='pctChange'), ax=axes[2,0])
    axes[2,0].set_title(titles[6])

    sns.heatmap(seasonalReturns[7].pivot_table(index=seasonalReturns[7]['date'].dt.time, columns=seasonalReturns[7]['date'].dt.date, values='pctChange'), ax=axes[2,1])
    axes[2,1].set_title(titles[7])

    sns.heatmap(seasonalReturns[8].pivot_table(index=seasonalReturns[8]['date'].dt.time, columns=seasonalReturns[8]['date'].dt.date, values='pctChange'), ax=axes[2,2])
    axes[2,2].set_title(titles[8])

    # tilt x axis labels 90 degrees
    axes[0,0].set_xticklabels(axes[0,0].get_xticklabels(), rotation=90, fontsize=8)
    axes[0,1].set_xticklabels(axes[0,0].get_xticklabels(), rotation=90, fontsize=8)
    axes[0,2].set_xticklabels(axes[0,0].get_xticklabels(), rotation=90, fontsize=8)
    axes[1,0].set_xticklabels(axes[0,0].get_xticklabels(), rotation=90, fontsize=8)
    axes[1,1].set_xticklabels(axes[0,0].get_xticklabels(), rotation=90, fontsize=8)
    axes[1,2].set_xticklabels(axes[0,0].get_xticklabels(), rotation=90, fontsize=8)

    axes[0,0].set_xticks(axes[0,0].get_xticks()[::3])
    axes[0,1].set_xticks(axes[0,1].get_xticks()[::3])
    axes[0,2].set_xticks(axes[0,2].get_xticks()[::3])
    axes[1,0].set_xticks(axes[1,0].get_xticks()[::3])
    axes[1,1].set_xticks(axes[1,1].get_xticks()[::3])
    axes[1,2].set_xticks(axes[1,2].get_xticks()[::3])

    # set margin of the figure
    plt.subplots_adjust(hspace=0.3, wspace=0.4, left=0.05, right=0.95, top=0.95, bottom=0.09)


""" 
Plots seasonal returns as per the following: 
    - weekly using 1day interval
    - monthly using 1day interval
    - intraday using 5min interval

    Inputs:
        - Symbol (str)
"""
def seasonalAnalysis_overview(symbol, restrictTradingHours=False, target='close'):
    # get px history from db
    with db.sqlite_connection(dbname_stock) as conn:
        pxHistory_1day = db.getPriceHistory(conn, symbol, '1day', withpctChange=True)
        pxHistory_5mins = db.getPriceHistory(conn, symbol, '5mins', withpctChange=True)

    # restrict trading hours to 9:30am to 4pm
    if restrictTradingHours:
        pxHistory_5mins = pxHistory_5mins[(pxHistory_5mins['date'].dt.time >= dt.time(9, 30)) & (pxHistory_5mins['date'].dt.time <= dt.time(15, 55))]
    
    # get seasonal aggregates for plotting 
    seasonalAggregate_1day = getSeasonalAggregate(pxHistory_1day, '1day', symbol)
    seasonalAggregate_5mins = getSeasonalAggregate(pxHistory_5mins, '5mins', symbol)
    seasonalAggregate_weekByDay = getSeasonalAggregate(pxHistory_5mins, 'weekByDay', symbol)
    seasonalAggregate_yearByMonth = getSeasonalAggregate(pxHistory_1day, 'yearByMonth', symbol)

    # get log returns for pxhistory 
    logReturn = ut.calcLogReturns(pxHistory_1day, 'close')
    seasonalAggregate_weekByDay_logReturns = ut.aggregate_by_month(logReturn, 'logReturn')

    ## construct figure and plots 

    # set up figure and axes with a 1x3 grid
    fig, axes = plt.subplots(2, 3, figsize=(17, 7))

    # add title to figure
    fig.suptitle('Overview of Seasonal Returns for %s (%s years of data)'%(symbol, round(len(pxHistory_1day)/252, 1)))
    
    #
    # plot monthly seasonality
    #
    # on axes[0,0] barplot of seasonalAggregate_1day mean, and std dev with a secondary axis for mean
    sns.barplot(x=seasonalAggregate_1day.index, y='pctChange_std', data=seasonalAggregate_1day, ax=axes[0,0], color='grey', alpha=0.5)
    sns.barplot(x=seasonalAggregate_1day.index, y='pctChange_mean', data=seasonalAggregate_1day, ax=axes[0,0].twinx(), color='red')
    axes[0,0].set_title('Monthly Seasonality') # set title for subplot
    axes[0,0].set_xlabel('Day of Month')
    # show every second x tick label
    axes[0,0].set_xticks(axes[0,0].get_xticks()[::2])

    #
    # plot intra day seasonality 
    #
    # on axes[1] barplot of seasonalAggregate_5mins mean, and std dev with a secondary axis for mean
    sns.barplot(x=seasonalAggregate_5mins.index, y='pctChange_std', data=seasonalAggregate_5mins, ax=axes[0,1], color='grey', alpha=0.5)
    sns.barplot(x=seasonalAggregate_5mins.index, y='pctChange_mean', data=seasonalAggregate_5mins, ax=axes[0,1].twinx(), color='red')
    axes[0,1].set_title('Intra-Day Seasonality') # set title for subplot

    # given that xticks are a Text Object formatted as 'HH:MM:SS', reformat the xtick labels to 'HH:MM'
    axes[0,1].set_xticklabels([x.get_text()[:5] for x in axes[0,1].get_xticklabels()])

    # show every second x tick label
    axes[0,1].set_xticks(axes[0,1].get_xticks()[::8])

    ## add vertical line at with x valus of 10:00:00, 11:30, 1:00, 2:00, 3:00
    if restrictTradingHours:
        axes[0,1].axvline(x=6, color='black', linestyle='--')
        axes[0,1].axvline(x=23, color='black', linestyle='--')
        axes[0,1].axvline(x=40, color='black', linestyle='--')
        axes[0,1].axvline(x=53, color='black', linestyle='--')
        axes[0,1].axvline(x=66, color='black', linestyle='--')
    else:
        axes[0,1].axvline(x=32, color='black', linestyle='--')
        axes[0,1].axvline(x=52, color='black', linestyle='--')
        axes[0,1].axvline(x=82, color='black', linestyle='--')
        axes[0,1].axvline(x=102, color='black', linestyle='--')
    
    #
    # plot weekly seasonality
    #
    # on axes[2] barplot of seasonalAggregate_weekByDay mean, and std dev with a secondary axis for mean
    sns.barplot(x=seasonalAggregate_weekByDay.index, y='pctChange_std', data=seasonalAggregate_weekByDay, ax=axes[0,2], color='grey', alpha=0.5)
    sns.barplot(x=seasonalAggregate_weekByDay.index, y='pctChange_mean', data=seasonalAggregate_weekByDay, ax=axes[0,2].twinx(), color='red')
    axes[0,2].set_title('Weekly Seasonality') # set title for subplot
    # hide xaxis label
    axes[0,2].set_xlabel('Day of Week')

    # set xaxis tick labels to day of the week
    axes[0,2].set_xticklabels(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])

    #
    # Plot year by month seasonality 
    #
    # on axes[1] barplot of seasonalAggregate_yearByMonth mean, and std dev with a secondary axis for mean
    sns.barplot(x=seasonalAggregate_yearByMonth.index, y='pctChange_std', data=seasonalAggregate_yearByMonth, ax=axes[1,0], color='grey', alpha=0.5)    
    sns.barplot(x=seasonalAggregate_yearByMonth.index, y='pctChange_mean', data=seasonalAggregate_yearByMonth, ax=axes[1,0].twinx(), color='red')
    axes[1,0].set_title('Yearly Seasonality') # set title for subplot
    # hide xaxis label
    axes[1,0].set_xlabel('')
    # set xaxis tick labels to month of the year
    axes[1,0].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    ## 
    # plot week by day aggregate logreturns
    #
    #
    # add sd as grey barplot on a secondary axis 
    sns.barplot(x=seasonalAggregate_weekByDay_logReturns.index, y='std', data=seasonalAggregate_weekByDay_logReturns, ax=axes[1,1], color='grey', alpha=0.5)

    sns.barplot(x=seasonalAggregate_weekByDay_logReturns.index, y='mean', data=seasonalAggregate_weekByDay_logReturns, ax=axes[1,1].twinx(), color='red', alpha=1)
    axes[1,1].set_title('Yearly Seasonality (Log Returns)') # set title for subplot
    axes[1,1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])


## this function plots a 3 x 3 grid of plots of log returns for various seasonalities 
def logReturns_overview_of_seasonality(symbol, restrictTradingHours=False):
    # get px history from db
    with db.sqlite_connection(dbname_stock) as conn:
        pxHistory_1day = db.getPriceHistory(conn, symbol, '1day', withpctChange=True)
        pxHistory_5mins = db.getPriceHistory(conn, symbol, '30mins', withpctChange=True)

    ###############################################
    # restrict trading hours to 9:30am to 4pm
    ###############################################
    if restrictTradingHours:
        pxHistory_5mins = pxHistory_5mins[(pxHistory_5mins['date'].dt.time >= dt.time(9, 30)) & (pxHistory_5mins['date'].dt.time <= dt.time(15, 55))]
    ###############################################
    ###############################################

    # get log returns for pxhistory
    logReturn_1day = ut.calcLogReturns(pxHistory_1day, 'close')
    logReturn_5mins = ut.calcLogReturns(pxHistory_5mins, 'close')
    
    # create figure, and axes
    fig, axes = plt.subplots(2, 3, figsize=(19, 9))

    ## ADD TITLE
    fig.suptitle('Log Return Seasonality for %s (%s years of data)'%(symbol.upper(), round(len(pxHistory_1day)/252, 1)))

    ### plot aggregate log returns for each month of the year
    seasonalAggregate_yearByMonth_logReturns_1day = ut.aggregate_by_month(logReturn_1day, 'logReturn')

    # plot seasonalAggregate_yearByMonth_logReturns_1day sd and mean, mean in red and alpha = 1, sd on secondary axis with alpha = 0.5

    sns.barplot(x=seasonalAggregate_yearByMonth_logReturns_1day.index, y='std', data=seasonalAggregate_yearByMonth_logReturns_1day, ax=axes[0,0], color='grey', alpha=0.5)
    sns.barplot(x=seasonalAggregate_yearByMonth_logReturns_1day.index, y='mean', data=seasonalAggregate_yearByMonth_logReturns_1day, ax=axes[0,0].twinx(), color='red', alpha=1)
    axes[0,0].set_title('Yearly Seasonality') # set title for subplot
    axes[0,0].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    ######
    ## day of month 
    ######
    aggregate_day_of_month = ut.aggregate_by_dayOfMonth(logReturn_1day, 'logReturn')
    # plot the mean and sd 
    sns.barplot(x=aggregate_day_of_month.index, y='std', data=aggregate_day_of_month, ax=axes[0,1], color='grey', alpha=0.5)
    sns.barplot(x=aggregate_day_of_month.index, y='mean', data=aggregate_day_of_month, ax=axes[0,1].twinx(), color='red', alpha=1)
    axes[0,1].set_title('Day of Month Seasonality') # set title for subplot
    axes[0,1].set_xlabel('Day of Month')
    # show every second x tick label
    axes[0,1].set_xticks(axes[0,1].get_xticks()[::2])

    ######
    ## day of week
    ######
    aggregate_day_of_week = ut.aggregate_by_dayOfWeek(logReturn_1day, 'logReturn')
    # plot the mean and sd
    sns.barplot(x=aggregate_day_of_week.index, y='std', data=aggregate_day_of_week, ax=axes[0,2], color='grey', alpha=0.5)
    sns.barplot(x=aggregate_day_of_week.index, y='mean', data=aggregate_day_of_week, ax=axes[0,2].twinx(), color='red', alpha=1)
    axes[0,2].set_title('Day of Week Seasonality') # set title for subplot
    axes[0,2].set_xlabel('Day of Week')
    # set xaxis tick labels to day of the week
    axes[0,2].set_xticklabels(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])

    ## get aggregate by timestamp for 5min interval
    aggregate_timestamp_5mins = ut.aggregate_by_timestamp(logReturn_5mins, 'logReturn')
    
    # plot the mean and sd
    sns.barplot(x=aggregate_timestamp_5mins.index, y='std', data=aggregate_timestamp_5mins, ax=axes[1,0], color='grey', alpha=0.5)
    sns.barplot(x=aggregate_timestamp_5mins.index, y='mean', data=aggregate_timestamp_5mins, ax=axes[1,0].twinx(), color='red', alpha=1)
    axes[1,0].set_title('Intra-Day Seasonality') # set title for subplot
    axes[1,0].set_xlabel('Time of Day')
    # set xtick labels to 'timestamp' column of aggregate_timestamp_5mins
    # tilt xticks 90 degrees
    axes[1,0].set_xticklabels(aggregate_timestamp_5mins['timestamp'], rotation=90, fontsize=8)

    # aggregate restricted hours only 
    logReturn_5mins_restricted = logReturn_5mins[(logReturn_5mins['date'].dt.time >= dt.time(9, 30)) & (logReturn_5mins['date'].dt.time <= dt.time(15, 55))]
    aggregate_logReturn_5mins_restricted = ut.aggregate_by_timestamp(logReturn_5mins_restricted, 'logReturn')
    
    # plot the mean and sd
    sns.barplot(x=aggregate_logReturn_5mins_restricted.index, y='std', data=aggregate_logReturn_5mins_restricted, ax=axes[1,1], color='grey', alpha=0.5)
    sns.barplot(x=aggregate_logReturn_5mins_restricted.index, y='mean', data=aggregate_logReturn_5mins_restricted, ax=axes[1,1].twinx(), color='red', alpha=1)
    axes[1,1].set_title('Intra-Day Seasonality (Restricted Hours)') # set title for subplot
    axes[1,1].set_xlabel('Time of Day')
    # set xtick labels to 'timestamp' column of aggregate_timestamp_5mins
    # tilt xticks 90 degrees
    axes[1,1].set_xticklabels(aggregate_logReturn_5mins_restricted['timestamp'], rotation=90, fontsize=8)
    ## now plot the same but drop timestamps not between 9:30 to 16:00 
    #aggregate_timestamp_5mins_restrictedHours = aggregate_timestamp_5mins[(aggregate_timestamp_5mins['timestamp'] >= dt.time(9, 30)) & (aggregate_timestamp_5mins['timestamp'] <= dt.time(15, 55))]
    #print(aggregate_timestamp_5mins_restrictedHours)



"""
Returns seasonal aggregate of passed in pxhistory df
"""
def getSeasonalAggregate(pxHistory, interval, symbol, numdays=0):
    
    # if numdays >0, then only aggregate data for last numdays
    if numdays > 0:
        pxHistory = pxHistory[pxHistory['date'] > (pxHistory['date'].max() - pd.Timedelta(days=numdays))]
    
    # aggregate by time and compute mean and std dev of %change
    if interval in ['1min', '5mins', '15mins', '30mins', '1hour']:
        
        pxHistory_aggregated = pxHistory.groupby(pxHistory['date'].dt.time).agg({'pctChange':['mean', 'std']})
        
        # drop the row where the time component of the date column = 9:30:00
        #pxHistory_aggregated = pxHistory_aggregated.drop(pd.to_datetime('9:30:00').time())
        #print(pxHistory_aggregated)
        #exit()

    elif interval in ['1day', '1week', '1month']:
        pxHistory_aggregated = pxHistory.groupby(pxHistory['date'].dt.day).agg({'pctChange':['mean', 'std']})
    
    elif interval in ('weekByDay'):
        pxHistory_aggregated = pxHistory.groupby(pxHistory['date'].dt.dayofweek).agg({'pctChange':['mean', 'std']})
    
    elif interval in ('yearByMonth'):
        
        # reset index so we can use the Date column to agg 
        pxHistory.reset_index(inplace=True)
        # group pxhistory by (year, month) and get the min and max Date in each group 
        pxHistory_monthly = pxHistory.groupby([pxHistory['date'].dt.year, pxHistory['date'].dt.month]).agg({'date':['min', 'max']})
        #rename index columns to year and month
        pxHistory_monthly.index.names = ['year', 'month']

        # flatten multi-index columns
        pxHistory_monthly.columns = ['_'.join(col).strip() for col in pxHistory_monthly.columns.values]
        # reset index
        pxHistory_monthly.reset_index(inplace=True)

        ## calc the percent change between the first and last trading day of each month:
        ##  1. given pxHistoroy contains the close price for any given Date 
        ##  2. Add a column to pxHistory_monthly that is the percent change of the close price between Date_min and Date_max
        ##  3. group by month and calculate the mean and std dev of pctChange
        pxHistory_monthly['pctChange'] = pxHistory_monthly.apply(lambda row: (pxHistory[(pxHistory['date'] == row['date_max'])]['close'].values[0] - pxHistory[(pxHistory['date'] == row['date_min'])]['close'].values[0])/pxHistory[(pxHistory['date'] == row['date_min'])]['close'].values[0], axis=1)

        pxHistory_aggregated = pxHistory_monthly.groupby('month').agg({'pctChange':['mean', 'std']})
    else:
        print('aggreagation not supported for interval: '+interval)

    # flatten multi-index columns
    pxHistory_aggregated.columns = ['_'.join(col).strip() for col in pxHistory_aggregated.columns.values]

    # add symbol and interval to aggregated df 
    pxHistory_aggregated['symbol'] = symbol
    pxHistory_aggregated['interval'] = interval

    return pxHistory_aggregated

"""
Runs seasonal analysis on intra-day data for a given symbol and interval
    plots different subsets of data: all, last 30 days, last 60 days, last 90 days 
"""
def seasonalAnalysis_intraday(symbol, interval, target='close'):
    ## gracefully exit with error if interval not in 1min, 5mins, 15mins, 30mins, 1hour
    if interval not in ['1min', '5mins', '15mins', '30mins', '1hour']:
        print('ERROR: interval not supported for intraday analysis')
        exit()
    
    with db.sqlite_connection(dbname_stock) as conn:
        pxHistory = db.getPriceHistory(conn, symbol, interval)

    if restrictTradingHours:
        # given that the Date column is a datetime object
        # select only the rows with time between 9:30am and 4pm
        pxHistory = pxHistory[(pxHistory['date'].dt.time >= dt.time(9, 30)) & (pxHistory['date'].dt.time <= dt.time(15, 55))]
   
    # get mean and std for aggregated data
    pxHistory_aggregated = getSeasonalAggregate(pxHistory, interval, symbol)

    # select only aggregated data of last 60 days
    pxHistory60 = pxHistory[pxHistory['date'] > (pxHistory['date'].max() - pd.Timedelta(days=60))]
    pxhistory60_aggregated = getSeasonalAggregate(pxHistory60, interval, symbol)

    # select last 30 days of data from pxhistory 
    pxHistory30 = pxHistory[pxHistory['date'] > (pxHistory['date'].max() - pd.Timedelta(days=30))]
    pxhistory30_aggregated = getSeasonalAggregate(pxHistory30, interval, symbol)

    # select last 90 days of data from pxhistory 
    pxHistory90 = pxHistory[pxHistory['date'] > (pxHistory['date'].max() - pd.Timedelta(days=90))]
    pxhistory90_aggregated = getSeasonalAggregate(pxHistory90, interval, symbol)

    # select aggregated data for last 30, prev 30, 
    # and prev prev 30 days of data from pxhistory
    pxHistory302 = pxHistory[(pxHistory['date'] < (pxHistory30['date'].min())) & (pxHistory['date'] > (pxHistory30['date'].min() - pd.Timedelta(days=31)))]
    pxHistory303 = pxHistory[(pxHistory['date'] < pxHistory302['date'].min()) & (pxHistory['date'] > pxHistory302['date'].min() - pd.Timedelta(days=31))]
    pxhistory302_aggregated = getSeasonalAggregate(pxHistory302, interval, symbol)
    pxhistory303_aggregated = getSeasonalAggregate(pxHistory303, interval, symbol)

    ## plot the results 
    plotSeasonalReturns_intraday(
    [
        pxHistory_aggregated, pxhistory60_aggregated, pxhistory90_aggregated, 
        pxhistory30_aggregated, pxhistory302_aggregated, pxhistory303_aggregated, pxHistory30, pxHistory302, pxHistory303],
          
          [interval, interval, interval, 
           interval, interval, interval, 
           interval, interval, interval], 
           
           [symbol, symbol, symbol, 
            symbol, symbol, symbol,
            symbol, symbol, symbol], 
            
            ['Starting from %s'%(pxHistory['date'].min().date()), 
             'Last %s Days'%(len(pd.bdate_range(pxHistory60.index.min(), pxHistory60.index.max()))),
              'Last %s Days'%(len(pd.bdate_range(pxHistory90.index.min(), pxHistory90.index.max()))),
             'From %s to %s'%(pxHistory30['date'].min().date(), pxHistory30['date'].max().date()), 
             'From %s to %s'%(pxHistory302['date'].min().date(), pxHistory302['date'].max().date()), 
             'From %s to %s'%(pxHistory303['date'].min().date(), pxHistory303['date'].max().date()),
             'From %s to %s'%(pxHistory30['date'].min().date(), pxHistory30['date'].max().date()),
              'From %s to %s'%(pxHistory302['date'].min().date(), pxHistory302['date'].max().date()),
               'From %s to %s'%(pxHistory303['date'].min().date(), pxHistory303['date'].max().date()) ])

## function that lists all the unique symbols in the db
def listSymbols():
    with db.sqlite_connection(dbname_stock) as conn:
        symbols = db.listSymbols(conn)
    print('Symbols in DB:')
    print(symbols)

## get timeseries data from db
symbol = 'spy'
# set symbol to cli arg if provided
if len(sys.argv) > 1:
    ## if the argument is 'list' then list all the symbols in the db
    if sys.argv[1] == 'list':
        listSymbols()
        exit()
    symbol = sys.argv[1]
interval = '30mins'
target = 'close' # open, high, low, close, volume
restrictTradingHours = True # if true -> only analyze data between 9:30am and 4pm

#seasonalAnalysis_intraday(symbol, interval, target, restrictTradingHours)
#seasonalAnalysis_overview(symbol, restrictTradingHours, target)

logReturns_overview_of_seasonality(symbol)

plt.tight_layout()
plt.show()

