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
    'Case III': ['$K=60$'] * 6 + ['$K=100$'] * 6 + ['$K=140$'] * 6,
    'Bias_Euler': [-23.3858, -18.1660, -14.2592, -12.1657, -11.1446, -9.9601,
                   -34.2395, -28.3605, -24.4228, -22.3514, -20.5244, -19.1239,
                   -31.4480, -27.2008, -23.2902, -21.4081, -19.4761, -17.8300],
    'Time_Euler': [1.05, 1.81, 3.65, 7.10, 14.03, 29.96,
                   4.33, 6.50, 7.88, 8.82, 12.85, 29.88,
                   5.34, 6.37, 7.78, 9.01, 12.55, 28.65],
    'Bias_QE_M': [-0.4179, -0.1901, -0.1667, -0.1457, -0.1732, -0.1839,
                   -0.0394, -0.2462, -0.3786, -0.3639, -0.4052, -0.4200,
                   0.0267, -0.2350, -0.3012, -0.3639, -0.4122, -0.4500],
    'Time_QE_M': [4.55, 7.09, 11.70, 20.85, 38.08, 74.76,
                   4.27, 6.17, 9.81, 22.01, 40.54, 78.63,
                   5.37, 7.76, 10.59, 22.34, 42.71, 79.64]
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
sns.barplot(x='Delta', y='Bias_Euler', hue='Case III', data=df, ax=axes[0, 0])
axes[0, 0].set_title(r'Bias for Euler Method', fontsize=18, pad=15)  # Increase `pad` for more space
axes[0, 0].set_ylabel(r'Bias ($e(\Delta)$)', fontsize=18)
axes[0, 0].set_xlabel(r'$\Delta$', fontsize=18)
axes[0, 0].tick_params(axis='x', labelsize=14)
axes[0, 0].tick_params(axis='y', labelsize=14)
# Move legend to bottom right
axes[0, 0].legend(title='Case III', fontsize=10, loc='lower right')  # Smaller legend, moved to lower right

# Bias for QE-M (Top-right)
# Bias for QE-M (Top-right)
sns.barplot(x='Delta', y='Bias_QE_M', hue='Case III', data=df, ax=axes[0, 1])
axes[0, 1].set_title(r'Bias for QE-M Method', fontsize=18, pad=15)  # Adjust pad as needed
axes[0, 1].set_ylabel(r'Bias ($e(\Delta)$)', fontsize=18)
axes[0, 1].set_xlabel(r'$\Delta$', fontsize=18)
axes[0, 1].tick_params(axis='x', labelsize=14)
axes[0, 1].tick_params(axis='y', labelsize=14)

# Adjust legend position to avoid overlap
axes[0, 1].legend(title='Case III', fontsize=10, loc='upper left', bbox_to_anchor=(0.1, 0.4))  # Move legend to the right


# Set y-axis limits for both time plots
y_min, y_max = 0, 80

# Time for Euler (Bottom-left)
sns.barplot(x='Delta', y='Time_Euler', hue='Case III', data=df, ax=axes[1, 0])
axes[1, 0].set_title(r'Time for Euler Method (in minutes)', fontsize=18, pad=15)  # Increase `pad` for more space
axes[1, 0].set_ylabel(r'Time (m)', fontsize=18)
axes[1, 0].set_xlabel(r'$\Delta$', fontsize=18)
axes[1, 0].set_ylim(y_min, y_max)
axes[1, 0].tick_params(axis='x', labelsize=14)
axes[1, 0].tick_params(axis='y', labelsize=14)
axes[1, 0].legend(title='Case III', fontsize=10, loc='best')  # Smaller legend

# Time for QE-M (Bottom-right)
sns.barplot(x='Delta', y='Time_QE_M', hue='Case III', data=df, ax=axes[1, 1])
axes[1, 1].set_title(r'Time for QE-M Method (in minutes)', fontsize=18, pad=15)  # Increase `pad` for more space
axes[1, 1].set_ylabel(r'Time (m)', fontsize=18)
axes[1, 1].set_xlabel(r'$\Delta$', fontsize=18)
axes[1, 1].set_ylim(y_min, y_max)
axes[1, 1].tick_params(axis='x', labelsize=14)
axes[1, 1].tick_params(axis='y', labelsize=14)
axes[1, 1].legend(title='Case III', fontsize=10, loc='best')  # Smaller legend

# Adjust the layout to prevent overlapping
plt.subplots_adjust(hspace=0.4)  # Increase `hspace` and set `top` for better spacing

plt.show()
