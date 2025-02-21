import nbformat as nbf
import os

def create_notebook():
    # Create a new notebook
    nb = nbf.v4.new_notebook()
    
    # Add markdown cell with title and description
    nb.cells.append(nbf.v4.new_markdown_cell("""# Fraxlend Market Analysis
    
This notebook visualizes lending rates and APRs across different markets (frxUSD and sfrxUSD).
It shows how different parameters affect the lending and borrowing rates in these markets."""))

    # Add imports cell
    imports = '''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# Create interactive sliders
utilization_slider = widgets.FloatSlider(
    value=0.85,
    min=0.0,
    max=1.0,
    step=0.01,
    description='Utilization Rate:',
    continuous_update=False
)

borrow_rate_slider = widgets.FloatSlider(
    value=0.10,
    min=0.0,
    max=0.20,
    step=0.01,
    description='Borrow APR:',
    continuous_update=False
)

sfrxusd_rate_slider = widgets.FloatSlider(
    value=0.08,
    min=0.0,
    max=0.20,
    step=0.01,
    description='sfrxUSD Rate:',
    continuous_update=False
)

# Display sliders
display(widgets.VBox([utilization_slider, borrow_rate_slider, sfrxusd_rate_slider]))'''
    nb.cells.append(nbf.v4.new_code_cell(imports))

    # Add data fetcher functions
    with open('src/data_fetcher.py', 'r') as f:
        content = f.read()
        # Remove imports as we already have them
        content = content.replace('import numpy as np\nimport pandas as pd\n\n', '')
        nb.cells.append(nbf.v4.new_markdown_cell('## Data Generation Functions'))
        nb.cells.append(nbf.v4.new_code_cell(content))

    # Add visualization functions
    with open('src/visualization.py', 'r') as f:
        content = f.read()
        # Remove imports as we already have them
        content = content.replace('import matplotlib.pyplot as plt\nimport seaborn as sns\nimport pandas as pd\nimport numpy as np\n\n', '')
        nb.cells.append(nbf.v4.new_markdown_cell('## Visualization Functions'))
        nb.cells.append(nbf.v4.new_code_cell(content))

    # Add first analysis with interactive update
    analysis = '''# Create output widgets for each plot
out1 = widgets.Output()
out2 = widgets.Output()
out3 = widgets.Output()

def update_first_plot(change=None):
    with out1:
        clear_output(wait=True)
        plt.figure(figsize=(12, 8))
        
        # Generate visualization with current slider values
        apr_data, borrow_rates = generate_apr_comparison_data(
            borrow_rate_slider.value,
            sfrxusd_rate_slider.value
        )
        
        plot_stacked_apr_comparison(
            apr_data,
            borrow_rates,
            sfrxusd_rate_slider.value,
            title=f"APR Comparison: frxUSD vs sfrxUSD ({borrow_rate_slider.value:.0%} Borrow Rate)"
        )

# Connect sliders to update function
borrow_rate_slider.observe(update_first_plot, names='value')
sfrxusd_rate_slider.observe(update_first_plot, names='value')

# Display first output widget
display(widgets.HTML("<h2>APR Comparison: frxUSD vs sfrxUSD</h2>"))
display(out1)

# Initial plot
update_first_plot()'''
    nb.cells.append(nbf.v4.new_code_cell(analysis))

    # Add second visualization with interactive update
    analysis2 = '''def update_second_plot(change=None):
    with out2:
        clear_output(wait=True)
        plt.figure(figsize=(12, 8))
        
        # Generate visualization with current slider values
        fixed_util_data, fixed_util_borrow_rates = generate_fixed_util_apr_data(
            utilization_rate=utilization_slider.value,
            sfrxusd_interest_rate=sfrxusd_rate_slider.value
        )
        
        plot_fixed_util_apr_comparison(
            fixed_util_data,
            fixed_util_borrow_rates,
            sfrxusd_rate_slider.value,
            utilization_rate=utilization_slider.value,
            title=f"APR Comparison at {utilization_slider.value:.0%} Utilization"
        )

# Connect sliders to update function
utilization_slider.observe(update_second_plot, names='value')
sfrxusd_rate_slider.observe(update_second_plot, names='value')

# Display second output widget
display(widgets.HTML("<h2>APR Comparison by Utilization</h2>"))
display(out2)

# Initial plot
update_second_plot()'''
    nb.cells.append(nbf.v4.new_code_cell(analysis2))

    # Add third visualization with interactive update
    analysis3 = '''def update_third_plot(change=None):
    with out3:
        clear_output(wait=True)
        plt.figure(figsize=(12, 8))
        
        # Generate visualization with current slider values
        lend_rate_data, lend_rate_borrow_rates = generate_lend_rate_comparison_data(
            utilization_rate=utilization_slider.value,
            sfrxusd_interest_rate=sfrxusd_rate_slider.value
        )
        
        plot_lend_rate_apr_comparison(
            lend_rate_data,
            lend_rate_borrow_rates,
            sfrxusd_rate_slider.value,
            utilization_rate=utilization_slider.value,
            title=f"APR Comparison by Lend Rate at {utilization_slider.value:.0%} Utilization"
        )

# Connect sliders to update function
utilization_slider.observe(update_third_plot, names='value')
sfrxusd_rate_slider.observe(update_third_plot, names='value')

# Display third output widget
display(widgets.HTML("<h2>APR Comparison by Lend Rate</h2>"))
display(out3)

# Initial plot
update_third_plot()'''
    nb.cells.append(nbf.v4.new_code_cell(analysis3))

    # Write the notebook to a file
    with open('FraxlendAnalysis.ipynb', 'w') as f:
        nbf.write(nb, f)

if __name__ == '__main__':
    create_notebook()
    print("Jupyter notebook 'FraxlendAnalysis.ipynb' has been created successfully!") 