# Mean-Variance Portfolio Optimizer

A web-based portfolio optimization tool implementing Modern Portfolio Theory (Mean-Variance Optimization).

## Features

- **Portfolio Optimization**
  - Tangency Portfolio (Maximum Sharpe Ratio)
  - Optimal Portfolio (with/without risk-free asset)
  - Global Minimum Variance Portfolio
  - Efficient Frontier visualization
  - Support for constraints on asset weights

- **Sensitivity Analysis**
  - Quantify cost of parameter misestimation
  - Analyze impact of expected return errors
  - Analyze impact of volatility errors
  - Visual representation of impacts

- **User-Friendly Interface**
  - Interactive web application
  - Real-time optimization
  - Clear visualization
  - Export capabilities

## Installation

### Requirements

- Python 3.8 or higher
- pip

### Setup

1. Clone or download this repository

2. Navigate to the `mvp_web` directory:
```bash
cd mvp_web
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development

Run the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Deployment

#### Streamlit Cloud (Recommended)

1. Push code to GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

#### Other Options

- **Heroku**: Use Procfile with `web: streamlit run app.py --server.port=$PORT`
- **AWS/GCP/Azure**: Deploy as container or serverless function
- **Local Network**: Use `streamlit run app.py --server.address 0.0.0.0`

## Usage

### 1. Configure Settings

In the sidebar:
- Set number of assets
- Enter risk-free rate
- Choose risk aversion coefficient
- Toggle risk-free asset inclusion
- Enable/disable constraints

### 2. Input Asset Data

In the Portfolio Optimization tab:
- Enter asset names
- Provide expected returns (%)
- Provide volatilities (%)
- Set constraints (if enabled)
- Fill correlation matrix

### 3. Optimize

- Click "Optimize Portfolio"
- View results and efficient frontier

### 4. Sensitivity Analysis

In the Sensitivity Analysis tab:
- Click "Run Sensitivity Analysis"
- View impact of parameter errors
- Analyze which parameters are most critical

## Project Structure

```
mvp_web/
├── app.py                 # Main Streamlit application
├── optimizer.py           # Core optimization engine
├── sensitivity.py         # Sensitivity analysis module
├── visualizations.py      # Plotting functions
├── utils.py              # Helper functions
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Module Documentation

### optimizer.py

Core optimization engine implementing:
- Tangency portfolio calculation
- Global minimum variance calculation
- Optimal portfolio with/without risk-free asset
- Efficient frontier computation

### sensitivity.py

Sensitivity analysis module:
- Quantifies cost of wrong parameter estimates
- Tests impact on portfolio return and volatility
- Supports both expected return and volatility errors

### visualizations.py

Visualization functions:
- Efficient frontier plots
- Sensitivity analysis charts
- Clear labeling and formatting

### utils.py

Utility functions:
- Input validation
- Data formatting
- Correlation matrix validation

## Key Concepts

### With Risk-Free Asset

- Optimal portfolio is combination of tangency portfolio and risk-free asset
- Located on Capital Allocation Line (CAL)
- Sharpe ratio equals tangency portfolio Sharpe ratio
- Formula: w* = (E[r_tangency] - r_f) / (A * σ_tangency²)

### Without Risk-Free Asset

- Optimal portfolio maximizes utility directly
- Utility: U = E[r] - 0.5 * A * σ²
- Not constrained to CAL
- Risk-return tradeoff depends on risk aversion

### Sensitivity Analysis

- Shows cost of using wrong inputs for optimization
- Portfolio optimized with "wrong" parameters
- Evaluated under "true" market conditions
- Negative values indicate worse performance than optimal

## Technical Details

### Optimization Algorithm

- Uses scipy.optimize.minimize with SLSQP method
- Supports equality and inequality constraints
- Handles bounded optimization

### Correlation Matrix Validation

- Checks symmetry
- Verifies diagonal elements = 1
- Ensures positive semi-definite
- Validates range [-1, 1]

## Credits

**Columbia Business School - Asset Management**

Implements concepts from Modern Portfolio Theory:
- Markowitz, H. (1952). Portfolio Selection
- Sharpe, W. (1964). Capital Asset Prices

## License

Educational use only - Columbia Business School

## Support

For questions or issues, please refer to course materials or contact course instructors.
