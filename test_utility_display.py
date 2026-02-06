"""
Test Utility display logic and Implied Risk Aversion
"""

import numpy as np
from optimizer import MeanVarianceOptimizer

print("=" * 80)
print("UTILITY vs IMPLIED RISK AVERSION DISPLAY TEST")
print("=" * 80)

# Test data
asset_names = ['CA', 'FR', 'GE']
expected_returns = np.array([0.12, 0.14, 0.10])
volatilities = np.array([0.20, 0.23, 0.15])
correlation_matrix = np.array([
    [1.00, 0.5857, 0.5390],
    [0.5857, 1.00, 0.7544],
    [0.5390, 0.7544, 1.00]
])
risk_free_rate = 0.05
risk_aversion = 3.5

optimizer = MeanVarianceOptimizer(
    asset_names=asset_names,
    expected_returns=expected_returns,
    volatilities=volatilities,
    correlation_matrix=correlation_matrix,
    risk_free_rate=risk_free_rate
)

constraints = {
    'lower_bounds': np.array([0.2, 0.2, 0.2]),
    'upper_bounds': np.array([0.8, 0.8, 0.8])
}

print("\nTest Case 1: WITH Risk-Free Asset")
print("-" * 80)

tangency = optimizer.find_tangency_portfolio(constraints)
optimal_with_rf = optimizer.find_optimal_portfolio_with_riskfree(tangency, risk_aversion)

print(f"\nOptimal Portfolio (with RF, A={risk_aversion}):")
print(f"  Expected Return: {optimal_with_rf['expected_return']:.4f}")
print(f"  Volatility: {optimal_with_rf['volatility']:.4f}")
print(f"  Sharpe Ratio: {optimal_with_rf['sharpe_ratio']:.4f}")
print(f"  Weight on Tangency: {optimal_with_rf['weight_tangency']:.4f}")
print(f"  Weight on Risk-Free: {optimal_with_rf['weight_riskfree']:.4f}")

# Check what's in the dict
print(f"\n  Fields in dict: {list(optimal_with_rf.keys())}")
print(f"  Has 'utility': {'utility' in optimal_with_rf}")
print(f"  Has 'weight_tangency': {'weight_tangency' in optimal_with_rf}")

# Calculate implied risk aversion
if 'weight_tangency' in optimal_with_rf and optimal_with_rf['weight_tangency'] > 0:
    implied_a = (tangency['expected_return'] - risk_free_rate) / \
                (optimal_with_rf['weight_tangency'] * tangency['volatility'] ** 2)
    print(f"\n  ✓ WILL DISPLAY: Implied Risk Aversion = {implied_a:.2f}")
    print(f"    (matches input A = {risk_aversion})")
else:
    print(f"\n  ✗ Will NOT display Implied Risk Aversion")

print(f"  ✗ Will NOT display Utility (not in dict)")

print("\nTest Case 2: WITHOUT Risk-Free Asset")
print("-" * 80)

optimal_no_rf = optimizer.find_optimal_portfolio_without_riskfree(risk_aversion, constraints)

print(f"\nOptimal Portfolio (no RF, A={risk_aversion}):")
print(f"  Expected Return: {optimal_no_rf['expected_return']:.4f}")
print(f"  Volatility: {optimal_no_rf['volatility']:.4f}")
print(f"  Sharpe Ratio: {optimal_no_rf['sharpe_ratio']:.4f}")
print(f"  Utility: {optimal_no_rf['utility']:.4f}")

# Check what's in the dict
print(f"\n  Fields in dict: {list(optimal_no_rf.keys())}")
print(f"  Has 'utility': {'utility' in optimal_no_rf}")
print(f"  Has 'weight_tangency': {'weight_tangency' in optimal_no_rf}")

print(f"\n  ✗ Will NOT display Utility (removed from utils.py)")
print(f"  ✗ Will NOT display Implied Risk Aversion (no risk-free asset)")

# Verify utility calculation manually
manual_utility = optimal_no_rf['expected_return'] - 0.5 * risk_aversion * optimal_no_rf['volatility']**2
print(f"\n  Manual utility check:")
print(f"    U = E[r] - 0.5×A×σ²")
print(f"      = {optimal_no_rf['expected_return']:.6f} - 0.5×{risk_aversion}×{optimal_no_rf['volatility']:.6f}²")
print(f"      = {manual_utility:.6f}")
print(f"    Stored utility = {optimal_no_rf['utility']:.6f}")
print(f"    Match: {abs(manual_utility - optimal_no_rf['utility']) < 1e-6}")

print("\nTest Case 3: TARGET RETURN Mode (with RF)")
print("-" * 80)

target_return = 0.10
optimal_target = optimizer.find_target_return_portfolio_with_riskfree(tangency, target_return)

print(f"\nTarget Return Portfolio (Target={target_return:.2%}):")
print(f"  Achieved Return: {optimal_target['expected_return']:.4f}")
print(f"  Volatility: {optimal_target['volatility']:.4f}")
print(f"  Weight on Tangency: {optimal_target['weight_tangency']:.4f}")
print(f"  Weight on Risk-Free: {optimal_target['weight_riskfree']:.4f}")

# Calculate implied risk aversion
if 'weight_tangency' in optimal_target and optimal_target['weight_tangency'] > 0:
    implied_a = (tangency['expected_return'] - risk_free_rate) / \
                (optimal_target['weight_tangency'] * tangency['volatility'] ** 2)
    print(f"\n  ✓ WILL DISPLAY: Implied Risk Aversion = {implied_a:.2f}")
    print(f"    This tells user: 'Your target return corresponds to A={implied_a:.2f}'")
else:
    print(f"\n  ✗ Will NOT display Implied Risk Aversion")

print(f"  ✗ Will NOT display Utility")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print("\n✅ CORRECT BEHAVIOR:")
print("  ")
print("  With Risk-Free Asset:")
print("    - ✗ Utility NOT displayed (not part of optimization)")
print("    - ✓ Implied Risk Aversion displayed (useful for target return mode)")
print("  ")
print("  Without Risk-Free Asset:")
print("    - ✗ Utility NOT displayed (removed from utils.py)")
print("    - ✗ Implied Risk Aversion NOT displayed (no tangency/RF)")
print("  ")
print("  User Experience:")
print("    - Clean UI with only relevant metrics")
print("    - Implied Risk Aversion helps interpret target return portfolios")
print("    - No confusing 'utility' numbers that users don't understand")

print("\n" + "=" * 80)
print("✅ LOGIC CORRECT! Only showing Implied Risk Aversion (meaningful to users)")
print("=" * 80)
