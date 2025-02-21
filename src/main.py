from data_fetcher import (
    generate_apr_comparison_data,
    generate_fixed_util_apr_data,
    generate_lend_rate_comparison_data
)
from visualization import (
    plot_stacked_apr_comparison,
    plot_fixed_util_apr_comparison,
    plot_lend_rate_apr_comparison
)
import os

def main():
    # Create output directory if it doesn't exist
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Common parameters
    sfrxusd_interest_rate = 0.08  # 8% sfrxUSD interest rate
    utilization_rate = 0.85  # 85% utilization
    
    # Generate first visualization - varying utilization at 10% borrow rate
    borrow_rate = 0.10  # 10% borrow rate
    apr_data, borrow_rates = generate_apr_comparison_data(borrow_rate, sfrxusd_interest_rate)
    
    plot_stacked_apr_comparison(
        apr_data,
        borrow_rates,
        sfrxusd_interest_rate,
        title="APR Comparison: frxUSD vs sfrxUSD (10% Borrow Rate)",
        save_path=os.path.join(output_dir, 'apr_by_utilization.png')
    )
    
    # Generate second visualization - varying borrow rate at 85% utilization
    fixed_util_data, fixed_util_borrow_rates = generate_fixed_util_apr_data(
        utilization_rate=utilization_rate,
        sfrxusd_interest_rate=sfrxusd_interest_rate
    )
    
    plot_fixed_util_apr_comparison(
        fixed_util_data,
        fixed_util_borrow_rates,
        sfrxusd_interest_rate,
        utilization_rate=utilization_rate,
        title=f"APR Comparison at {utilization_rate:.0%} Utilization",
        save_path=os.path.join(output_dir, 'apr_by_borrow_rate.png')
    )
    
    # Generate third visualization - varying lend rate at 85% utilization
    lend_rate_data, lend_rate_borrow_rates = generate_lend_rate_comparison_data(
        utilization_rate=utilization_rate,
        sfrxusd_interest_rate=sfrxusd_interest_rate
    )
    
    plot_lend_rate_apr_comparison(
        lend_rate_data,
        lend_rate_borrow_rates,
        sfrxusd_interest_rate,
        utilization_rate=utilization_rate,
        title=f"APR Comparison by Lend Rate at {utilization_rate:.0%} Utilization",
        save_path=os.path.join(output_dir, 'apr_by_lend_rate.png')
    )
    
    print("APR comparison graphs have been generated in the 'output' directory.")

if __name__ == "__main__":
    main() 