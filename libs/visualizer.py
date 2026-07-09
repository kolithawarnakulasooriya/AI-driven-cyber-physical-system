
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Visualizer:
    def __init__(self):
        pass

    def describe_data(self, df: pd.DataFrame):

        print("describing data...")
        print(df.describe())
        print("========================================")

        print("info...")
        print(df.info())
        print("========================================")

        print("data types...")
        print(df.dtypes)
        print("========================================")

        print("isnull...")
        print(df.isnull().sum())
        print("========================================")

        print("duplicates...")
        print(df.duplicated().sum())
        print("========================================")

    def visualize_raw_data(self, data:list = [], figsize=(15,8), title="", x_label="", y_label="", grid=False):
        plt.figure(figsize=figsize)
        for key in data:
            plt.scatter(x = key['X'], y = key['Y'], label = key['name'])
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()
        plt.grid(grid)
        plt.show()

    def visualize_distributions(self, data:list = [], figsize=(15,8), title="", grid=False):
        if not data:
            print("No data to visualize.")
            return

        n_cols = 3
        n_rows = max(1, (len(data) + n_cols - 1) // n_cols)

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(figsize[0], figsize[1] * n_rows))
        axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

        for ax, key in zip(axes, data):
            sns.histplot(key['X'], kde=True, ax=ax)
            ax.set_title(key.get('name', ''))
            ax.set_xlabel(key.get('x_label', ''))
            ax.set_ylabel(key.get('y_label', ''))
            ax.grid(grid)

        for ax in axes[len(data):]:
            ax.axis("off")

        fig.suptitle(title)
        plt.tight_layout()
        plt.show()

    def visualize_outliers(self, data:list = [], figsize=(15,8), title="", grid=False):
        if not data:
            print("No data to visualize.")
            return

        n_cols = 3
        n_rows = max(1, (len(data) + n_cols - 1) // n_cols)

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(figsize[0], figsize[1] * n_rows))
        axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

        for ax, key in zip(axes, data):
            sns.boxplot(key['X'], ax=ax)
            ax.set_title(key.get('name', ''))
            ax.set_xlabel(key.get('x_label', ''))
            ax.set_ylabel(key.get('y_label', ''))
            ax.grid(grid)

        for ax in axes[len(data):]:
            ax.axis("off")

        fig.suptitle(title)
        plt.tight_layout()
        plt.show()

    def visualize_correlations(self, df: pd.DataFrame, figsize=(15,8), title="", method="pearson"):
        plt.figure(figsize=figsize)
        sns.heatmap(df.corr(method=method), annot=True, cmap='coolwarm', linewidths=0.5)
        plt.title(title)
        plt.show()
