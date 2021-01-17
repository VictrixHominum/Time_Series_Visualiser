import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import datetime
register_matplotlib_converters()

# Data imported and date parsed
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# Remove upper and lower 2.5% of data
df = df[(df.value >= df.value.quantile(0.025)) & (df.value <= df.value.quantile(0.975))]

df = df.rename(columns={"value": "Page Views"})


def draw_line_plot():
    axes = df.plot.line(figsize=(40, 10))
    axes.set_xlabel("Date")
    axes.set_ylabel("Page Views")
    axes.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    fig = axes.get_figure()
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    df_bar = df.copy()
    df_bar["month"] = df_bar.index.month
    df_bar["year"] = df_bar.index.year
    df_bar_grouped = df_bar.groupby(["year", "month"])["Page Views"].mean().unstack()
    
    axes = df_bar_grouped.plot.bar(figsize=(10,10))
    axes.set_xlabel("Years")
    axes.set_ylabel("Average Page Views")
    axes.legend(labels = [datetime.datetime.strptime(str(d), "%m").strftime("%B") for d in sorted(df_bar.index.month.unique())])
    fig = axes.get_figure()
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    fig, axes = plt.subplots(figsize=(12, 7), ncols=2, sharex=False)
    sns.despine(left=True)

    ax1 = sns.boxplot(x='year', y='Page Views', data=df_box, ax=axes[0])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_title('Year-wise Box Plot (Trend)')

    ax2 = sns.boxplot(x='month', y='Page Views', data=df_box, ax=axes[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    fig.savefig('box_plot.png')
    return fig
