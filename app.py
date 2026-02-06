"""
Mean-Variance Portfolio Optimizer
Streamlit Web Application

Columbia Business School - Asset Management
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from optimizer import MeanVarianceOptimizer
from sensitivity import SensitivityAnalyzer
from visualizations import plot_efficient_frontier, plot_sensitivity_analysis
from utils import (format_portfolio_results, create_correlation_matrix_template, 
                   validate_inputs, validate_correlation_matrix)


# Page configuration
st.set_page_config(
    page_title="Mean-Variance Portfolio Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("Mean-Variance Portfolio Optimizer")
st.markdown("**Columbia Business School - Asset Management**")
st.markdown("---")

# Initialize session state
if 'n_assets' not in st.session_state:
    st.session_state.n_assets = 3
if 'asset_names' not in st.session_state:
    st.session_state.asset_names = ['Domestic Equity', 'Foreign Equity', 'Domestic Bonds']

# Sidebar for main settings
st.sidebar.header("Portfolio Settings")

# Number of assets
n_assets = st.sidebar.number_input(
    "Number of Assets",
    min_value=2,
    max_value=20,
    value=st.session_state.n_assets,
    step=1
)

# Update asset names if number changed
if n_assets != st.session_state.n_assets:
    st.session_state.n_assets = n_assets
    if n_assets > len(st.session_state.asset_names):
        # Add new assets
        for i in range(len(st.session_state.asset_names), n_assets):
            st.session_state.asset_names.append(f'Asset {i+1}')
    else:
        # Remove assets
        st.session_state.asset_names = st.session_state.asset_names[:n_assets]

# Risk-free rate
risk_free_rate = st.sidebar.number_input(
    "Risk-Free Rate (%)",
    min_value=0.0,
    max_value=20.0,
    value=2.0,
    step=0.1,
    format="%.2f"
) / 100

# Risk aversion
risk_aversion = st.sidebar.number_input(
    "Risk Aversion Coefficient",
    min_value=0.1,
    max_value=10.0,
    value=3.0,
    step=0.1,
    format="%.1f"
)

# Use risk-free asset
use_riskless = st.sidebar.checkbox("Include Risk-Free Asset", value=True)

# Use constraints
use_constraints = st.sidebar.checkbox("Use Constraints", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This tool implements Mean-Variance Optimization based on Modern Portfolio Theory. "
    "It helps find optimal asset allocations and analyze the cost of parameter misestimation."
)

# Main tabs
tab1, tab2, tab3 = st.tabs(["📊 Portfolio Optimization", "📈 Sensitivity Analysis", "ℹ️ Instructions"])

with tab1:
    st.header("Portfolio Input")
    
    # Asset Information
    st.subheader("1. Asset Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Asset Names**")
        asset_names = []
        for i in range(n_assets):
            name = st.text_input(
                f"Asset {i+1}",
                value=st.session_state.asset_names[i],
                key=f"asset_name_{i}",
                label_visibility="collapsed"
            )
            asset_names.append(name)
        st.session_state.asset_names = asset_names
    
    with col2:
        st.markdown("**Expected Return (%)**")
        expected_returns = []
        default_returns = [6.5, 6.5, 4.3] + [5.0] * (n_assets - 3)
        for i in range(n_assets):
            ret = st.number_input(
                f"Return {i+1}",
                min_value=0.0,
                max_value=100.0,
                value=default_returns[i] if i < len(default_returns) else 5.0,
                step=0.1,
                key=f"return_{i}",
                label_visibility="collapsed"
            )
            expected_returns.append(ret / 100)
    
    with col3:
        st.markdown("**Volatility (%)**")
        volatilities = []
        default_vols = [16.0, 17.0, 7.0] + [15.0] * (n_assets - 3)
        for i in range(n_assets):
            vol = st.number_input(
                f"Vol {i+1}",
                min_value=0.1,
                max_value=100.0,
                value=default_vols[i] if i < len(default_vols) else 15.0,
                step=0.1,
                key=f"vol_{i}",
                label_visibility="collapsed"
            )
            volatilities.append(vol / 100)
    
    # Constraints
    if use_constraints:
        st.subheader("2. Constraints")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Lower Bounds (%)**")
            lower_bounds = []
            for i in range(n_assets):
                lb = st.number_input(
                    f"Lower {i+1}",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=1.0,
                    key=f"lower_{i}",
                    label_visibility="collapsed"
                )
                lower_bounds.append(lb / 100)
        
        with col2:
            st.markdown("**Upper Bounds (%)**")
            upper_bounds = []
            for i in range(n_assets):
                ub = st.number_input(
                    f"Upper {i+1}",
                    min_value=0.0,
                    max_value=100.0,
                    value=100.0,
                    step=1.0,
                    key=f"upper_{i}",
                    label_visibility="collapsed"
                )
                upper_bounds.append(ub / 100)
    else:
        lower_bounds = [0.0] * n_assets
        upper_bounds = [1.0] * n_assets
    
    # Correlation Matrix
    st.subheader("3. Correlation Matrix")
    
    # Create default correlation matrix
    default_corr = np.eye(n_assets)
    if n_assets == 3:
        default_corr = np.array([
            [1.0, 0.5, 0.4],
            [0.5, 1.0, 0.25],
            [0.4, 0.25, 1.0]
        ])
    elif n_assets > 3:
        # Fill with moderate correlations
        default_corr = np.eye(n_assets)
        for i in range(n_assets):
            for j in range(i+1, n_assets):
                default_corr[i, j] = default_corr[j, i] = 0.3
    
    # Display correlation matrix input
    corr_matrix = []
    for i in range(n_assets):
        row = []
        cols = st.columns(n_assets)
        for j in range(n_assets):
            with cols[j]:
                if i == j:
                    val = 1.0
                    st.text_input(
                        f"corr_{i}_{j}",
                        value="1.00",
                        disabled=True,
                        key=f"corr_{i}_{j}",
                        label_visibility="collapsed"
                    )
                elif i < j:
                    val = st.number_input(
                        f"corr_{i}_{j}",
                        min_value=-1.0,
                        max_value=1.0,
                        value=float(default_corr[i, j]),
                        step=0.01,
                        key=f"corr_{i}_{j}",
                        label_visibility="collapsed"
                    )
                else:
                    # Mirror upper triangle
                    val = corr_matrix[j][i]
                    st.text_input(
                        f"corr_{i}_{j}",
                        value=f"{val:.2f}",
                        disabled=True,
                        key=f"corr_{i}_{j}_mirror",
                        label_visibility="collapsed"
                    )
                row.append(val)
        corr_matrix.append(row)
    
    # Convert to numpy array
    correlation_matrix = np.array(corr_matrix)
    
    st.markdown("---")
    
    # Optimize button
    if st.button("Optimize Portfolio", type="primary", use_container_width=True):
        # Validate inputs
        is_valid, errors = validate_inputs(
            asset_names, expected_returns, volatilities,
            correlation_matrix, lower_bounds, upper_bounds
        )
        
        if not is_valid:
            st.error("Input validation errors:")
            for error in errors:
                st.error(f"- {error}")
        else:
            with st.spinner("Computing optimal portfolios..."):
                try:
                    # Create optimizer
                    optimizer = MeanVarianceOptimizer(
                        asset_names=asset_names,
                        expected_returns=expected_returns,
                        volatilities=volatilities,
                        correlation_matrix=correlation_matrix,
                        risk_free_rate=risk_free_rate
                    )
                    
                    # Setup constraints
                    if use_constraints:
                        constraints = {
                            'lower_bounds': lower_bounds,
                            'upper_bounds': upper_bounds
                        }
                    else:
                        constraints = None
                    
                    # Store in session state
                    st.session_state.optimizer = optimizer
                    st.session_state.constraints = constraints
                    st.session_state.use_riskless = use_riskless
                    st.session_state.risk_aversion = risk_aversion
                    
                    # Compute portfolios
                    portfolios = {}
                    
                    # Tangency
                    tangency = optimizer.find_tangency_portfolio(constraints)
                    portfolios['tangency'] = tangency
                    
                    # GMV
                    gmv = optimizer.find_global_minimum_variance(constraints)
                    portfolios['gmv'] = gmv
                    
                    # Optimal
                    if use_riskless and tangency:
                        optimal = optimizer.find_optimal_portfolio_with_riskfree(
                            tangency, risk_aversion
                        )
                    else:
                        optimal = optimizer.find_optimal_portfolio_without_riskfree(
                            risk_aversion, constraints
                        )
                    portfolios['optimal'] = optimal
                    
                    st.session_state.portfolios = portfolios
                    st.session_state.optimal = optimal
                    
                    # Compute efficient frontier
                    frontier = optimizer.compute_efficient_frontier(n_points=50, constraints=constraints)
                    st.session_state.frontier = frontier
                    
                    st.success("Optimization completed successfully!")
                    
                except Exception as e:
                    st.error(f"Optimization error: {str(e)}")
    
    # Display results if available
    if 'portfolios' in st.session_state:
        st.markdown("---")
        st.header("Results")
        
        # Display portfolios
        col1, col2, col3 = st.columns(3)
        
        portfolios = st.session_state.portfolios
        
        with col1:
            st.subheader("Tangency Portfolio")
            if portfolios['tangency']:
                result = format_portfolio_results(portfolios['tangency'], "Tangency")
                st.dataframe(result['weights_df'], hide_index=True)
                for key, value in result['metrics'].items():
                    st.metric(key, value)
            else:
                st.warning("Tangency portfolio not found")
        
        with col2:
            st.subheader("Optimal Portfolio")
            if portfolios['optimal']:
                result = format_portfolio_results(portfolios['optimal'], "Optimal")
                st.dataframe(result['weights_df'], hide_index=True)
                for key, value in result['metrics'].items():
                    st.metric(key, value)
                if result['additional_info']:
                    for key, value in result['additional_info'].items():
                        st.metric(key, value)
            else:
                st.warning("Optimal portfolio not found")
        
        with col3:
            st.subheader("GMV Portfolio")
            if portfolios['gmv']:
                result = format_portfolio_results(portfolios['gmv'], "GMV")
                st.dataframe(result['weights_df'], hide_index=True)
                for key, value in result['metrics'].items():
                    st.metric(key, value)
            else:
                st.warning("GMV portfolio not found")
        
        # Plot efficient frontier
        st.markdown("---")
        st.subheader("Efficient Frontier")
        
        fig = plot_efficient_frontier(
            st.session_state.optimizer,
            st.session_state.frontier,
            portfolios,
            use_riskless=st.session_state.use_riskless
        )
        st.pyplot(fig)
        plt.close()

with tab2:
    st.header("Sensitivity Analysis")
    st.markdown(
        "Analyze the cost of using wrong parameter estimates. "
        "This shows how portfolio performance degrades when optimization "
        "is based on incorrect expected returns or volatilities."
    )
    
    if 'optimal' not in st.session_state or st.session_state.optimal is None:
        st.warning("Please optimize portfolio first in the Portfolio Optimization tab")
    else:
        if st.button("Run Sensitivity Analysis", type="primary"):
            with st.spinner("Running sensitivity analysis... This may take a moment..."):
                try:
                    sensitivity = SensitivityAnalyzer(
                        base_optimizer=st.session_state.optimizer,
                        base_optimal_weights=st.session_state.optimal['weights']
                    )
                    
                    # Analyze
                    df_return_sens = sensitivity.analyze_return_sensitivity(
                        percentage_change=0.01,
                        risk_aversion=st.session_state.risk_aversion,
                        constraints=st.session_state.constraints,
                        use_riskless=st.session_state.use_riskless
                    )
                    
                    df_vol_sens = sensitivity.analyze_volatility_sensitivity(
                        percentage_change=0.01,
                        risk_aversion=st.session_state.risk_aversion,
                        constraints=st.session_state.constraints,
                        use_riskless=st.session_state.use_riskless
                    )
                    
                    st.session_state.df_return_sens = df_return_sens
                    st.session_state.df_vol_sens = df_vol_sens
                    st.session_state.sensitivity_base = {
                        'return': sensitivity.base_return,
                        'volatility': sensitivity.base_volatility,
                        'sharpe': sensitivity.base_sharpe
                    }
                    
                    st.success("Sensitivity analysis completed!")
                    
                except Exception as e:
                    st.error(f"Sensitivity analysis error: {str(e)}")
        
        # Display results
        if 'df_return_sens' in st.session_state:
            st.markdown("---")
            
            # Base metrics
            st.subheader("Base Optimal Portfolio Metrics")
            col1, col2, col3 = st.columns(3)
            base = st.session_state.sensitivity_base
            with col1:
                st.metric("Expected Return", f"{base['return']:.2%}")
            with col2:
                st.metric("Volatility", f"{base['volatility']:.2%}")
            with col3:
                st.metric("Sharpe Ratio", f"{base['sharpe']:.4f}")
            
            st.markdown("---")
            
            # Plots
            st.subheader("Impact of Parameter Errors")
            st.markdown(
                "**Interpretation**: Negative values indicate worse performance "
                "compared to the optimal portfolio. The larger the absolute value, "
                "the higher the cost of parameter misestimation."
            )
            
            fig = plot_sensitivity_analysis(
                st.session_state.df_return_sens,
                st.session_state.df_vol_sens
            )
            st.pyplot(fig)
            plt.close()
            
            # Data tables
            st.markdown("---")
            st.subheader("Detailed Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Expected Return Sensitivity**")
                st.dataframe(st.session_state.df_return_sens, hide_index=True)
            
            with col2:
                st.markdown("**Volatility Sensitivity**")
                st.dataframe(st.session_state.df_vol_sens, hide_index=True)

with tab3:
    st.header("Instructions")
    
    st.markdown("""
    ### How to Use This Tool
    
    #### 1. Portfolio Optimization Tab
    
    **Step 1: Configure Settings (Sidebar)**
    - Set the number of assets
    - Enter risk-free rate
    - Choose risk aversion coefficient
    - Toggle risk-free asset inclusion
    - Enable/disable constraints
    
    **Step 2: Input Asset Data**
    - Enter asset names
    - Provide expected returns (annual %)
    - Provide volatilities/standard deviations (annual %)
    - If using constraints, set lower and upper bounds
    - Fill in correlation matrix (symmetric, values between -1 and 1)
    
    **Step 3: Optimize**
    - Click "Optimize Portfolio" button
    - View results:
        - **Tangency Portfolio**: Maximum Sharpe ratio portfolio
        - **Optimal Portfolio**: Best portfolio for your risk aversion
        - **GMV Portfolio**: Global minimum variance portfolio
        - **Efficient Frontier**: Visual representation of risk-return tradeoffs
    
    #### 2. Sensitivity Analysis Tab
    
    **Purpose**: Quantify the cost of using wrong parameter estimates
    
    **Process**:
    - First optimize portfolio in tab 1
    - Run sensitivity analysis in tab 2
    - View impact of ±1% parameter errors
    
    **Interpretation**:
    - Shows how portfolio performance changes when you optimize using incorrect inputs
    - Negative values = worse than optimal
    - Helps understand which parameters are most critical
    
    ### Key Concepts
    
    **With Risk-Free Asset**:
    - Optimal portfolio combines tangency portfolio with risk-free asset
    - Located on Capital Allocation Line (CAL)
    - Sharpe ratio equals tangency portfolio Sharpe ratio
    
    **Without Risk-Free Asset**:
    - Optimal portfolio maximizes utility directly among risky assets
    - Not constrained to CAL
    - Risk-return tradeoff depends on risk aversion
    
    **Constraints**:
    - Lower bound: Minimum allocation to each asset (e.g., 0 = no short selling)
    - Upper bound: Maximum allocation to each asset (e.g., 1 = max 100%)
    
    ### Tips
    
    - Start with default values to understand the tool
    - Ensure correlation matrix is valid (symmetric, diagonal = 1)
    - Higher risk aversion → more conservative portfolio
    - Sensitivity analysis helps identify critical assumptions
    """)
    
    st.markdown("---")
    st.markdown("**Columbia Business School - Asset Management**")
