"""
Test fixes for:
1. Correlation matrix syncing
2. Efficient frontier range
3. Sensitivity analysis logic
4. Portfolio display logic
"""

import numpy as np
import sys
sys.path.append('/Users/andyzhang/Desktop/26_Spring/Asset_Management/-Pre-first class readings/mvp_web')

from optimizer import MeanVarianceOptimizer
from sensitivity import SensitivityAnalyzer

def test_sensitivity_logic():
    """Test new sensitivity analysis logic"""
    print("\n=== Testing Sensitivity Analysis Logic ===")
    
    # Simple 3-asset portfolio
    asset_names = ["Asset A", "Asset B", "Asset C"]
    expected_returns = np.array([0.10, 0.08, 0.06])
    volatilities = np.array([0.15, 0.12, 0.10])
    correlation = np.array([
        [1.0, 0.5, 0.3],
        [0.5, 1.0, 0.4],
        [0.3, 0.4, 1.0]
    ])
    
    optimizer = MeanVarianceOptimizer(
        asset_names=asset_names,
        expected_returns=expected_returns,
        volatilities=volatilities,
        correlation_matrix=correlation,
        risk_free_rate=0.05
    )
    
    # Get optimal weights
    tangency = optimizer.find_tangency_portfolio()
    optimal = optimizer.find_optimal_portfolio_with_riskfree(tangency, risk_aversion=3.0)
    
    print(f"\nOptimal weights: {optimal['weights']}")
    print(f"Expected return: {optimal['expected_return']:.4f}")
    print(f"Volatility: {optimal['volatility']:.4f}")
    
    # Run sensitivity analysis
    analyzer = SensitivityAnalyzer(optimizer, optimal['weights'])
    
    # Test return sensitivity
    df_return = analyzer.analyze_return_sensitivity(percentage_change=0.01)
    print("\n--- Return Sensitivity ---")
    print(df_return)
    
    # Verify logic: weights stay fixed, only returns change
    # For Asset A increase 1%, portfolio return should increase by weight[0] * 0.01
    asset_a_increase = df_return[(df_return['asset'] == 'Asset A') & 
                                  (df_return['direction'] == 'increase')]
    expected_impact = optimal['weights'][0] * 0.01
    actual_impact = asset_a_increase['return_impact'].values[0]
    
    print(f"\nAsset A weight: {optimal['weights'][0]:.4f}")
    print(f"Expected return impact: {expected_impact:.6f}")
    print(f"Actual return impact: {actual_impact:.6f}")
    print(f"Match: {np.isclose(expected_impact, actual_impact, atol=1e-6)}")
    
    # Test volatility sensitivity
    df_vol = analyzer.analyze_volatility_sensitivity(percentage_change=0.01)
    print("\n--- Volatility Sensitivity ---")
    print(df_vol)
    
    return df_return, df_vol

def test_efficient_frontier_range():
    """Test that efficient frontier extends beyond min/max returns"""
    print("\n=== Testing Efficient Frontier Range ===")
    
    asset_names = ["Asset A", "Asset B"]
    expected_returns = np.array([0.10, 0.06])
    volatilities = np.array([0.15, 0.10])
    correlation = np.array([[1.0, 0.3], [0.3, 1.0]])
    
    optimizer = MeanVarianceOptimizer(
        asset_names=asset_names,
        expected_returns=expected_returns,
        volatilities=volatilities,
        correlation_matrix=correlation,
        risk_free_rate=0.05
    )
    
    tangency = optimizer.find_tangency_portfolio()
    frontier = optimizer.compute_efficient_frontier(n_points=50)
    
    print(f"\nAsset return range: [{expected_returns.min():.4f}, {expected_returns.max():.4f}]")
    print(f"Frontier return range: [{frontier['returns'].min():.4f}, {frontier['returns'].max():.4f}]")
    print(f"Tangency return: {tangency['expected_return']:.4f}")
    print(f"Frontier includes tangency: {frontier['returns'].min() <= tangency['expected_return'] <= frontier['returns'].max()}")
    
    return frontier, tangency

if __name__ == "__main__":
    print("Testing all fixes...")
    
    # Test 1: Sensitivity analysis logic
    df_return, df_vol = test_sensitivity_logic()
    
    # Test 2: Efficient frontier range
    frontier, tangency = test_efficient_frontier_range()
    
    print("\n=== All Tests Complete ===")
