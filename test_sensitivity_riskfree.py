"""
Test sensitivity analysis with risk-free asset
"""

import numpy as np
import sys
sys.path.append('/Users/andyzhang/Desktop/26_Spring/Asset_Management/-Pre-first class readings/mvp_web')

from optimizer import MeanVarianceOptimizer
from sensitivity import SensitivityAnalyzer

def test_sensitivity_with_riskfree():
    """Test that sensitivity base metrics match optimal portfolio"""
    
    # Screenshot data
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
    
    # Get optimal portfolio with risk-free
    tangency = optimizer.find_tangency_portfolio()
    optimal = optimizer.find_optimal_portfolio_with_riskfree(tangency, risk_aversion=3.0)
    
    print("=== Optimal Portfolio (from optimizer) ===")
    print(f"Expected Return: {optimal['expected_return']:.4f}")
    print(f"Volatility: {optimal['volatility']:.4f}")
    print(f"Weight Tangency: {optimal['weight_tangency']:.4f}")
    print(f"Weight Risk-Free: {optimal['weight_riskfree']:.4f}")
    
    # Create sensitivity analyzer
    analyzer = SensitivityAnalyzer(optimizer, optimal)
    
    print("\n=== Sensitivity Analyzer Base ===")
    print(f"Base Return: {analyzer.base_return:.4f}")
    print(f"Base Volatility: {analyzer.base_volatility:.4f}")
    
    print("\n=== Match? ===")
    print(f"Return match: {np.isclose(optimal['expected_return'], analyzer.base_return)}")
    print(f"Volatility match: {np.isclose(optimal['volatility'], analyzer.base_volatility)}")
    
    # Test sensitivity
    df_return = analyzer.analyze_return_sensitivity(0.01)
    print("\n=== Return Sensitivity Sample ===")
    print(df_return.head())
    
    # Verify return impact calculation
    # For Domestic Equity with weight = optimal['weights'][0] * optimal['weight_tangency']
    effective_weight = optimal['weights'][0] * optimal['weight_tangency']
    expected_impact = effective_weight * 0.01
    actual_impact = df_return[
        (df_return['asset'] == 'Domestic Equity') & 
        (df_return['direction'] == 'increase')
    ]['return_impact'].values[0]
    
    print(f"\n=== Impact Calculation Check ===")
    print(f"Domestic Equity weight in optimal: {optimal['weights'][0]:.4f}")
    print(f"Weight tangency: {optimal['weight_tangency']:.4f}")
    print(f"Effective weight: {effective_weight:.4f}")
    print(f"Expected impact (1% increase): {expected_impact:.6f}")
    print(f"Actual impact: {actual_impact:.6f}")
    print(f"Match: {np.isclose(expected_impact, actual_impact)}")

if __name__ == "__main__":
    test_sensitivity_with_riskfree()
