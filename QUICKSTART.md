# Quick Start Guide

## Mean-Variance Portfolio Optimizer Web Application

### Project Structure

```
mvp_web/
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── app.py                   # Main Streamlit application
├── optimizer.py             # Core optimization engine
├── sensitivity.py           # Sensitivity analysis module
├── visualizations.py        # Plotting functions
├── utils.py                 # Helper and validation functions
├── test.py                  # Test script
├── requirements.txt         # Python dependencies
├── README.md               # Full documentation
├── DEPLOYMENT.md           # Deployment guide
└── QUICKSTART.md           # This file
```

### Installation & Running

#### Step 1: Install Dependencies

```bash
cd mvp_web
pip install -r requirements.txt
```

#### Step 2: Test Installation (Optional)

```bash
python test.py
```

#### Step 3: Run Application

```bash
streamlit run app.py
```

The app will open at: `http://localhost:8501`

### Module Overview

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `app.py` | Web interface | User inputs, results display |
| `optimizer.py` | Core engine | Portfolio optimization, efficient frontier |
| `sensitivity.py` | Analysis | Parameter error impact quantification |
| `visualizations.py` | Plots | Efficient frontier, sensitivity charts |
| `utils.py` | Utilities | Validation, formatting |

### Key Features

1. **Portfolio Optimization**
   - Tangency Portfolio (max Sharpe ratio)
   - Optimal Portfolio (with/without risk-free)
   - Global Minimum Variance
   - Efficient Frontier

2. **Sensitivity Analysis**
   - Expected return errors: ±1%
   - Volatility errors: ±1%
   - Impact on portfolio metrics
   - 4 detailed charts

3. **User Controls**
   - Number of assets (2-20)
   - Asset parameters (returns, vols)
   - Correlation matrix
   - Constraints (optional)
   - Risk-free rate
   - Risk aversion

### Usage Flow

1. **Configure** (Sidebar)
   - Set number of assets
   - Choose risk-free rate
   - Set risk aversion
   - Toggle options

2. **Input Data** (Tab 1)
   - Asset names
   - Expected returns
   - Volatilities
   - Constraints
   - Correlation matrix

3. **Optimize** (Tab 1)
   - Click "Optimize Portfolio"
   - View results
   - See efficient frontier

4. **Analyze** (Tab 2)
   - Run sensitivity analysis
   - View impact charts
   - Understand parameter criticality

### Code Quality

- **Clean**: No emojis, clear naming
- **Modular**: Separate concerns
- **Documented**: Docstrings throughout
- **Validated**: Input validation
- **Tested**: Test script included

### Deployment

See `DEPLOYMENT.md` for:
- Streamlit Cloud (easiest)
- Heroku
- Docker
- Local network

### Troubleshooting

**Import Error**:
```bash
pip install -r requirements.txt
```

**Port in Use**:
```bash
streamlit run app.py --server.port 8502
```

**Slow Optimization**:
- Reduce number of assets
- Reduce efficient frontier points
- Check constraint feasibility

### Next Steps

1. Test with sample data
2. Customize for your needs
3. Deploy to web
4. Share with users

### Support

- See `README.md` for full documentation
- See `DEPLOYMENT.md` for deployment help
- Run `python test.py` to verify setup

---

**Columbia Business School - Asset Management**
