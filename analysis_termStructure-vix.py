import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## local libs
import interface_localDB as db
import termStructure_vix as vixts

### CONFIG ### 
vvix_topPercentile = 0.9
vvix_bottomPercentile = 0.1
vvix_percentileLookbackDays = 252 ## 1 year lookback = 252 trading days

## prepare vix term structure data 
vix_ts_pctContango = vixts.getVixTermStructurePctContango(fourToSeven=True, currentToLast=True, averageContango=True)
## add a column that is 'contango' if fourToSevenMoContango is positive, 'backwardation' if negative
#vix_ts_pctContango['firstToLastTermStruct'] = vix_ts_pctContango['currentToLastContango'].apply(lambda x: 'contango' if x > 0 else 'backwardation')

## prepare price history data
###################################
# VIX  ############################
vix = db.getPriceHistory('VIX', '1day', withpctChange=True)

## make sure vix and vix_ts_pctContango start on the same date
#vix = vix[vix.index >= vix_ts_pctContango.index.min()]

###################################
# VVIX ############################
vvix = db.getPriceHistory('VVIX', '1day')

##  make sure vvix and vix_ts_pctContango start on the same date 
#vvix = vvix[vvix.index >= vix_ts_pctContango.index.min() - pd.Timedelta(days=252)]

## calculate percentile rank of VVIX
vvix['percentileRank'] = vvix['close'].rolling(vvix_percentileLookbackDays).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])

############## Final cleanup ... ################
# reset index to eliminate duplicate indices resulting from joins 
vix_ts_pctContango.reset_index(inplace=True)
# make sure vix and vix_ts_pctContango start on the same date
#vix = vix[vix.index >= vix_ts_pctContango['Date'].min()]

## from vix_ts_pctContango remove any dates that are not in vix and vvix
vix_ts_pctContango = vix_ts_pctContango[vix_ts_pctContango['Date'].isin(vix.index) & vix_ts_pctContango['Date'].isin(vvix.index)]

# from vvix remove any dates that are not in vix and vix_ts_pctContango
vvix = vvix[vvix.index.isin(vix.index) & vvix.index.isin(vix_ts_pctContango['Date'])]

# from vix remove any dates that are not in vvix and vix_ts_pctContango
vix = vix[vix.index.isin(vvix.index) & vix.index.isin(vix_ts_pctContango['Date'])]

## plot the relationships between vix term structure and vix price history
# arguments:
#  vix_ts_pctContango: the vix term structure data
#  vix: the vix price history data
# then generates a 1x3 figure with the following subplots:
#  1. scatter of fourToSevenMoContango vs. VIX close_pctChange
#  2. scatter of avgContango vs. VIX close_pctChange
#  3. scatter of vvix percentileRank vs. VIX close_pctChange
# notes: 
#  - vix pct change is shifted by 1 day so the scatters represent the
#    relationship with  next day's return
def plotVixRelationships(vix_ts_pctContango, vix, vvix):
   
    fig2, ax2 = plt.subplots(1, 3, figsize=(15, 5))
    fig2.suptitle('Contango & VIX next day returns')
    
    # shift vix by 1 day for next day returns
    vix['close_pctChange'] = vix['close_pctChange'].shift(-1)

    # plot fourToSevenMoContango vs. VIX close_pctChange
    sns.scatterplot(x=vix_ts_pctContango['fourToSevenMoContango'], y=vix['close_pctChange'], ax=ax2[0])
    sns.regplot(x=vix_ts_pctContango['fourToSevenMoContango'], y=vix['close_pctChange'], ax=ax2[0], line_kws={'color': 'red'})
    ax2[0].set_title('4-7 Mo Contango')

    # plot avgContango vs. VIX close_pctChange
    sns.scatterplot(x=vix_ts_pctContango['averageContango'], y=vix['close_pctChange'], ax=ax2[1])
    sns.regplot(x=vix_ts_pctContango['averageContango'], y=vix['close_pctChange'], ax=ax2[1], line_kws={'color': 'red'})
    ax2[1].set_title('Avg Contango')

    # plot vvix percentileRank vs. VIX close_pctChange
    sns.scatterplot(x=vvix['percentileRank'], y=vix['close_pctChange'], ax=ax2[2])
    sns.regplot(x=vvix['percentileRank'], y=vix['close_pctChange'], ax=ax2[2], line_kws={'color': 'red'})
    ax2[2].set_title('VVIX Percentile Rank')
    # reverse x axis
    ax2[2].invert_xaxis()

"""
Acts as a main view for day to day monitoring of VIX term structure changes. The following are displayed:
    - VIX: 4-7 month contango, and percentile rank of vvix
    - VIX: close 
    - VIX close pct change vs. vvix percentile rank scatter
"""
def plotVixTermStructureMonitor(vix_ts_pctContango, vix, vvix):
    # using seaborn, create figure with 2 subplots
    fig, ax = plt.subplots(3, 1, figsize=(15, 10))

    # set title
    fig.suptitle('VIX Term Structure')

    # plot fourtosevenMoContango, and percentile rank of vvix
    sns.lineplot(x='Date', y='fourToSevenMoContango', data=vix_ts_pctContango, ax=ax[0])
    sns.lineplot(x=vvix.index, y='percentileRank', data=vvix, ax=ax[0].twinx(), drawstyle='steps-pre', color='red')
    #add black line at 0
    ax[0].axhline(y=0, color='black', linestyle='-')
    ax[0].set_title('4th to 7th Month Contango')
    
    ## plot vix close
    sns.lineplot(x='Date', y='close', data=vix, ax=ax[1])
    
    ## x-axes of both plots start on the same date (easier to compare)
    ax[1].set_xlim(ax[0].get_xlim())

    ## plot scatter of vvix percentileRank vs vix next day return
    
    # shift vix by 1 day for next day returns 
    vix['close_pctChange']= vix['close_pctChange'].shift(-1)

    ## join vvix percentileRank with vix close_pctChange 
    vvix = vvix.join(vix['close_pctChange'], on='Date')

    ## plot the scatter with line of best fit
    sns.scatterplot(x=vvix['percentileRank'], y=vvix['close_pctChange'], data=vvix, ax=ax[2])
    #sns.scatterplot(x='percentileRank', y='close_pctChange', data=vvix, ax=ax[2])
    sns.regplot(x='percentileRank', y='close_pctChange', data=vvix, scatter=False, ax=ax[2], line_kws={'color': 'red'})
    ax[2].set_title('VVIX Percentile Rank vs VIX Close Pct Change')



##################################################
############### Plot Scatters, histograms, etc. 
##################################################

# set seaborn style
sns.set()
sns.set_style('darkgrid')

plotVixRelationships(vix_ts_pctContango, vix, vvix)
plotVixTermStructureMonitor(vix_ts_pctContango, vix, vvix)

plt.tight_layout()
plt.show()