import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_lending_rates(data, title="Lending Rates vs Utilization", save_path=None):
    """
    Create a line plot showing lending rates vs utilization rates for different markets.
    
    Args:
        data (pandas.DataFrame): DataFrame containing market data
        title (str): Title for the plot
        save_path (str, optional): Path to save the plot. If None, displays the plot.
    """
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")
    
    # Create the line plot
    sns.lineplot(
        data=data,
        x='utilization_rate',
        y='lending_rate',
        hue='market',
        linewidth=2.5
    )
    
    # Customize the plot
    plt.title(title, fontsize=16, pad=20)
    plt.xlabel('Utilization Rate', fontsize=12)
    plt.ylabel('Lending Rate', fontsize=12)
    
    # Format axis labels as percentages
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0%}'.format(x)))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    # Add legend with custom styling
    plt.legend(title='Markets', title_fontsize=12, fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()

def plot_rate_comparison(data, utilization_points=[0.2, 0.5, 0.8, 0.95], save_path=None):
    """
    Create a bar plot comparing lending rates across markets at specific utilization points.
    
    Args:
        data (pandas.DataFrame): DataFrame containing market data
        utilization_points (list): List of utilization rates to compare
        save_path (str, optional): Path to save the plot. If None, displays the plot.
    """
    # Filter data for specific utilization points
    comparison_data = []
    for util in utilization_points:
        closest_idx = abs(data['utilization_rate'] - util).groupby(data['market']).idxmin()
        comparison_data.append(data.loc[closest_idx])
    
    comparison_df = pd.concat(comparison_data)
    
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    # Create the bar plot
    sns.barplot(
        data=comparison_df,
        x='market',
        y='lending_rate',
        hue='utilization_rate',
        palette='viridis'
    )
    
    # Customize the plot
    plt.title('Lending Rate Comparison Across Markets', fontsize=16, pad=20)
    plt.xlabel('Market', fontsize=12)
    plt.ylabel('Lending Rate', fontsize=12)
    
    # Format y-axis labels as percentages
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    # Customize legend
    legend = plt.legend(title='Utilization Rate', title_fontsize=12, fontsize=10)
    for t in legend.get_texts():
        t.set_text('{:.0%}'.format(float(t.get_text())))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()

def plot_stacked_apr_comparison(data, borrow_rates, sfrxusd_interest_rate, title="APR Comparison: frxUSD vs sfrxUSD", save_path=None):
    """
    Create a stacked bar chart comparing total APRs (lentAPR + unlentAPR) for both markets,
    with borrow rate curves overlaid.
    
    Args:
        data (pandas.DataFrame): DataFrame containing APR data
        borrow_rates (pandas.DataFrame): DataFrame containing borrow rate data
        sfrxusd_interest_rate (float): The sfrxUSD interest rate
        title (str): Title for the plot
        save_path (str, optional): Path to save the plot. If None, displays the plot.
    """
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Get unique utilization rates
    util_rates = sorted(data[data['market'] == 'frxUSD']['utilization_rate'].unique())
    
    # Set width of bars and positions of the bars
    width = 0.35
    x = np.arange(len(util_rates))
    
    # Prepare data for both markets
    markets = ['frxUSD', 'sfrxUSD']
    positions = [-width/2, width/2]  # Offset for side-by-side bars
    colors = {'frxUSD': ['#2ecc71', '#27ae60'], 'sfrxUSD': ['#3498db', '#2980b9']}
    
    for market, pos in zip(markets, positions):
        market_data = data[data['market'] == market]
        lent_data = market_data[market_data['apr_type'] == 'lentAPR']
        unlent_data = market_data[market_data['apr_type'] == 'unlentAPR']
        
        # Create bars - lentAPR at bottom, unlentAPR on top
        ax.bar(x + pos, lent_data['value'], width, 
               label=f'{market} Lent APR',
               color=colors[market][0])
        ax.bar(x + pos, unlent_data['value'], width, 
               bottom=lent_data['value'],
               label=f'{market} Unlent APR',
               color=colors[market][1],
               hatch='//' if market == 'sfrxUSD' else '')
    
    # Add single borrow rate line (using frxUSD market)
    market_borrow = borrow_rates[borrow_rates['market'] == 'frxUSD']
    ax.plot(x, market_borrow['value'], 
            label='Borrow APR',
            color='#e74c3c',
            linewidth=2.5,
            marker='o',
            markersize=4)
    
    # Add sfrxUSD interest rate line
    ax.axhline(y=sfrxusd_interest_rate, color='#8e44ad', linestyle='--', 
               label='sfrxUSD Interest Rate', linewidth=2)
    
    # Customize the plot
    ax.set_ylabel('APR', fontsize=12)
    ax.set_xlabel('Utilization Rate', fontsize=12)
    ax.set_title(title, fontsize=16, pad=20)
    
    # Set x-axis labels
    ax.set_xticks(x)
    ax.set_xticklabels([f'{rate:.0%}' for rate in util_rates])
    plt.setp(ax.get_xticklabels(), rotation=45)
    
    # Format y-axis as percentage
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    # Add legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add grid for better readability
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()

def plot_fixed_util_apr_comparison(data, borrow_rates, sfrxusd_interest_rate, utilization_rate=0.85, title=None, save_path=None):
    """
    Create a stacked bar chart comparing total APRs (lentAPR + unlentAPR) for both markets
    across different borrow rates at fixed utilization.
    
    Args:
        data (pandas.DataFrame): DataFrame containing APR data
        borrow_rates (pandas.DataFrame): DataFrame containing borrow rate data
        sfrxusd_interest_rate (float): The sfrxUSD interest rate
        utilization_rate (float): The fixed utilization rate used
        title (str): Title for the plot
        save_path (str, optional): Path to save the plot. If None, displays the plot.
    """
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Get unique borrow rates
    borrow_rates_list = sorted(data[data['market'] == 'frxUSD']['borrow_rate'].unique())
    
    # Set width of bars and positions of the bars
    width = 0.35
    x = np.arange(len(borrow_rates_list))
    
    # Prepare data for both markets
    markets = ['frxUSD', 'sfrxUSD']
    positions = [-width/2, width/2]  # Offset for side-by-side bars
    colors = {'frxUSD': ['#2ecc71', '#27ae60'], 'sfrxUSD': ['#3498db', '#2980b9']}
    
    for market, pos in zip(markets, positions):
        market_data = data[data['market'] == market]
        lent_data = market_data[market_data['apr_type'] == 'lentAPR']
        unlent_data = market_data[market_data['apr_type'] == 'unlentAPR']
        
        # Create bars - lentAPR at bottom, unlentAPR on top
        ax.bar(x + pos, lent_data['value'], width, 
               label=f'{market} Lent APR',
               color=colors[market][0])
        ax.bar(x + pos, unlent_data['value'], width, 
               bottom=lent_data['value'],
               label=f'{market} Unlent APR',
               color=colors[market][1],
               hatch='//' if market == 'sfrxUSD' else '')
    
    # Add single borrow rate line (using frxUSD market)
    market_borrow = borrow_rates[borrow_rates['market'] == 'frxUSD']
    ax.plot(x, market_borrow['value'], 
            label='Borrow APR',
            color='#e74c3c',
            linewidth=2.5,
            marker='o',
            markersize=4)
    
    # Add sfrxUSD interest rate line
    ax.axhline(y=sfrxusd_interest_rate, color='#8e44ad', linestyle='--', 
               label='sfrxUSD Interest Rate', linewidth=2)
    
    # Customize the plot
    ax.set_ylabel('APR', fontsize=12)
    ax.set_xlabel('Borrow Rate', fontsize=12)
    if title is None:
        title = f"APR Comparison at {utilization_rate:.0%} Utilization"
    ax.set_title(title, fontsize=16, pad=20)
    
    # Set x-axis labels
    ax.set_xticks(x[::5])  # Show every 5th label to avoid crowding
    ax.set_xticklabels([f'{rate:.0%}' for rate in borrow_rates_list[::5]])
    plt.setp(ax.get_xticklabels(), rotation=45)
    
    # Format y-axis as percentage
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    # Add legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add grid for better readability
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()

def plot_lend_rate_apr_comparison(data, borrow_rates, sfrxusd_interest_rate, utilization_rate=0.85, title=None, save_path=None):
    """
    Create a stacked bar chart comparing total APRs (lentAPR + unlentAPR) for both markets
    across different lend rates at fixed utilization.
    
    Args:
        data (pandas.DataFrame): DataFrame containing APR data
        borrow_rates (pandas.DataFrame): DataFrame containing borrow rate data
        sfrxusd_interest_rate (float): The sfrxUSD interest rate
        utilization_rate (float): The fixed utilization rate used
        title (str): Title for the plot
        save_path (str, optional): Path to save the plot. If None, displays the plot.
    """
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Get unique lend rates
    lend_rates_list = sorted(data[data['market'] == 'frxUSD']['lend_rate'].unique())
    
    # Set width of bars and positions of the bars
    width = 0.35
    x = np.arange(len(lend_rates_list))
    
    # Prepare data for both markets
    markets = ['frxUSD', 'sfrxUSD']
    positions = [-width/2, width/2]  # Offset for side-by-side bars
    colors = {'frxUSD': ['#2ecc71', '#27ae60'], 'sfrxUSD': ['#3498db', '#2980b9']}
    line_colors = {'frxUSD': '#e74c3c', 'sfrxUSD': '#9b59b6'}
    
    for market, pos in zip(markets, positions):
        market_data = data[data['market'] == market]
        lent_data = market_data[market_data['apr_type'] == 'lentAPR']
        unlent_data = market_data[market_data['apr_type'] == 'unlentAPR']
        
        # Create bars - lentAPR at bottom, unlentAPR on top
        ax.bar(x + pos, lent_data['value'], width, 
               label=f'{market} Lent APR',
               color=colors[market][0])
        ax.bar(x + pos, unlent_data['value'], width, 
               bottom=lent_data['value'],
               label=f'{market} Unlent APR',
               color=colors[market][1],
               hatch='//' if market == 'sfrxUSD' else '')
        
        # Add borrow rate line for each market
        market_borrow = borrow_rates[borrow_rates['market'] == market]
        ax.plot(x, market_borrow['value'], 
                label=f'{market} Borrow APR',
                color=line_colors[market],
                linewidth=2.5,
                marker='o',
                markersize=4,
                linestyle='-' if market == 'frxUSD' else '--')
    
    # Add sfrxUSD interest rate line
    ax.axhline(y=sfrxusd_interest_rate, color='#8e44ad', linestyle='--', 
               label='sfrxUSD Interest Rate', linewidth=2)
    
    # Customize the plot
    ax.set_ylabel('APR', fontsize=12)
    ax.set_xlabel('Lend Rate', fontsize=12)
    if title is None:
        title = f"APR Comparison at {utilization_rate:.0%} Utilization"
    ax.set_title(title, fontsize=16, pad=20)
    
    # Set x-axis labels
    ax.set_xticks(x[::5])  # Show every 5th label to avoid crowding
    ax.set_xticklabels([f'{rate:.0%}' for rate in lend_rates_list[::5]])
    plt.setp(ax.get_xticklabels(), rotation=45)
    
    # Format y-axis as percentage
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    # Add legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add grid for better readability
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show() 