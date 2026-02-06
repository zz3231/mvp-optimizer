"""
Verify that sensitivity base metrics match optimal portfolio metrics
"""

import numpy as np
import sys
sys.path.append('/Users/andyzhang/Desktop/26_Spring/Asset_Management/-Pre-first class readings/mvp_web')

from optimizer import MeanVarianceOptimizer

def test_metrics_consistency():
    """Verify that portfolio_return and portfolio_volatility give same results"""
    
    # Use screenshot data
    asset_names = ["Domestic Equity", "Foreign Equity", "Emerging Markets"]
    expected_returns = np.array([0.10, 0.0667, 0.0867])
    volatilities = np.array([0.15, 0.20, 0.25])
    correlation = np.array([
        [1.0, 0.5, 0.4],
        [0.5, 1.0, 0.35],
        [0.4, 0.35, 1.0]
    ])
    
    optimizer = MeanVarianceOptimizer(
        asset_names=asset_names,
        expected_returns=expected_returns,
        volatilities=volatilities,
        correlation_matrix=correlation,
        risk_free_rate=0.05
    )
    
    # Get optimal portfolio
    tangency = optimizer.find_tangency_portfolio()
    optimal = optimizer.find_optimal_portfolio_with_riskfree(tangency, risk_aversion=3.0)
    
    print("=== Optimal Portfolio ===")
    print(f"Expected Return: {optimal['expected_return']:.4f}")
    print(f"Volatility: {optimal['volatility']:.4f}")
    print(f"Weights: {optimal['weights']}")
    
    # Now recalculate using the weights
    recalc_return = optimizer.portfolio_return(optimal['weights'])
    recalc_volatility = optimizer.portfolio_volatility(optimal['weights'])
    
    print("\n=== Recalculated from Weights ===")
    print(f"Expected Return: {recalc_return:.4f}")
    print(f"Volatility: {recalc_volatility:.4f}")
    
    print("\n=== Differences ===")
    print(f"Return diff: {abs(optimal['expected_return'] - recalc_return):.10f}")
    print(f"Volatility diff: {abs(optimal['volatility'] - recalc_volatility):.10f}")
    
    print("\n=== Match? ===")
    print(f"Returns match: {np.isclose(optimal['expected_return'], recalc_return)}")
    print(f"Volatility match: {np.isclose(optimal['volatility'], recalc_volatility)}")

if __name__ == "__main__":
    test_metrics_consistency()
