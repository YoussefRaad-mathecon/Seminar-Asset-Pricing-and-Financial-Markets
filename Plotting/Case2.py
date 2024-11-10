import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure Matplotlib to use LaTeX for text rendering
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# Define the data as a dictionary
data = { 
    'K': [60, 60, 60, 60, 60, 60,
          100, 100, 100, 100, 100, 100,
          140, 140, 140, 140, 140, 140],
    'Delta': ['1/1', '1/2', '1/4', '1/8', '1/16', '1/32',
              '1/1', '1/2', '1/4', '1/8', '1/16', '1/32',
              '1/1', '1/2', '1/4', '1/8', '1/16', '1/32'],
    'Case II': ['$K=60$'] * 6 + ['$K=100$'] * 6 + ['$K=140$'] * 6,
    'Bias_Euler': [-5.7897, -4.4864, -3.2522, -2.3008, -1.6642, -1.4461,
                   -8.6943, -7.9377, -6.3953, -5.0601, -4.1210, -3.3890,
                   -9.4718, -8.6841, -7.9196, -6.9277, -6.2815, -5.8093],
    'Time_Euler': [0.49, 0.73, 1.30, 2.41, 4.56, 9.36,
                   0.44, 0.70, 1.28, 2.42, 4.92, 9.91,
                   0.44, 0.68, 1.35, 2.55, 4.98, 10.02],
    'Bias_QE_M': [-0.00174, -0.00296, 0.04700, -0.01771, -0.04467, -0.02734,
                   0.09509, -0.03973, -0.07598, 0.02733, 0.06960, -0.00796,
                   0.50122, 0.28617, 0.05839, 0.01283, -0.02590, -0.00600],
    'Time_QE_M': [3.84, 4.49, 8.31, 9.91, 16.71, 24.52,
                   3.12, 3.68, 4.94, 7.50, 12.67, 27.35,
                   4.19, 5.09, 6.38, 7.95, 13.18, 29.88]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Set a black, white, and grey color palette
colors = ["#2C3E50",  # Midnight Blue
          "#95A5A6",  # Concrete Gray
          "#BDC3C7"]  # Silver
sns.set_palette(colors)

# Increase the font size for ticks and labels
sns.set_context("notebook", font_scale=1.5)  # Increase font sizes globally

# Create a single figure with a 2x2 grid layout
fig, axes = plt.subplots(2, 2, figsize=(20, 15))

# Bias for Euler (Top-left)
sns.barplot(x='Delta', y='Bias_Euler', hue='Case II', data=df, ax=axes[0, 0])
axes[0, 0].set_title(r'Bias for Euler Method', fontsize=18, pad=15)  # Increase `pad` for more space
axes[0, 0].set_ylabel(r'Bias ($e(\Delta)$)', fontsize=18)
axes[0, 0].set_xlabel(r'$\Delta$', fontsize=18)
axes[0, 0].tick_params(axis='x', labelsize=14)
axes[0, 0].tick_params(axis='y', labelsize=14)
# Move legend to bottom right
axes[0, 0].legend(title='Case II', fontsize=10, loc='lower right')  # Smaller legend, moved to lower right

# Bias for QE-M (Top-right)
sns.barplot(x='Delta', y='Bias_QE_M', hue='Case II', data=df, ax=axes[0, 1])
axes[0, 1].set_title(r'Bias for QE-M Method', fontsize=18, pad=15)  # Increase `pad` for more space
axes[0, 1].set_ylabel(r'Bias ($e(\Delta)$)', fontsize=18)
axes[0, 1].set_xlabel(r'$\Delta$', fontsize=18)
axes[0, 1].tick_params(axis='x', labelsize=14)
axes[0, 1].tick_params(axis='y', labelsize=14)
axes[0, 1].legend(title='Case II', fontsize=10, loc='best')  # Smaller legend

# Set y-axis limits for both time plots
y_min, y_max = 0, 45

# Time for Euler (Bottom-left)
sns.barplot(x='Delta', y='Time_Euler', hue='Case II', data=df, ax=axes[1, 0])
axes[1, 0].set_title(r'Time for Euler Method (in minutes)', fontsize=18, pad=15)  # Increase `pad` for more space
axes[1, 0].set_ylabel(r'Time (m)', fontsize=18)
axes[1, 0].set_xlabel(r'$\Delta$', fontsize=18)
axes[1, 0].set_ylim(y_min, y_max)
axes[1, 0].tick_params(axis='x', labelsize=14)
axes[1, 0].tick_params(axis='y', labelsize=14)
axes[1, 0].legend(title='Case II', fontsize=10, loc='best')  # Smaller legend

# Time for QE-M (Bottom-right)
sns.barplot(x='Delta', y='Time_QE_M', hue='Case II', data=df, ax=axes[1, 1])
axes[1, 1].set_title(r'Time for QE-M Method (in minutes)', fontsize=18, pad=15)  # Increase `pad` for more space
axes[1, 1].set_ylabel(r'Time (m)', fontsize=18)
axes[1, 1].set_xlabel(r'$\Delta$', fontsize=18)
axes[1, 1].set_ylim(y_min, y_max)
axes[1, 1].tick_params(axis='x', labelsize=14)
axes[1, 1].tick_params(axis='y', labelsize=14)
axes[1, 1].legend(title='Case II', fontsize=10, loc='best')  # Smaller legend

# Adjust the layout to prevent overlapping
plt.subplots_adjust(hspace=0.4)  # Increase `hspace` and set `top` for better spacing

plt.show()
