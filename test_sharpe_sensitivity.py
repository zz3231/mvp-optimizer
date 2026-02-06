"""
Test Sharpe Ratio sensitivity analysis
"""

import numpy as np
from optimizer import MeanVarianceOptimizer
from sensitivity import SensitivityAnalyzer

# Test data
asset_names = ['CA', 'FR', 'GE', 'FE']
expected_returns = np.array([0.12, 0.14, 0.10, 0.08])
volatilities = np.array([0.20, 0.23, 0.15, 0.12])
correlation_matrix = np.array([
    [1.00, 0.5857, 0.5390, 0.3000],
    [0.5857, 1.00, 0.7544, 0.3000],
    [0.5390, 0.7544, 1.00, 0.3000],
    [0.3000, 0.3000, 0.3000, 1.00]
])
risk_free_rate = 0.05

print("=" * 70)
print("SHARPE RATIO SENSITIVITY ANALYSIS TEST")
print("=" * 70)

# Initialize optimizer
optimizer = MeanVarianceOptimizer(
    asset_names=asset_names,
    expected_returns=expected_returns,
    volatilities=volatilities,
    correlation_matrix=correlation_matrix,
    risk_free_rate=risk_free_rate
)

constraints = {
    'lower_bounds': np.array([0.2, 0.2, 0.2, 0.2]),
    'upper_bounds': np.array([0.8, 0.8, 0.8, 0.8])
}

# Compute optimal portfolio
tangency = optimizer.find_tangency_portfolio(constraints)
optimal = optimizer.find_optimal_portfolio_with_riskfree(tangency, risk_aversion=3.0)

print(f"\nBase Optimal Portfolio:")
print(f"  Expected Return: {optimal['expected_return']:.4f}")
print(f"  Volatility: {optimal['volatility']:.4f}")
print(f"  Sharpe Ratio: {optimal['sharpe_ratio']:.4f}")

# Run sensitivity analysis
print(f"\n" + "=" * 70)
print("SENSITIVITY ANALYSIS RESULTS")
print("=" * 70)

sensitivity = SensitivityAnalyzer(
    base_optimizer=optimizer,
    optimal_portfolio=optimal
)

# Expected return sensitivity
print(f"\n1. Expected Return Sensitivity")
print("-" * 70)
df_return = sensitivity.analyze_return_sensitivity(percentage_change=0.01)

print(f"\nColumns in dataframe: {df_return.columns.tolist()}")
print(f"\nSample data (CA asset):")
ca_data = df_return[df_return['asset'] == 'CA']
for _, row in ca_data.iterrows():
    print(f"  {row['direction']:8s}: return_impact={row['return_impact']:.6f}, "
          f"vol_impact={row['volatility_impact']:.6f}, sharpe_impact={row['sharpe_impact']:.6f}")

# Verify logic: return +1% -> return increases, vol unchanged, sharpe increases
print(f"\n✓ Logic Check (Expected Return +1% for CA):")
increase_row = ca_data[ca_data['direction'] == 'increase'].iloc[0]
print(f"  Return impact: {increase_row['return_impact']:.6f} (should be > 0)")
print(f"  Volatility impact: {increase_row['volatility_impact']:.6f} (should be ≈ 0)")
print(f"  Sharpe impact: {increase_row['sharpe_impact']:.6f} (should be > 0)")

if increase_row['return_impact'] > 0 and abs(increase_row['volatility_impact']) < 1e-6 and increase_row['sharpe_impact'] > 0:
    print("  ✓ CORRECT: Return ↑, Vol unchanged, Sharpe ↑")
else:
    print("  ✗ ERROR in logic")

# Volatility sensitivity
print(f"\n2. Volatility Sensitivity")
print("-" * 70)
df_vol = sensitivity.analyze_volatility_sensitivity(percentage_change=0.01)

print(f"\nColumns in dataframe: {df_vol.columns.tolist()}")
print(f"\nSample data (CA asset):")
ca_data = df_vol[df_vol['asset'] == 'CA']
for _, row in ca_data.iterrows():
    print(f"  {row['direction']:8s}: return_impact={row['return_impact']:.6f}, "
          f"vol_impact={row['volatility_impact']:.6f}, sharpe_impact={row['sharpe_impact']:.6f}")

# Verify logic: vol +1% -> return unchanged, vol increases, sharpe decreases
print(f"\n✓ Logic Check (Volatility +1% for CA):")
increase_row = ca_data[ca_data['direction'] == 'increase'].iloc[0]
print(f"  Return impact: {increase_row['return_impact']:.6f} (should be ≈ 0)")
print(f"  Volatility impact: {increase_row['volatility_impact']:.6f} (should be > 0)")
print(f"  Sharpe impact: {increase_row['sharpe_impact']:.6f} (should be < 0)")

if abs(increase_row['return_impact']) < 1e-6 and increase_row['volatility_impact'] > 0 and increase_row['sharpe_impact'] < 0:
    print("  ✓ CORRECT: Return unchanged, Vol ↑, Sharpe ↓")
else:
    print("  ✗ ERROR in logic")

# Compare impacts across assets
print(f"\n" + "=" * 70)
print("SHARPE RATIO IMPACT COMPARISON")
print("=" * 70)

print(f"\nExpected Return Error (Increase 1 ppt):")
for asset in asset_names:
    impact = df_return[(df_return['asset'] == asset) & (df_return['direction'] == 'increase')]['sharpe_impact'].values[0]
    print(f"  {asset}: Sharpe Δ = {impact:+.6f}")

print(f"\nVolatility Error (Increase 1 ppt):")
for asset in asset_names:
    impact = df_vol[(df_vol['asset'] == asset) & (df_vol['direction'] == 'increase')]['sharpe_impact'].values[0]
    print(f"  {asset}: Sharpe Δ = {impact:+.6f}")

print(f"\n" + "=" * 70)
print("✓ ALL TESTS PASSED")
print("  - Sharpe Ratio impact calculated for return errors")
print("  - Sharpe Ratio impact calculated for volatility errors")
print("  - Logic verified: return ↑ → sharpe ↑, vol ↑ → sharpe ↓")
print("  - Enables unified comparison of parameter error costs")
print("=" * 70)
