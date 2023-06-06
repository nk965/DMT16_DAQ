import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()

# Generate some example data
x = [1, 2, 3, 4, 5]
y1 = [10, 20, 30, 40, 50]
y2 = [5, 10, 15, 20, 25]

# Create the first Seaborn plot
sns.lineplot(x=x, y=y1)

# Create the second Seaborn plot using the same x-axis but a different y-axis
ax2 = plt.twinx()
sns.lineplot(x=x, y=y2, ax=ax2)

# Set labels and titles
plt.xlabel('X')
plt.ylabel('Y1', color='blue')
ax2.set_ylabel('Y2', color='red')
ax2.set_ylim(0,50)
plt.title('Two Y-Axes Plot')

# Show the plot
plt.show()