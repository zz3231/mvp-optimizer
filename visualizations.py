"""
Visualization Module for Mean-Variance Portfolio Optimization
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def plot_efficient_frontier(optimizer, frontier, portfolios, use_riskless=True):
    """
    Plot efficient frontier with colorful individual assets and special portfolios
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot efficient frontier
    ax.plot(frontier['volatilities'], frontier['returns'], 
            'b-', linewidth=2.5, label='Efficient Frontier', zorder=3)
    
    # Generate distinct colors for each asset
    n_assets = len(optimizer.asset_names)
    colors = cm.get_cmap('tab10')(np.linspace(0, 1, n_assets))
    
    # Plot individual assets with different colors (no legend)
    for i, name in enumerate(optimizer.asset_names):
        asset_return = optimizer.expected_returns[i]
        asset_vol = optimizer.volatilities[i]
        ax.scatter(asset_vol, asset_return, s=150, c=[colors[i]], 
                  alpha=0.8, edgecolors='black', linewidth=1.5, 
                  zorder=5)  # No label for legend
        # Simple text annotation without background box
        ax.annotate(name, (asset_vol, asset_return), 
                   xytext=(8, 8), textcoords='offset points',
                   fontsize=10, fontweight='bold')
    
    # Plot special portfolios with larger sizes
    if portfolios['tangency']:
        tang = portfolios['tangency']
        ax.scatter(tang['volatility'], tang['expected_return'], 
                  s=220, c='purple', marker='D', label='Tangency',
                  edgecolors='black', linewidth=2, zorder=7, alpha=0.9)
    
    if portfolios['optimal']:
        opt = portfolios['optimal']
        ax.scatter(opt['volatility'], opt['expected_return'],
                  s=300, c='red', marker='*', label='Optimal',
                  edgecolors='black', linewidth=2, zorder=7, alpha=0.9)
    
    if portfolios['gmv']:
        gmv = portfolios['gmv']
        ax.scatter(gmv['volatility'], gmv['expected_return'],
                  s=220, c='orange', marker='s', label='GMV',
                  edgecolors='black', linewidth=2, zorder=7, alpha=0.9)
    
    # Plot CAL if risk-free asset is used
    if use_riskless and portfolios['tangency']:
        rf_rate = optimizer.risk_free_rate
        tang_return = portfolios['tangency']['expected_return']
        tang_vol = portfolios['tangency']['volatility']
        sharpe = (tang_return - rf_rate) / tang_vol
        
        # Extend CAL line
        max_vol = max(frontier['volatilities']) * 1.2
        cal_vols = np.linspace(0, max_vol, 100)
        cal_returns = rf_rate + sharpe * cal_vols
        
        ax.plot(cal_vols, cal_returns, 'r--', linewidth=2,
               label=f'CAL (Sharpe={sharpe:.4f})', alpha=0.7, zorder=2)
        
        # Plot risk-free rate
        ax.scatter(0, rf_rate, s=180, c='black', marker='s',
                  label='Risk-Free', zorder=6, edgecolors='white', linewidth=2)
    
    ax.set_xlabel('Volatility (Standard Deviation)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Expected Return', fontsize=13, fontweight='bold')
    ax.set_title('Mean-Variance Efficient Frontier', fontsize=15, fontweight='bold', pad=20)
    
    # Set smart axis limits
    # Collect all relevant points
    all_vols = list(optimizer.volatilities) + list(frontier['volatilities'])
    all_returns = list(optimizer.expected_returns) + list(frontier['returns'])
    
    if portfolios['tangency']:
        all_vols.append(portfolios['tangency']['volatility'])
        all_returns.append(portfolios['tangency']['expected_return'])
    if portfolios['optimal']:
        all_vols.append(portfolios['optimal']['volatility'])
        all_returns.append(portfolios['optimal']['expected_return'])
    if portfolios['gmv']:
        all_vols.append(portfolios['gmv']['volatility'])
        all_returns.append(portfolios['gmv']['expected_return'])
    
    # Always include risk-free asset if used
    if use_riskless:
        all_vols.append(0.0)
        all_returns.append(optimizer.risk_free_rate)
    
    # Calculate ranges
    vol_max = max(all_vols)
    ret_min, ret_max = min(all_returns), max(all_returns)
    ret_range = ret_max - ret_min
    
    # X-axis: Always start from 0 (to show risk-free), extend 15% beyond max
    ax.set_xlim(0, vol_max * 1.15)
    
    # Y-axis: Add 10% margin on both sides
    ax.set_ylim(ret_min - ret_range * 0.1, ret_max + ret_range * 0.1)
    
    # Improved legend
    ax.legend(loc='best', fontsize=10, framealpha=0.95, 
             edgecolor='gray', fancybox=True, shadow=True)
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, p: f'{y:.1%}'))
    
    plt.tight_layout()
    return fig


def plot_sensitivity_analysis(df_return_sens, df_vol_sens):
    """
    Create 2 plots for sensitivity analysis
    
    1. Expected return error -> Portfolio return impact
    2. Volatility error -> Portfolio volatility impact
    
    Note: Expected return error doesn't affect volatility, and 
    volatility error doesn't affect expected return (with fixed weights).
    
    Returns:
    --------
    matplotlib figure
    """
    assets = df_return_sens['asset'].unique()
    n_assets = len(assets)
    
    # Prepare data for return sensitivity
    return_decrease_impact = []
    return_increase_impact = []
    
    for asset in assets:
        return_data = df_return_sens[df_return_sens['asset'] == asset]
        return_decrease_impact.append(
            return_data[return_data['direction'] == 'decrease']['return_impact'].values[0]
        )
        return_increase_impact.append(
            return_data[return_data['direction'] == 'increase']['return_impact'].values[0]
        )
    
    # Prepare data for volatility sensitivity
    vol_decrease_impact = []
    vol_increase_impact = []
    
    for asset in assets:
        vol_data = df_vol_sens[df_vol_sens['asset'] == asset]
        vol_decrease_impact.append(
            vol_data[vol_data['direction'] == 'decrease']['volatility_impact'].values[0]
        )
        vol_increase_impact.append(
            vol_data[vol_data['direction'] == 'increase']['volatility_impact'].values[0]
        )
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    y_positions = np.arange(n_assets)
    bar_width = 0.35
    
    # Plot 1: Expected Return Error → Portfolio Return Impact
    ax1.barh(y_positions - bar_width/2, return_decrease_impact, bar_width, 
             label='Decrease 1 ppt', color='crimson', alpha=0.7)
    ax1.barh(y_positions + bar_width/2, return_increase_impact, bar_width,
             label='Increase 1 ppt', color='forestgreen', alpha=0.7)
    ax1.set_yticks(y_positions)
    ax1.set_yticklabels(assets)
    ax1.set_xlabel('Portfolio Return Impact (percentage points)', fontsize=12, fontweight='bold')
    ax1.set_title('Expected Return Error → Portfolio Return Impact', 
                  fontsize=13, fontweight='bold')
    ax1.axvline(0, color='black', linewidth=0.8, linestyle='-')
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(axis='x', alpha=0.3)
    # Format as percentage points
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x*100:.2f}%'))
    
    # Plot 2: Volatility Error → Portfolio Volatility Impact
    ax2.barh(y_positions - bar_width/2, vol_decrease_impact, bar_width,
             label='Decrease 1 ppt', color='crimson', alpha=0.7)
    ax2.barh(y_positions + bar_width/2, vol_increase_impact, bar_width,
             label='Increase 1 ppt', color='forestgreen', alpha=0.7)
    ax2.set_yticks(y_positions)
    ax2.set_yticklabels(assets)
    ax2.set_xlabel('Portfolio Volatility Impact (percentage points)', fontsize=12, fontweight='bold')
    ax2.set_title('Volatility Error → Portfolio Volatility Impact', 
                  fontsize=13, fontweight='bold')
    ax2.axvline(0, color='black', linewidth=0.8, linestyle='-')
    ax2.legend(loc='best', fontsize=10)
    ax2.grid(axis='x', alpha=0.3)
    # Format as percentage points
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x*100:.2f}%'))
    
    plt.suptitle('Sensitivity Analysis: Cost of Wrong Parameter Estimates', 
                 fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    return fig
