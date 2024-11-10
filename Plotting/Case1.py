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
    'Case I': ['$K=60$'] * 6 + ['$K=100$'] * 6 + ['$K=140$'] * 6,
    'Bias_Euler': [-11.309, -10.067, -8.7578, -7.6602, -7.0415, -6.2607,
                   -19.290, -18.186, -16.895, -15.682, -14.405, -13.313,
                   -15.811, -15.024, -14.239, -13.453, -12.844, -12.200],
    'Time_Euler': [0.6, 1.1, 2.2, 4.3, 9.6, 20.3,
                   0.6, 1.1, 2.1, 4.2, 8.2, 21.7,
                   0.7, 1.3, 2.3, 4.6, 9.8, 21.5],
    'Bias_QE_M': [-0.00863, 0.05309, 0.05150, 0.00839, -0.01370, 0.03051,
                   -0.21578, -0.10644, -0.00682, -0.00022, 0.01341, 0.00307,
                   0.08830, 0.01813, -0.00659, -0.00517, 0.00111, 0.00610],
    'Time_QE_M': [3.6, 6.1, 7.8, 13.4, 25.9, 40.7,
                   4.0, 5.5, 7.6, 12.5, 22.9, 43.5,
                   4.0, 5.2, 7.1, 11.6, 21.3, 42.4]
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
sns.barplot(x='Delta', y='Bias_Euler', hue='Case I', data=df, ax=axes[0, 0])
axes[0, 0].set_title(r'Bias for Euler Method', fontsize=16, pad=15)
axes[0, 0].set_ylabel(r'Bias ($e(\Delta)$)', fontsize=18)
axes[0, 0].set_xlabel(r'$\Delta$', fontsize=18)
axes[0, 0].tick_params(axis='x', labelsize=14)
axes[0, 0].tick_params(axis='y', labelsize=14)
axes[0, 0].legend(title='Case I', fontsize=7, loc='lower right')

# Bias for QE-M (Top-right)
sns.barplot(x='Delta', y='Bias_QE_M', hue='Case I', data=df, ax=axes[0, 1])
axes[0, 1].set_title(r'Bias for QE-M Method', fontsize=16, pad=20)
axes[0, 1].set_ylabel(r'Bias ($e(\Delta)$)', fontsize=18)
axes[0, 1].set_xlabel(r'$\Delta$', fontsize=18)
axes[0, 1].tick_params(axis='x', labelsize=14)
axes[0, 1].tick_params(axis='y', labelsize=14)
axes[0, 1].legend(title='Case I', fontsize=7)

# Set y-axis limits for both time plots
y_min, y_max = 0, 45

# Time for Euler (Bottom-left)
sns.barplot(x='Delta', y='Time_Euler', hue='Case I', data=df, ax=axes[1, 0])
axes[1, 0].set_title(r'Time for Euler Method (in minutes)', fontsize=16, pad=15)
axes[1, 0].set_ylabel(r'Time (m)', fontsize=18)
axes[1, 0].set_xlabel(r'$\Delta$', fontsize=18)
axes[1, 0].set_ylim(y_min, y_max)
axes[1, 0].tick_params(axis='x', labelsize=14)
axes[1, 0].tick_params(axis='y', labelsize=14)
axes[1, 0].legend(title='Case I', fontsize=7)

# Time for QE-M (Bottom-right)
sns.barplot(x='Delta', y='Time_QE_M', hue='Case I', data=df, ax=axes[1, 1])
axes[1, 1].set_title(r'Time for QE-M Method (in minutes)', fontsize=16, pad=15)
axes[1, 1].set_ylabel(r'Time (m)', fontsize=18)
axes[1, 1].set_xlabel(r'$\Delta$', fontsize=18)
axes[1, 1].set_ylim(y_min, y_max)
axes[1, 1].tick_params(axis='x', labelsize=14)
axes[1, 1].tick_params(axis='y', labelsize=14)
axes[1, 1].legend(title='Case I', fontsize=7)

# Adjust the layout to prevent overlapping
plt.subplots_adjust(hspace=0.4)  # Increase vertical spacing between rows
plt.tight_layout
plt.show()
