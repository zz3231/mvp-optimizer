"""
Test script to verify all modules work correctly
Run this before deploying
"""

import numpy as np
from optimizer import MeanVarianceOptimizer
from sensitivity import SensitivityAnalyzer
from utils import validate_inputs, validate_correlation_matrix

def test_optimizer():
    """Test basic optimization"""
    print("Testing optimizer...")
    
    # Sample data
    asset_names = ['Domestic Equity', 'Foreign Equity', 'Domestic Bonds']
    expected_returns = [0.065, 0.065, 0.043]
    volatilities = [0.16, 0.17, 0.07]
    correlation_matrix = [
        [1.0, 0.5, 0.4],
        [0.5, 1.0, 0.25],
        [0.4, 0.25, 1.0]
    ]
    risk_free_rate = 0.02
    
    # Create optimizer
    optimizer = MeanVarianceOptimizer(
        asset_names=asset_names,
        expected_returns=expected_returns,
        volatilities=volatilities,
        correlation_matrix=correlation_matrix,
        risk_free_rate=risk_free_rate
    )
    
    # Test tangency
    tangency = optimizer.find_tangency_portfolio()
    assert tangency is not None, "Tangency portfolio failed"
    print(f"  Tangency Sharpe Ratio: {tangency['sharpe_ratio']:.4f}")
    
    # Test GMV
    gmv = optimizer.find_global_minimum_variance()
    assert gmv is not None, "GMV portfolio failed"
    print(f"  GMV Volatility: {gmv['volatility']:.4f}")
    
    # Test optimal with risk-free
    optimal = optimizer.find_optimal_portfolio_with_riskfree(tangency, 3.0)
    assert optimal is not None, "Optimal portfolio failed"
    print(f"  Optimal Return: {optimal['expected_return']:.4f}")
    
    # Test efficient frontier
    frontier = optimizer.compute_efficient_frontier(n_points=20)
    assert len(frontier['returns']) > 0, "Efficient frontier failed"
    print(f"  Frontier points: {len(frontier['returns'])}")
    
    print("Optimizer tests passed!\n")
    return optimizer, optimal


def test_sensitivity(optimizer, optimal):
    """Test sensitivity analysis"""
    print("Testing sensitivity analysis...")
    
    sensitivity = SensitivityAnalyzer(
        base_optimizer=optimizer,
        base_optimal_weights=optimal['weights']
    )
    
    # Test return sensitivity
    df_return = sensitivity.analyze_return_sensitivity(
        percentage_change=0.01,
        risk_aversion=3.0,
        constraints=None,
        use_riskless=True
    )
    assert len(df_return) > 0, "Return sensitivity failed"
    print(f"  Return sensitivity rows: {len(df_return)}")
    
    # Test volatility sensitivity
    df_vol = sensitivity.analyze_volatility_sensitivity(
        percentage_change=0.01,
        risk_aversion=3.0,
        constraints=None,
        use_riskless=True
    )
    assert len(df_vol) > 0, "Volatility sensitivity failed"
    print(f"  Volatility sensitivity rows: {len(df_vol)}")
    
    print("Sensitivity tests passed!\n")


def test_validation():
    """Test input validation"""
    print("Testing validation...")
    
    # Valid correlation matrix
    corr_valid = np.eye(3)
    is_valid, msg = validate_correlation_matrix(corr_valid)
    assert is_valid, "Valid correlation rejected"
    
    # Invalid correlation matrix (not symmetric)
    corr_invalid = np.array([[1, 0.5, 0.3], [0.4, 1, 0.2], [0.3, 0.2, 1]])
    is_valid, msg = validate_correlation_matrix(corr_invalid)
    assert not is_valid, "Invalid correlation accepted"
    
    print("Validation tests passed!\n")


def main():
    print("="*50)
    print("Running tests...")
    print("="*50 + "\n")
    
    try:
        optimizer, optimal = test_optimizer()
        test_sensitivity(optimizer, optimal)
        test_validation()
        
        print("="*50)
        print("All tests passed!")
        print("="*50)
        print("\nYou can now run the app:")
        print("  streamlit run app.py")
        
    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
