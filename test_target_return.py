"""
Test target return and limited borrowing functionality
"""

import numpy as np
import sys
sys.path.append('/Users/andyzhang/Desktop/26_Spring/Asset_Management/-Pre-first class readings/mvp_web')

from optimizer import MeanVarianceOptimizer

def test_target_return_with_riskfree():
    """Test target return mode with risk-free asset"""
    print("=== Test 1: Target Return with Risk-Free ===")
    
    asset_names = ["Domestic Equity", "Foreign Equity", "Emerging Markets"]
    expected_returns = np.array([0.10, 0.0667, 0.0867])
    volatilities = np.array([0.15, 0.20, 0.25])
    correlation = np.array([
        [1.0, 0.5, 0.4],
        [0.5, 1.0, 0.35],
        [0.4, 0.35, 1.0]
    ])
    
    optimizer = MeanVarianceOptimizer(
        asset_names, expected_returns, volatilities, correlation, risk_free_rate=0.05
    )
    
    tangency = optimizer.find_tangency_portfolio()
    print(f"\nTangency: Return={tangency['expected_return']:.4f}, Vol={tangency['volatility']:.4f}")
    
    # Test 1a: Target return achievable without borrowing
    target_return = 0.08
    optimal = optimizer.find_target_return_portfolio_with_riskfree(
        tangency, target_return, limited_borrowing=False
    )
    print(f"\nTarget={target_return:.2%}, No borrowing limit:")
    print(f"  w_tangency={optimal['weight_tangency']:.4f}, w_rf={optimal['weight_riskfree']:.4f}")
    print(f"  Return={optimal['expected_return']:.4f}, Vol={optimal['volatility']:.4f}")
    
    # Test 1b: Target return requires borrowing, but borrowing allowed
    target_return = 0.12
    optimal = optimizer.find_target_return_portfolio_with_riskfree(
        tangency, target_return, limited_borrowing=False
    )
    print(f"\nTarget={target_return:.2%}, No borrowing limit:")
    print(f"  w_tangency={optimal['weight_tangency']:.4f}, w_rf={optimal['weight_riskfree']:.4f}")
    if optimal['weight_riskfree'] < 0:
        print(f"  ✓ Borrowing {abs(optimal['weight_riskfree']):.2%} at risk-free rate")
    print(f"  Return={optimal['expected_return']:.4f}, Vol={optimal['volatility']:.4f}")
    
    # Test 1c: Target return requires borrowing, but borrowing NOT allowed
    optimal = optimizer.find_target_return_portfolio_with_riskfree(
        tangency, target_return, limited_borrowing=True
    )
    print(f"\nTarget={target_return:.2%}, WITH borrowing limit:")
    print(f"  w_tangency={optimal['weight_tangency']:.4f}, w_rf={optimal['weight_riskfree']:.4f}")
    print(f"  Return={optimal['expected_return']:.4f}, Vol={optimal['volatility']:.4f}")
    if optimal.get('warning'):
        print(f"  ⚠️  {optimal['warning']}")

def test_target_return_without_riskfree():
    """Test target return mode without risk-free asset"""
    print("\n\n=== Test 2: Target Return without Risk-Free ===")
    
    asset_names = ["Domestic Equity", "Foreign Equity", "Emerging Markets"]
    expected_returns = np.array([0.10, 0.0667, 0.0867])
    volatilities = np.array([0.15, 0.20, 0.25])
    correlation = np.array([
        [1.0, 0.5, 0.4],
        [0.5, 1.0, 0.35],
        [0.4, 0.35, 1.0]
    ])
    
    optimizer = MeanVarianceOptimizer(
        asset_names, expected_returns, volatilities, correlation, risk_free_rate=0.05
    )
    
    gmv = optimizer.find_global_minimum_variance()
    print(f"\nGMV: Return={gmv['expected_return']:.4f}, Vol={gmv['volatility']:.4f}")
    
    # Test 2a: Target return achievable
    target_return = 0.09
    optimal = optimizer.find_target_return_portfolio_without_riskfree(target_return)
    print(f"\nTarget={target_return:.2%}:")
    if optimal and optimal['success']:
        print(f"  Return={optimal['expected_return']:.4f}, Vol={optimal['volatility']:.4f}")
        print(f"  Weights: {optimal['weights']}")
    else:
        print(f"  ⚠️  {optimal.get('warning', 'Failed')}")
    
    # Test 2b: Target return below GMV
    target_return = 0.07
    optimal = optimizer.find_target_return_portfolio_without_riskfree(target_return)
    print(f"\nTarget={target_return:.2%} (below GMV):")
    if optimal.get('warning'):
        print(f"  ⚠️  {optimal['warning']}")
    print(f"  Returning: Return={optimal['expected_return']:.4f}, Vol={optimal['volatility']:.4f}")

if __name__ == "__main__":
    test_target_return_with_riskfree()
    test_target_return_without_riskfree()
    print("\n=== All Tests Complete ===")
