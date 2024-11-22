import matplotlib.pyplot as plt

# Configure Matplotlib to use LaTeX for text rendering
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# Data for the plots
N_values = [10**3, 10**4, 10**5, 10**6]
bias_euler = [-16.54658388891954, -15.922168766815467, -15.622747932510684, -15.659216673590254]
bias_qem = [0.25808037435313835, 0.05182597699853986, 0.03539258589101202, 0.006350744704317179]

# Create a stacked plot
fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# Plot for EulerDisc method
axes[0].plot(N_values, bias_euler, marker='o', color='blue', label='EulerDisc')
axes[0].axhline(0, color='black', linestyle='--', linewidth=0.8, label=r'$y=0$')
axes[0].set_xscale('log')
axes[0].set_ylabel(r'Bias ($e(\Delta)$)')
axes[0].set_title('Bias vs. Number of Paths (EulerDisc)')
axes[0].grid(True)
axes[0].legend()

# Plot for QEMDisc method
axes[1].plot(N_values, bias_qem, marker='o', color='green', label='QEMDisc')
axes[1].axhline(0, color='black', linestyle='--', linewidth=0.8, label=r'$y=0$')
axes[1].set_xscale('log')
axes[1].set_xlabel(r'Number of Paths ($N$)')
axes[1].set_ylabel(r'Bias ($e(\Delta)$)')
axes[1].set_title('Bias vs. Number of Paths (QEMDisc)')
axes[1].grid(True)
axes[1].legend()

# Adjust layout for better visualization
plt.tight_layout()

# Show the plots
plt.show()
