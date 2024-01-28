# Dataframe A with a column to be used as the "signal"
#    assume the signal df has close px to calculate fwd returrns 
# add n number of forward returns columns
# round signal column to n decimal places, or otherwise bucket it to calculate the mean fwd returns on
# calculate means for each fwdreturn column grouped by signal column
# 

"""
    Calculates autocrrelations for a given dataframe and target column
"""
def calculateAutocorrelations(df, targetColName, max_lag=60):
    # calculate autocorrelations
    autocorrelations = []
    for i in range(1, max_lag + 1):
        autocorrelations.append(df[targetColName].autocorr(lag=i))
    return autocorrelations

"""
    Buckets by signal and calculates the mean fwdReturns for each period 
    inputs:
        signaldf: dataframe with a column to be used as the "signal", and close px to calculate fwd returrns
        signal_col: identifies the column to be used as the signal 
        signal_rounding: (optional) Round the signal column to n decimal places, default is 2
        maxperiod_fwdreturns: (optional) number of fwd returns columns to add to the dataframe, default 2
"""
def bucketAndCalcSignalReturns(signaldf, signal_col, signal_rounding=2, maxperiod_fwdreturns=50):
    
    signaldf.dropna(subset=['signal'], inplace=True)
    
    # add fwdreturn column for each fwdreturn period
    for i in range(1, maxperiod_fwdreturns+1):
        if 'fwdReturns%s'%(i) in signaldf.columns: # skip if col exists
            continue
        signaldf['fwdReturns%s'%(i)] = signaldf['close'].pct_change(i).shift(-i)
    # strip 'fwdReturns' from the column names
    
    # round signal column to n decimal places, or otherwise bucket it to calculate the mean fwd returns on
    signaldf['%s_normalized'%(signal_col)] = signaldf[signal_col].round(signal_rounding) #.apply(lambda x: round(x, signal_rounding))
    
    # List of column names for fwdReturns
    fwd_returns_cols = ['fwdReturns{}'.format(i) for i in range(1, maxperiod_fwdreturns + 1)]

    # Perform the groupby and mean calculation in one step
    signal_meanReturns = signaldf.groupby('%s_normalized'%(signal_col))[fwd_returns_cols].mean()
    signal_meanReturns.sort_index(inplace=True, ascending=False) # transpose so that fwdReturns are columns



    return signal_meanReturns