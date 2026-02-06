"""
Visualization Module
All plotting functions for portfolio optimization and sensitivity analysis
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_efficient_frontier(optimizer, frontier, portfolios_dict, use_riskless=True):
    """
    Plot efficient frontier with individual assets and key portfolios
    
    Parameters:
    -----------
    optimizer : MeanVarianceOptimizer
    frontier : dict with 'returns' and 'volatilities'
    portfolios_dict : dict containing 'tangency', 'optimal', 'gmv', etc.
    use_riskless : bool
    
    Returns:
    --------
    matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Efficient Frontier
    ax.plot(frontier['volatilities'], frontier['returns'], 
            'b-', linewidth=2, label='Efficient Frontier')
    
    # Individual Assets
    ax.scatter(optimizer.volatilities, optimizer.expected_returns, 
              s=100, c='red', marker='o', alpha=0.6, edgecolors='black', linewidth=1.5)
    
    # Label individual assets
    for i, name in enumerate(optimizer.asset_names):
        ax.annotate(name, 
                   xy=(optimizer.volatilities[i], optimizer.expected_returns[i]),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=9, fontweight='bold')
    
    # Tangency Portfolio
    if 'tangency' in portfolios_dict and portfolios_dict['tangency']:
        tangency = portfolios_dict['tangency']
        ax.scatter(tangency['volatility'], tangency['expected_return'],
                  s=200, c='green', marker='*', edgecolors='black', 
                  linewidth=1.5, label='Tangency', zorder=5)
    
    # Optimal Portfolio
    if 'optimal' in portfolios_dict and portfolios_dict['optimal']:
        optimal = portfolios_dict['optimal']
        ax.scatter(optimal['volatility'], optimal['expected_return'],
                  s=200, c='purple', marker='D', edgecolors='black',
                  linewidth=1.5, label='Optimal', zorder=5)
    
    # GMV Portfolio
    if 'gmv' in portfolios_dict and portfolios_dict['gmv']:
        gmv = portfolios_dict['gmv']
        ax.scatter(gmv['volatility'], gmv['expected_return'],
                  s=150, c='orange', marker='s', edgecolors='black',
                  linewidth=1.5, label='GMV', zorder=5)
    
    # Capital Allocation Line
    if use_riskless and 'tangency' in portfolios_dict and portfolios_dict['tangency']:
        tangency = portfolios_dict['tangency']
        sharpe_ratio = tangency['sharpe_ratio']
        max_vol = max(frontier['volatilities']) * 1.3
        cal_vols = np.array([0, max_vol])
        cal_returns = optimizer.risk_free_rate + sharpe_ratio * cal_vols
        
        ax.plot(cal_vols, cal_returns, 'r--', linewidth=2, 
               label=f'CAL (Sharpe={sharpe_ratio:.4f})', alpha=0.7)
        
        # Risk-free rate point
        ax.scatter(0, optimizer.risk_free_rate, s=100, c='black', 
                  marker='s', label='Risk-Free')
    
    ax.set_xlabel('Volatility (Standard Deviation)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Expected Return', fontsize=12, fontweight='bold')
    ax.set_title('Mean-Variance Efficient Frontier', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, p: f'{y:.1%}'))
    
    plt.tight_layout()
    return fig


def plot_sensitivity_analysis(df_return_sens, df_vol_sens):
    """
    Create 4 separate plots for sensitivity analysis
    
    1. Expected return error -> Portfolio return impact
    2. Expected return error -> Portfolio volatility impact
    3. Volatility error -> Portfolio return impact
    4. Volatility error -> Portfolio volatility impact
    
    Returns:
    --------
    matplotlib figure
    """
    assets = df_return_sens['asset'].unique()
    n_assets = len(assets)
    
    # Prepare data
    return_decrease_return_impact = []
    return_increase_return_impact = []
    return_decrease_vol_impact = []
    return_increase_vol_impact = []
    
    vol_decrease_return_impact = []
    vol_increase_return_impact = []
    vol_decrease_vol_impact = []
    vol_increase_vol_impact = []
    
    for asset in assets:
        # Return sensitivity
        return_data = df_return_sens[df_return_sens['asset'] == asset]
        return_decrease_return_impact.append(
            return_data[return_data['direction'] == 'decrease']['return_impact'].values[0]
        )
        return_increase_return_impact.append(
            return_data[return_data['direction'] == 'increase']['return_impact'].values[0]
        )
        return_decrease_vol_impact.append(
            return_data[return_data['direction'] == 'decrease']['volatility_impact'].values[0]
        )
        return_increase_vol_impact.append(
            return_data[return_data['direction'] == 'increase']['volatility_impact'].values[0]
        )
        
        # Volatility sensitivity
        vol_data = df_vol_sens[df_vol_sens['asset'] == asset]
        vol_decrease_return_impact.append(
            vol_data[vol_data['direction'] == 'decrease']['return_impact'].values[0]
        )
        vol_increase_return_impact.append(
            vol_data[vol_data['direction'] == 'increase']['return_impact'].values[0]
        )
        vol_decrease_vol_impact.append(
            vol_data[vol_data['direction'] == 'decrease']['volatility_impact'].values[0]
        )
        vol_increase_vol_impact.append(
            vol_data[vol_data['direction'] == 'increase']['volatility_impact'].values[0]
        )
    
    # Create figure with 4 subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    y_positions = np.arange(n_assets)
    bar_width = 0.35
    
    # Plot 1: Expected Return Error -> Portfolio Return Impact
    ax1 = axes[0, 0]
    ax1.barh(y_positions - bar_width/2, return_decrease_return_impact, bar_width, 
             label='Decrease 1%', color='crimson', alpha=0.7)
    ax1.barh(y_positions + bar_width/2, return_increase_return_impact, bar_width,
             label='Increase 1%', color='forestgreen', alpha=0.7)
    ax1.set_yticks(y_positions)
    ax1.set_yticklabels(assets)
    ax1.set_xlabel('Portfolio Return Impact', fontweight='bold')
    ax1.set_title('Expected Return Error → Portfolio Return Impact', fontweight='bold')
    ax1.axvline(0, color='black', linewidth=0.8, linestyle='-')
    ax1.legend()
    ax1.grid(axis='x', alpha=0.3)
    
    # Plot 2: Expected Return Error -> Portfolio Volatility Impact
    ax2 = axes[0, 1]
    ax2.barh(y_positions - bar_width/2, return_decrease_vol_impact, bar_width,
             label='Decrease 1%', color='crimson', alpha=0.7)
    ax2.barh(y_positions + bar_width/2, return_increase_vol_impact, bar_width,
             label='Increase 1%', color='forestgreen', alpha=0.7)
    ax2.set_yticks(y_positions)
    ax2.set_yticklabels(assets)
    ax2.set_xlabel('Portfolio Volatility Impact', fontweight='bold')
    ax2.set_title('Expected Return Error → Portfolio Volatility Impact', fontweight='bold')
    ax2.axvline(0, color='black', linewidth=0.8, linestyle='-')
    ax2.legend()
    ax2.grid(axis='x', alpha=0.3)
    
    # Plot 3: Volatility Error -> Portfolio Return Impact
    ax3 = axes[1, 0]
    ax3.barh(y_positions - bar_width/2, vol_decrease_return_impact, bar_width,
             label='Decrease 1%', color='crimson', alpha=0.7)
    ax3.barh(y_positions + bar_width/2, vol_increase_return_impact, bar_width,
             label='Increase 1%', color='forestgreen', alpha=0.7)
    ax3.set_yticks(y_positions)
    ax3.set_yticklabels(assets)
    ax3.set_xlabel('Portfolio Return Impact', fontweight='bold')
    ax3.set_title('Volatility Error → Portfolio Return Impact', fontweight='bold')
    ax3.axvline(0, color='black', linewidth=0.8, linestyle='-')
    ax3.legend()
    ax3.grid(axis='x', alpha=0.3)
    
    # Plot 4: Volatility Error -> Portfolio Volatility Impact
    ax4 = axes[1, 1]
    ax4.barh(y_positions - bar_width/2, vol_decrease_vol_impact, bar_width,
             label='Decrease 1%', color='crimson', alpha=0.7)
    ax4.barh(y_positions + bar_width/2, vol_increase_vol_impact, bar_width,
             label='Increase 1%', color='forestgreen', alpha=0.7)
    ax4.set_yticks(y_positions)
    ax4.set_yticklabels(assets)
    ax4.set_xlabel('Portfolio Volatility Impact', fontweight='bold')
    ax4.set_title('Volatility Error → Portfolio Volatility Impact', fontweight='bold')
    ax4.axvline(0, color='black', linewidth=0.8, linestyle='-')
    ax4.legend()
    ax4.grid(axis='x', alpha=0.3)
    
    plt.suptitle('Sensitivity Analysis: Cost of Wrong Parameter Estimates', 
                fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    return fig
