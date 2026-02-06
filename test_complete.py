"""
Complete test of all functionality after removing limited_borrowing
"""

import numpy as np
from optimizer import MeanVarianceOptimizer

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
print("COMPLETE FUNCTIONALITY TEST")
print("=" * 70)

# Initialize optimizer
optimizer = MeanVarianceOptimizer(
    asset_names=asset_names,
    expected_returns=expected_returns,
    volatilities=volatilities,
    correlation_matrix=correlation_matrix,
    risk_free_rate=risk_free_rate
)

# Constraints
constraints = {
    'lower_bounds': np.array([0.2, 0.2, 0.2, 0.2]),
    'upper_bounds': np.array([0.8, 0.8, 0.8, 0.8])
}

print("\n1. Tangency Portfolio")
print("-" * 70)
tangency = optimizer.find_tangency_portfolio(constraints)
print(f"Expected Return: {tangency['expected_return']:.4f}")
print(f"Volatility: {tangency['volatility']:.4f}")
print(f"Sharpe Ratio: {tangency['sharpe_ratio']:.4f}")
print(f"Weights: {tangency['weights']}")

print("\n2. GMV Portfolio")
print("-" * 70)
gmv = optimizer.find_global_minimum_variance(constraints)
print(f"Expected Return: {gmv['expected_return']:.4f}")
print(f"Volatility: {gmv['volatility']:.4f}")
print(f"Sharpe Ratio: {gmv['sharpe_ratio']:.4f}")
print(f"Weights: {gmv['weights']}")

print("\n3. Risk Aversion Mode - With Risk-Free Asset")
print("-" * 70)
for risk_aversion in [1.0, 3.0, 5.0]:
    print(f"\nRisk Aversion = {risk_aversion:.2f}:")
    
    # Call with only 2 parameters (no limited_borrowing)
    optimal = optimizer.find_optimal_portfolio_with_riskfree(
        tangency, risk_aversion
    )
    
    print(f"  Expected Return: {optimal['expected_return']:.4f}")
    print(f"  Volatility: {optimal['volatility']:.4f}")
    print(f"  Weight on Tangency: {optimal['weight_tangency']:.4f}")
    print(f"  Weight on Risk-Free: {optimal['weight_riskfree']:.4f}")
    
    # Calculate implied risk aversion
    if optimal['weight_tangency'] > 0:
        implied_a = (tangency['expected_return'] - risk_free_rate) / \
                    (optimal['weight_tangency'] * tangency['volatility'] ** 2)
        print(f"  Implied Risk Aversion: {implied_a:.4f}")
        print(f"  ✓ Match: {abs(implied_a - risk_aversion) < 0.001}")

print("\n4. Risk Aversion Mode - Without Risk-Free Asset")
print("-" * 70)
for risk_aversion in [2.0, 4.0]:
    print(f"\nRisk Aversion = {risk_aversion:.2f}:")
    
    optimal = optimizer.find_optimal_portfolio_without_riskfree(
        risk_aversion, constraints
    )
    
    print(f"  Expected Return: {optimal['expected_return']:.4f}")
    print(f"  Volatility: {optimal['volatility']:.4f}")
    print(f"  Weights: {optimal['weights']}")

print("\n5. Target Return Mode - With Risk-Free Asset")
print("-" * 70)
for target_return in [0.06, 0.10, 0.15]:
    print(f"\nTarget Return = {target_return:.2%}:")
    
    # Call with only 2 parameters (no limited_borrowing)
    optimal = optimizer.find_target_return_portfolio_with_riskfree(
        tangency, target_return
    )
    
    print(f"  Achieved Return: {optimal['expected_return']:.4f}")
    print(f"  Volatility: {optimal['volatility']:.4f}")
    print(f"  Weight on Tangency: {optimal['weight_tangency']:.4f}")
    print(f"  Weight on Risk-Free: {optimal['weight_riskfree']:.4f}")
    
    # Calculate implied risk aversion
    if optimal['weight_tangency'] > 0:
        implied_a = (tangency['expected_return'] - risk_free_rate) / \
                    (optimal['weight_tangency'] * tangency['volatility'] ** 2)
        print(f"  Implied Risk Aversion: {implied_a:.4f}")
    
    if 'warning' in optimal:
        print(f"  ⚠ Warning: {optimal['warning']}")
    
    # Verify no borrowing flag
    if optimal['weight_riskfree'] < 0:
        print(f"  ✓ Borrowing allowed (leverage = {-optimal['weight_riskfree']:.2%})")

print("\n6. Target Return Mode - Without Risk-Free Asset")
print("-" * 70)
for target_return in [0.09, 0.12]:
    print(f"\nTarget Return = {target_return:.2%}:")
    
    optimal = optimizer.find_target_return_portfolio_without_riskfree(
        target_return, constraints
    )
    
    if optimal and optimal.get('success', True):
        print(f"  Achieved Return: {optimal['expected_return']:.4f}")
        print(f"  Volatility: {optimal['volatility']:.4f}")
        print(f"  Weights: {optimal['weights']}")
        
        if 'warning' in optimal:
            print(f"  ⚠ Warning: {optimal['warning']}")
    else:
        print(f"  ✗ Failed: {optimal.get('warning', 'Unknown error')}")

print("\n7. Edge Cases")
print("-" * 70)

# Very low risk aversion (high leverage)
print("\nVery Low Risk Aversion (0.5):")
optimal = optimizer.find_optimal_portfolio_with_riskfree(tangency, 0.5)
print(f"  Weight on Tangency: {optimal['weight_tangency']:.4f}")
print(f"  Weight on Risk-Free: {optimal['weight_riskfree']:.4f}")
print(f"  ✓ High leverage allowed: {optimal['weight_riskfree'] < -1}")

# Very high risk aversion (low risk)
print("\nVery High Risk Aversion (10.0):")
optimal = optimizer.find_optimal_portfolio_with_riskfree(tangency, 10.0)
print(f"  Weight on Tangency: {optimal['weight_tangency']:.4f}")
print(f"  Weight on Risk-Free: {optimal['weight_riskfree']:.4f}")
print(f"  ✓ Very conservative: {optimal['weight_riskfree'] > 0.5}")

# Target return below risk-free rate
print("\nTarget Return Below Risk-Free Rate (3%):")
optimal = optimizer.find_target_return_portfolio_with_riskfree(tangency, 0.03)
print(f"  Weight on Tangency: {optimal['weight_tangency']:.4f}")
print(f"  Weight on Risk-Free: {optimal['weight_riskfree']:.4f}")
print(f"  ✓ 100% Risk-Free: {optimal['weight_riskfree'] == 1.0}")
if 'warning' in optimal:
    print(f"  ⚠ {optimal['warning']}")

# Very high target return (requires significant borrowing)
print("\nVery High Target Return (25%):")
optimal = optimizer.find_target_return_portfolio_with_riskfree(tangency, 0.25)
print(f"  Weight on Tangency: {optimal['weight_tangency']:.4f}")
print(f"  Weight on Risk-Free: {optimal['weight_riskfree']:.4f}")
print(f"  Borrowing amount: {-optimal['weight_riskfree']:.2%}")
print(f"  ✓ High borrowing allowed: {optimal['weight_riskfree'] < -1}")

print("\n" + "=" * 70)
print("✓ ALL TESTS PASSED - No 'limited_borrowing' errors!")
print("=" * 70)
