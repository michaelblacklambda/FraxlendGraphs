# Fraxlend Market Analysis

This Python project visualizes lending rates across different markets based on utilization rates. It provides tools to analyze and compare lending rates using interactive graphs and data visualization.

## Interactive Notebook

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/main?labpath=FraxlendAnalysis.ipynb)

Click the Binder badge above to launch an interactive version of the notebook!

## Local Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

- `src/` - Contains the main source code
  - `data_fetcher.py` - Functions for fetching market data
  - `visualization.py` - Functions for creating graphs and visualizations
  - `main.py` - Main script to run the analysis
- `FraxlendAnalysis.ipynb` - Interactive Jupyter notebook with visualizations
- `create_notebook.py` - Script to generate the Jupyter notebook

## Deployment Options

### 1. Binder (Recommended)
- Click the Binder badge above
- No installation required
- Runs directly in your browser

### 2. Google Colab
1. Upload `FraxlendAnalysis.ipynb` to Google Drive
2. Open with Google Colab
3. Upload the `src` folder to the Colab runtime
4. Run all cells

### 3. Local Jupyter Server
1. Follow the Local Setup instructions above
2. Run `jupyter notebook`
3. Open `FraxlendAnalysis.ipynb`

## Usage

Run the main script:
```bash
python src/main.py
```

This will generate graphs showing the relationship between utilization rates and lending rates across different markets. 