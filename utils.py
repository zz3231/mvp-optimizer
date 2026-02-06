"""
Utility Functions
Helper functions for data formatting and display
"""

import pandas as pd
import numpy as np


def format_portfolio_results(portfolio_dict, portfolio_name):
    """
    Format portfolio results as a DataFrame
    
    Parameters:
    -----------
    portfolio_dict : dict
        Portfolio optimization results
    portfolio_name : str
        Name of the portfolio
        
    Returns:
    --------
    dict with formatted data
    """
    if portfolio_dict is None:
        return None
    
    # Weights DataFrame
    weights_df = pd.DataFrame({
        'Asset': list(portfolio_dict['weights_dict'].keys()),
        'Weight': list(portfolio_dict['weights_dict'].values())
    })
    weights_df['Weight'] = weights_df['Weight'].apply(lambda x: f"{x:.2%}")
    
    # Metrics
    metrics = {
        'Expected Return': f"{portfolio_dict['expected_return']:.2%}",
        'Volatility': f"{portfolio_dict['volatility']:.2%}",
        'Sharpe Ratio': f"{portfolio_dict['sharpe_ratio']:.4f}"
    }
    
    # Additional info for portfolios with risk-free asset
    additional_info = {}
    if 'weight_riskfree' in portfolio_dict:
        additional_info['Weight on Risk-Free'] = f"{portfolio_dict['weight_riskfree']:.2%}"
        additional_info['Weight on Tangency'] = f"{portfolio_dict['weight_tangency']:.2%}"
    
    # Note: Utility is not displayed to users (internal optimization metric only)
    
    return {
        'name': portfolio_name,
        'weights_df': weights_df,
        'metrics': metrics,
        'additional_info': additional_info
    }


def create_correlation_matrix_template(n_assets):
    """
    Create a template correlation matrix
    
    Parameters:
    -----------
    n_assets : int
        Number of assets
        
    Returns:
    --------
    numpy array with identity matrix
    """
    return np.eye(n_assets)


def validate_correlation_matrix(corr_matrix):
    """
    Validate correlation matrix
    
    Parameters:
    -----------
    corr_matrix : array-like
        Correlation matrix to validate
        
    Returns:
    --------
    tuple (is_valid, error_message)
    """
    corr_matrix = np.array(corr_matrix)
    
    # Check if square
    if corr_matrix.shape[0] != corr_matrix.shape[1]:
        return False, "Correlation matrix must be square"
    
    # Check diagonal elements
    if not np.allclose(np.diag(corr_matrix), 1.0):
        return False, "Diagonal elements must be 1.0"
    
    # Check symmetry
    if not np.allclose(corr_matrix, corr_matrix.T):
        return False, "Correlation matrix must be symmetric"
    
    # Check range
    if np.any(corr_matrix < -1) or np.any(corr_matrix > 1):
        return False, "Correlation values must be between -1 and 1"
    
    # Check positive semi-definite
    eigenvalues = np.linalg.eigvals(corr_matrix)
    if np.any(eigenvalues < -1e-8):
        return False, "Correlation matrix must be positive semi-definite"
    
    return True, ""


def validate_inputs(asset_names, expected_returns, volatilities, 
                   correlation_matrix, lower_bounds, upper_bounds):
    """
    Validate all user inputs
    
    Returns:
    --------
    tuple (is_valid, error_messages)
    """
    errors = []
    
    # Check lengths match
    n = len(asset_names)
    if len(expected_returns) != n:
        errors.append(f"Expected returns length ({len(expected_returns)}) != number of assets ({n})")
    if len(volatilities) != n:
        errors.append(f"Volatilities length ({len(volatilities)}) != number of assets ({n})")
    if len(lower_bounds) != n:
        errors.append(f"Lower bounds length ({len(lower_bounds)}) != number of assets ({n})")
    if len(upper_bounds) != n:
        errors.append(f"Upper bounds length ({len(upper_bounds)}) != number of assets ({n})")
    
    # Check correlation matrix
    is_valid_corr, corr_error = validate_correlation_matrix(correlation_matrix)
    if not is_valid_corr:
        errors.append(f"Correlation matrix error: {corr_error}")
    
    # Check volatilities are positive
    if np.any(np.array(volatilities) <= 0):
        errors.append("All volatilities must be positive")
    
    # Check bounds
    if np.any(np.array(lower_bounds) < 0) or np.any(np.array(upper_bounds) > 1):
        errors.append("Bounds must be between 0 and 1")
    
    if np.any(np.array(lower_bounds) > np.array(upper_bounds)):
        errors.append("Lower bounds must be <= upper bounds")
    
    if len(errors) == 0:
        return True, []
    else:
        return False, errors
