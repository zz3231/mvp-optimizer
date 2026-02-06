# Deployment Guide

## Quick Start (Local)

```bash
cd mvp_web
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud Deployment

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `mvp_web/app.py`
   - Click "Deploy"

3. **Your app will be live at**: `https://yourapp.streamlit.app`

## Alternative Deployment Options

### Heroku

1. Create `Procfile`:
   ```
   web: cd mvp_web && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Docker

1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY mvp_web/ /app/
   
   RUN pip install -r requirements.txt
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "app.py"]
   ```

2. Build and run:
   ```bash
   docker build -t mvp-optimizer .
   docker run -p 8501:8501 mvp-optimizer
   ```

## Environment Variables

No environment variables required for basic deployment.

## Configuration

All configuration is in `.streamlit/config.toml`

## Troubleshooting

- **Port already in use**: Change port in command or config
- **Module not found**: Verify all requirements are installed
- **Optimization timeout**: Increase number of iterations in optimizer.py
