import numpy as np
import pandas as pd

def frxUSDRates(utilization_rate, borrowRate, sfrxusdInterestRate):
    return  {
        'lentAPR': borrowRate * utilization_rate,
        'unlentAPR': 0,
        'borrowAPR': borrowRate
    };

def sfrxUSDRates(utilization_rate, borrowRate, sfrxusdInterestRate):
    # lentAPR = ((1 + borrowRate) / (1 + sfrxusdInterestRate)) - 1
    return {
        'lentAPR': borrowRate * utilization_rate,
        'unlentAPR': sfrxusdInterestRate * (1 - utilization_rate),
        'borrowAPR': borrowRate
    }


def getRates(utilization_rate, borrowRate, sfrxusdInterestRate):
    return {
        'frxUSDRates': frxUSDRates(utilization_rate, borrowRate, sfrxusdInterestRate),
        'sfrxUSDRates': sfrxUSDRates(utilization_rate, borrowRate, sfrxusdInterestRate)
    }

def calcfrxUSDBorrowRate(utilization_rate, lendRate, sfrxusdInterestRate):
    return  {
        'lentAPR': lendRate,
        'unlentAPR': 0,
        'borrowAPR': lendRate / (utilization_rate)
    };

def calcsfrxUSDBorrowRate(utilization_rate, lendRate, sfrxusdInterestRate):
    borrowRate = (lendRate - (sfrxusdInterestRate * (1 - utilization_rate))) / utilization_rate
    return {
        'lentAPR': borrowRate * utilization_rate,
        'unlentAPR': sfrxusdInterestRate * (1 - utilization_rate),
        'borrowAPR': borrowRate
    }

def getBorrowRates(utilization_rate, lendRate, sfrxusdInterestRate):
    return {
        'frxUSDRates': calcfrxUSDBorrowRate(utilization_rate, lendRate, sfrxusdInterestRate),
        'sfrxUSDRates': calcsfrxUSDBorrowRate(utilization_rate, lendRate, sfrxusdInterestRate)
    }

def generate_apr_comparison_data(current_interest_rate=0.05, sfrxusd_interest_rate=0.04):
    """
    Generate APR data for frxUSD and sfrxUSD markets across different utilization rates.
    
    Args:
        current_interest_rate (float): The current interest rate
        sfrxusd_interest_rate (float): The sfrxUSD interest rate
    
    Returns:
        tuple: (DataFrame containing APR data, DataFrame containing borrow rates)
    """
    # Generate utilization rates from 0 to 1
    utilization_rates = np.linspace(0, 1, 21)  # 5% increments
    
    data = []
    borrow_rates = []
    for util in utilization_rates:
        rates = getRates(util, current_interest_rate, sfrxusd_interest_rate)
        
        # Add frxUSD data
        data.append({
            'utilization_rate': util,
            'market': 'frxUSD',
            'apr_type': 'lentAPR',
            'value': rates['frxUSDRates']['lentAPR']
        })
        data.append({
            'utilization_rate': util,
            'market': 'frxUSD',
            'apr_type': 'unlentAPR',
            'value': rates['frxUSDRates']['unlentAPR']
        })
        
        # Add sfrxUSD data
        data.append({
            'utilization_rate': util,
            'market': 'sfrxUSD',
            'apr_type': 'lentAPR',
            'value': rates['sfrxUSDRates']['lentAPR']
        })
        data.append({
            'utilization_rate': util,
            'market': 'sfrxUSD',
            'apr_type': 'unlentAPR',
            'value': rates['sfrxUSDRates']['unlentAPR']
        })
        
        # Add borrow rates
        borrow_rates.append({
            'utilization_rate': util,
            'market': 'frxUSD',
            'value': rates['frxUSDRates']['borrowAPR']
        })
        borrow_rates.append({
            'utilization_rate': util,
            'market': 'sfrxUSD',
            'value': rates['sfrxUSDRates']['borrowAPR']
        })
    
    return pd.DataFrame(data), pd.DataFrame(borrow_rates)

def generate_fixed_util_apr_data(utilization_rate=0.85, sfrxusd_interest_rate=0.04, max_borrow_rate=0.20):
    """
    Generate APR data for frxUSD and sfrxUSD markets across different borrow rates at fixed utilization.
    
    Args:
        utilization_rate (float): Fixed utilization rate (default 85%)
        sfrxusd_interest_rate (float): The sfrxUSD interest rate
        max_borrow_rate (float): Maximum borrow rate to plot (default 20%)
    
    Returns:
        tuple: (DataFrame containing APR data, DataFrame containing borrow rates)
    """
    # Generate borrow rates from 0 to max_borrow_rate in 1% increments
    borrow_rates_array = np.linspace(0, max_borrow_rate, int(max_borrow_rate * 100) + 1)
    
    data = []
    borrow_rates_data = []
    
    for borrow_rate in borrow_rates_array:
        rates = getRates(utilization_rate, borrow_rate, sfrxusd_interest_rate)
        
        # Add frxUSD data
        data.append({
            'borrow_rate': borrow_rate,
            'market': 'frxUSD',
            'apr_type': 'lentAPR',
            'value': rates['frxUSDRates']['lentAPR']
        })
        data.append({
            'borrow_rate': borrow_rate,
            'market': 'frxUSD',
            'apr_type': 'unlentAPR',
            'value': rates['frxUSDRates']['unlentAPR']
        })
        
        # Add sfrxUSD data
        data.append({
            'borrow_rate': borrow_rate,
            'market': 'sfrxUSD',
            'apr_type': 'lentAPR',
            'value': rates['sfrxUSDRates']['lentAPR']
        })
        data.append({
            'borrow_rate': borrow_rate,
            'market': 'sfrxUSD',
            'apr_type': 'unlentAPR',
            'value': rates['sfrxUSDRates']['unlentAPR']
        })
        
        # Add borrow rates
        borrow_rates_data.append({
            'borrow_rate': borrow_rate,
            'market': 'frxUSD',
            'value': rates['frxUSDRates']['borrowAPR']
        })
        borrow_rates_data.append({
            'borrow_rate': borrow_rate,
            'market': 'sfrxUSD',
            'value': rates['sfrxUSDRates']['borrowAPR']
        })
    
    return pd.DataFrame(data), pd.DataFrame(borrow_rates_data)

def generate_lend_rate_comparison_data(utilization_rate=0.85, sfrxusd_interest_rate=0.08, max_lend_rate=0.20):
    """
    Generate APR data for frxUSD and sfrxUSD markets across different lend rates at fixed utilization.
    
    Args:
        utilization_rate (float): Fixed utilization rate (default 85%)
        sfrxusd_interest_rate (float): The sfrxUSD interest rate
        max_lend_rate (float): Maximum lend rate to plot (default 20%)
    
    Returns:
        tuple: (DataFrame containing APR data, DataFrame containing borrow rates)
    """
    # Generate lend rates from 0 to max_lend_rate in 1% increments
    lend_rates_array = np.linspace(0, max_lend_rate, int(max_lend_rate * 100) + 1)
    
    data = []
    borrow_rates_data = []
    
    for lend_rate in lend_rates_array:
        rates = getBorrowRates(utilization_rate, lend_rate, sfrxusd_interest_rate)
        
        # Add frxUSD data
        data.append({
            'lend_rate': lend_rate,
            'market': 'frxUSD',
            'apr_type': 'lentAPR',
            'value': rates['frxUSDRates']['lentAPR']
        })
        data.append({
            'lend_rate': lend_rate,
            'market': 'frxUSD',
            'apr_type': 'unlentAPR',
            'value': rates['frxUSDRates']['unlentAPR']
        })
        
        # Add sfrxUSD data
        data.append({
            'lend_rate': lend_rate,
            'market': 'sfrxUSD',
            'apr_type': 'lentAPR',
            'value': rates['sfrxUSDRates']['lentAPR']
        })
        data.append({
            'lend_rate': lend_rate,
            'market': 'sfrxUSD',
            'apr_type': 'unlentAPR',
            'value': rates['sfrxUSDRates']['unlentAPR']
        })
        
        # Add borrow rates
        borrow_rates_data.append({
            'lend_rate': lend_rate,
            'market': 'frxUSD',
            'value': rates['frxUSDRates']['borrowAPR']
        })
        borrow_rates_data.append({
            'lend_rate': lend_rate,
            'market': 'sfrxUSD',
            'value': rates['sfrxUSDRates']['borrowAPR']
        })
    
    return pd.DataFrame(data), pd.DataFrame(borrow_rates_data) 