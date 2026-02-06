"""
Test script for recent updates:
1. Removed Limited Borrowing
2. Added Implied Risk Aversion
3. Target Return mode disables Risk Aversion input
"""

import numpy as np
from optimizer import MeanVarianceOptimizer

# Test data (same as before)
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

print("=" * 60)
print("Test 1: Risk Aversion Mode with Risk-Free Asset")
print("=" * 60)

optimizer = MeanVarianceOptimizer(
    asset_names=asset_names,
    expected_returns=expected_returns,
    volatilities=volatilities,
    correlation_matrix=correlation_matrix,
    risk_free_rate=risk_free_rate
)

# Compute tangency
constraints = {
    'lower_bounds': np.array([0.2, 0.2, 0.2, 0.2]),
    'upper_bounds': np.array([0.8, 0.8, 0.8, 0.8])
}
tangency = optimizer.find_tangency_portfolio(constraints)

print(f"\nTangency Portfolio:")
print(f"  Expected Return: {tangency['expected_return']:.4f}")
print(f"  Volatility: {tangency['volatility']:.4f}")
print(f"  Sharpe Ratio: {tangency['sharpe_ratio']:.4f}")

# Test with different risk aversions
for risk_aversion in [3.0, 1.0, 5.0]:
    optimal = optimizer.find_optimal_portfolio_with_riskfree(tangency, risk_aversion)
    
    print(f"\nRisk Aversion = {risk_aversion:.2f}:")
    print(f"  Expected Return: {optimal['expected_return']:.4f}")
    print(f"  Volatility: {optimal['volatility']:.4f}")
    print(f"  Weight on Tangency: {optimal['weight_tangency']:.4f}")
    print(f"  Weight on Risk-Free: {optimal['weight_riskfree']:.4f}")
    
    # Calculate implied risk aversion
    w_tangency = optimal['weight_tangency']
    r_tangency = tangency['expected_return']
    sigma_tangency = tangency['volatility']
    implied_a = (r_tangency - risk_free_rate) / (w_tangency * sigma_tangency ** 2)
    
    print(f"  Implied Risk Aversion: {implied_a:.4f}")
    print(f"  Match Original: {abs(implied_a - risk_aversion) < 0.001}")

print("\n" + "=" * 60)
print("Test 2: Target Return Mode with Risk-Free Asset")
print("=" * 60)

for target_return in [0.08, 0.10, 0.15]:
    optimal = optimizer.find_target_return_portfolio_with_riskfree(tangency, target_return)
    
    print(f"\nTarget Return = {target_return:.2%}:")
    print(f"  Achieved Return: {optimal['expected_return']:.4f}")
    print(f"  Volatility: {optimal['volatility']:.4f}")
    print(f"  Weight on Tangency: {optimal['weight_tangency']:.4f}")
    print(f"  Weight on Risk-Free: {optimal['weight_riskfree']:.4f}")
    
    # Calculate implied risk aversion
    w_tangency = optimal['weight_tangency']
    if w_tangency > 0:
        implied_a = (r_tangency - risk_free_rate) / (w_tangency * sigma_tangency ** 2)
        print(f"  Implied Risk Aversion: {implied_a:.4f}")
    
    if 'warning' in optimal:
        print(f"  Warning: {optimal['warning']}")

print("\n" + "=" * 60)
print("Test 3: Leverage (Borrowing) Scenarios")
print("=" * 60)

# Low risk aversion = high leverage
optimal_low_a = optimizer.find_optimal_portfolio_with_riskfree(tangency, 0.5)
print(f"\nLow Risk Aversion (A=0.5):")
print(f"  Weight on Tangency: {optimal_low_a['weight_tangency']:.4f}")
print(f"  Weight on Risk-Free: {optimal_low_a['weight_riskfree']:.4f}")
print(f"  Can Borrow: {optimal_low_a['weight_riskfree'] < 0}")

# High target return = requires borrowing
optimal_high_target = optimizer.find_target_return_portfolio_with_riskfree(tangency, 0.20)
print(f"\nHigh Target Return (20%):")
print(f"  Weight on Tangency: {optimal_high_target['weight_tangency']:.4f}")
print(f"  Weight on Risk-Free: {optimal_high_target['weight_riskfree']:.4f}")
print(f"  Borrowed Amount: {-optimal_high_target['weight_riskfree']:.4f}" if optimal_high_target['weight_riskfree'] < 0 else "  No Borrowing")

print("\n" + "=" * 60)
print("All Tests Completed!")
print("=" * 60)
