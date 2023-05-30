import seaborn as sns
import matplotlib.pyplot as plt

# Set the seaborn style with modified grid line width
sns.set_style("whitegrid", {'grid.linewidth': 0.05})

tips = sns.load_dataset("tips")

# Create a scatter plot
sns.scatterplot(data=tips, x="total_bill", y="tip")

# Show the plot
plt.show()