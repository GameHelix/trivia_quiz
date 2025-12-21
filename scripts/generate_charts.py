#!/usr/bin/env python3
"""
Obesity Analysis - Chart Generation Script
Generates comprehensive visualizations for global obesity trends
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style for professional charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Define paths
DATA_DIR = Path(__file__).parent.parent / 'data'
CHARTS_DIR = Path(__file__).parent.parent / 'charts'
CHARTS_DIR.mkdir(exist_ok=True)

# Color palette
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#06A77D',
    'warning': '#D62828',
    'male': '#4A90E2',
    'female': '#E24A90'
}

def load_data():
    """Load obesity datasets"""
    adult_df = pd.read_csv(DATA_DIR / 'adult_obesity.csv', na_values=['-', ''])
    child_df = pd.read_csv(DATA_DIR / 'child_obesity.csv', na_values=['-', ''])

    # Convert numeric columns
    numeric_cols_adult = ['Males_Overweight', 'Males_Obesity', 'Females_Overweight',
                          'Females_Obesity', 'All_Overweight', 'All_Obesity']
    numeric_cols_child = ['Boys', 'Girls', 'All_children']

    for col in numeric_cols_adult:
        adult_df[col] = pd.to_numeric(adult_df[col], errors='coerce')

    for col in numeric_cols_child:
        child_df[col] = pd.to_numeric(child_df[col], errors='coerce')

    return adult_df, child_df


def chart1_top_countries_obesity(adult_df):
    """Chart 1: Top 20 Countries by Adult Obesity Rate"""
    # Clean and sort data
    df_clean = adult_df[adult_df['All_Obesity'].notna()].copy()
    df_top = df_clean.nlargest(20, 'All_Obesity')

    fig, ax = plt.subplots(figsize=(14, 10))
    bars = ax.barh(df_top['Country'], df_top['All_Obesity'],
                   color=COLORS['warning'], alpha=0.8, edgecolor='black', linewidth=0.5)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, df_top['All_Obesity'])):
        ax.text(val + 1, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}%', va='center', fontweight='bold', fontsize=10)

    ax.set_xlabel('Obesity Prevalence (%)', fontweight='bold', fontsize=13)
    ax.set_title('Top 20 Countries by Adult Obesity Rate\nA Global Health Crisis',
                 fontweight='bold', fontsize=16, pad=20)
    ax.set_xlim(0, max(df_top['All_Obesity']) + 8)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '1_top_countries_obesity.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Chart 1: Top countries by obesity rate")


def chart2_gender_comparison(adult_df):
    """Chart 2: Gender Comparison - Males vs Females Obesity"""
    df_clean = adult_df[(adult_df['Males_Obesity'].notna()) &
                        (adult_df['Females_Obesity'].notna())].copy()

    # Select top 15 countries by total obesity
    df_clean['Total'] = df_clean['Males_Obesity'] + df_clean['Females_Obesity']
    df_top = df_clean.nlargest(15, 'Total')

    fig, ax = plt.subplots(figsize=(14, 10))
    x = np.arange(len(df_top))
    width = 0.35

    bars1 = ax.barh(x - width/2, df_top['Males_Obesity'], width,
                    label='Males', color=COLORS['male'], alpha=0.8, edgecolor='black', linewidth=0.5)
    bars2 = ax.barh(x + width/2, df_top['Females_Obesity'], width,
                    label='Females', color=COLORS['female'], alpha=0.8, edgecolor='black', linewidth=0.5)

    ax.set_yticks(x)
    ax.set_yticklabels(df_top['Country'])
    ax.set_xlabel('Obesity Prevalence (%)', fontweight='bold', fontsize=13)
    ax.set_title('Gender Disparities in Obesity Rates\nTop 15 Countries',
                 fontweight='bold', fontsize=16, pad=20)
    ax.legend(loc='lower right', fontsize=12, frameon=True, shadow=True)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '2_gender_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Chart 2: Gender comparison")


def chart3_income_group_analysis(adult_df):
    """Chart 3: Obesity by Income Group"""
    df_clean = adult_df[adult_df['All_Obesity'].notna()].copy()

    # Calculate statistics by income group
    income_stats = df_clean.groupby('Income_group')['All_Obesity'].agg(['mean', 'median', 'std']).reset_index()
    income_stats = income_stats.sort_values('mean', ascending=False)

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(income_stats['Income_group'], income_stats['mean'],
                  color=COLORS['accent'], alpha=0.8, edgecolor='black', linewidth=1.5)

    # Add error bars for standard deviation
    ax.errorbar(income_stats['Income_group'], income_stats['mean'],
                yerr=income_stats['std'], fmt='none', color='black',
                capsize=5, capthick=2, linewidth=2, alpha=0.6)

    # Add value labels
    for bar, val, median in zip(bars, income_stats['mean'], income_stats['median']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 1,
                f'{val:.1f}%\n(median: {median:.1f}%)',
                ha='center', va='bottom', fontweight='bold', fontsize=10)

    ax.set_ylabel('Mean Obesity Prevalence (%)', fontweight='bold', fontsize=13)
    ax.set_title('Obesity Rates by Income Group\nMean ± Standard Deviation',
                 fontweight='bold', fontsize=16, pad=20)
    ax.set_ylim(0, max(income_stats['mean']) + 8)
    plt.xticks(rotation=15, ha='right')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '3_income_group_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Chart 3: Income group analysis")


def chart4_child_vs_adult_obesity(adult_df, child_df):
    """Chart 4: Child vs Adult Obesity Comparison"""
    # Merge datasets
    adult_clean = adult_df[adult_df['All_Obesity'].notna()][['Country', 'All_Obesity']].copy()
    adult_clean.rename(columns={'All_Obesity': 'Adult_Obesity'}, inplace=True)

    child_clean = child_df[child_df['All_children'].notna()][['Country', 'All_children']].copy()
    child_clean.rename(columns={'All_children': 'Child_Obesity'}, inplace=True)

    merged = pd.merge(adult_clean, child_clean, on='Country', how='inner')
    merged = merged.nlargest(15, 'Adult_Obesity')

    fig, ax = plt.subplots(figsize=(14, 10))
    x = np.arange(len(merged))
    width = 0.35

    bars1 = ax.barh(x - width/2, merged['Adult_Obesity'], width,
                    label='Adults', color=COLORS['primary'], alpha=0.8, edgecolor='black', linewidth=0.5)
    bars2 = ax.barh(x + width/2, merged['Child_Obesity'], width,
                    label='Children', color=COLORS['success'], alpha=0.8, edgecolor='black', linewidth=0.5)

    ax.set_yticks(x)
    ax.set_yticklabels(merged['Country'])
    ax.set_xlabel('Obesity Prevalence (%)', fontweight='bold', fontsize=13)
    ax.set_title('Child vs Adult Obesity Rates\nMulti-Generational Crisis',
                 fontweight='bold', fontsize=16, pad=20)
    ax.legend(loc='lower right', fontsize=12, frameon=True, shadow=True)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '4_child_vs_adult.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Chart 4: Child vs adult comparison")


def chart5_pacific_islands_crisis(adult_df):
    """Chart 5: Pacific Islands Obesity Crisis"""
    pacific = ['Cook Islands', 'Nauru', 'Tonga', 'American Samoa', 'Samoa',
               'Federated States of Micronesia', 'Palau', 'Kiribati', 'Tuvalu',
               'Niue', 'Wallis and Futuna']

    df_pacific = adult_df[adult_df['Country'].isin(pacific)].copy()
    df_pacific = df_pacific[df_pacific['All_Obesity'].notna()]
    df_pacific = df_pacific.sort_values('All_Obesity', ascending=False)

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(df_pacific['Country'], df_pacific['All_Obesity'],
                  color=COLORS['warning'], alpha=0.9, edgecolor='darkred', linewidth=2)

    # Add value labels
    for bar, val in zip(bars, df_pacific['All_Obesity']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 1,
                f'{val:.1f}%', ha='center', va='bottom',
                fontweight='bold', fontsize=11, color='darkred')

    ax.set_ylabel('Obesity Prevalence (%)', fontweight='bold', fontsize=13)
    ax.set_title('Pacific Islands: The World\'s Obesity Hotspot\nExceptional Rates Above 50%',
                 fontweight='bold', fontsize=16, pad=20, color='darkred')
    ax.set_ylim(0, max(df_pacific['All_Obesity']) + 8)
    plt.xticks(rotation=45, ha='right')
    ax.grid(axis='y', alpha=0.3)
    ax.axhline(y=50, color='red', linestyle='--', linewidth=2, alpha=0.5, label='50% threshold')
    ax.legend()

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '5_pacific_islands_crisis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Chart 5: Pacific islands crisis")


def chart6_regional_heatmap(adult_df):
    """Chart 6: Regional Obesity Heatmap"""
    # Define regions
    regions = {
        'North America': ['United States', 'Canada', 'Mexico'],
        'South America': ['Brazil', 'Argentina', 'Chile', 'Peru', 'Colombia', 'Ecuador', 'Bolivia', 'Uruguay'],
        'Europe': ['United Kingdom', 'Germany', 'France', 'Italy', 'Spain', 'Poland', 'Greece', 'Romania',
                   'Netherlands', 'Belgium', 'Austria', 'Switzerland', 'Sweden', 'Norway', 'Denmark', 'Finland',
                   'Portugal', 'Czech Republic', 'Hungary', 'Ireland', 'Russia', 'Ukraine'],
        'Middle East': ['Saudi Arabia', 'Turkey', 'Iran', 'Iraq', 'Jordan', 'Lebanon', 'Israel', 'Qatar',
                        'Bahrain', 'Oman', 'United Arab Emirates', 'Kuwait', 'Egypt'],
        'Asia': ['China', 'Japan', 'India', 'Indonesia', 'Philippines', 'Vietnam', 'Thailand', 'Bangladesh',
                 'South Korea', 'Singapore', 'Malaysia', 'Pakistan'],
        'Africa': ['South Africa', 'Ethiopia', 'Kenya', 'Nigeria', 'Morocco', 'Algeria'],
        'Oceania': ['Australia', 'New Zealand']
    }

    # Calculate regional averages
    regional_data = []
    for region, countries in regions.items():
        region_df = adult_df[adult_df['Country'].isin(countries)]
        male_avg = region_df['Males_Obesity'].mean()
        female_avg = region_df['Females_Obesity'].mean()
        all_avg = region_df['All_Obesity'].mean()
        regional_data.append({
            'Region': region,
            'Male': male_avg,
            'Female': female_avg,
            'Overall': all_avg
        })

    regional_df = pd.DataFrame(regional_data)
    regional_df = regional_df.set_index('Region')

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(regional_df, annot=True, fmt='.1f', cmap='YlOrRd',
                cbar_kws={'label': 'Obesity Prevalence (%)'},
                linewidths=2, linecolor='white', ax=ax,
                vmin=0, vmax=40, annot_kws={'fontsize': 12, 'fontweight': 'bold'})

    ax.set_title('Global Regional Obesity Heatmap\nAverage Prevalence by Gender and Region',
                 fontweight='bold', fontsize=16, pad=20)
    ax.set_ylabel('')
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(rotation=0, fontsize=11)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '6_regional_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Chart 6: Regional heatmap")


def chart7_high_income_paradox(adult_df):
    """Chart 7: High Income Countries Obesity Paradox"""
    high_income = adult_df[adult_df['Income_group'] == 'High income'].copy()
    high_income = high_income[high_income['All_Obesity'].notna()]
    high_income = high_income.nlargest(15, 'All_Obesity')

    fig, ax = plt.subplots(figsize=(14, 9))

    # Create scatter plot with country labels
    scatter = ax.scatter(high_income['Males_Obesity'], high_income['Females_Obesity'],
                        s=high_income['All_Obesity']*20, alpha=0.6,
                        c=high_income['All_Obesity'], cmap='Reds',
                        edgecolors='black', linewidth=1.5)

    # Add country labels
    for idx, row in high_income.iterrows():
        ax.annotate(row['Country'],
                   (row['Males_Obesity'], row['Females_Obesity']),
                   fontsize=9, ha='center', fontweight='bold')

    # Add diagonal line (equal obesity)
    max_val = max(high_income['Males_Obesity'].max(), high_income['Females_Obesity'].max())
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.3, linewidth=2, label='Equal obesity')

    ax.set_xlabel('Male Obesity (%)', fontweight='bold', fontsize=13)
    ax.set_ylabel('Female Obesity (%)', fontweight='bold', fontsize=13)
    ax.set_title('High-Income Countries Obesity Paradox\nMale vs Female Obesity (bubble size = overall rate)',
                 fontweight='bold', fontsize=16, pad=20)
    ax.grid(alpha=0.3)
    ax.legend()

    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Overall Obesity (%)', fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '7_high_income_paradox.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Chart 7: High income paradox")


def chart8_child_obesity_hotspots(child_df):
    """Chart 8: Child Obesity Hotspots"""
    df_clean = child_df[child_df['All_children'].notna()].copy()
    df_top = df_clean.nlargest(20, 'All_children')

    fig, ax = plt.subplots(figsize=(14, 10))
    bars = ax.barh(df_top['Country'], df_top['All_children'],
                   color=COLORS['secondary'], alpha=0.8, edgecolor='black', linewidth=0.5)

    # Color code extreme cases
    for i, (bar, val) in enumerate(zip(bars, df_top['All_children'])):
        if val > 50:
            bar.set_color('darkred')
            bar.set_alpha(0.9)
        ax.text(val + 1, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}%', va='center', fontweight='bold', fontsize=10)

    ax.set_xlabel('Child Obesity/Overweight Prevalence (%)', fontweight='bold', fontsize=13)
    ax.set_title('Top 20 Countries by Child Obesity\nThe Future Generation at Risk',
                 fontweight='bold', fontsize=16, pad=20)
    ax.set_xlim(0, max(df_top['All_children']) + 8)
    ax.grid(axis='x', alpha=0.3)
    ax.axvline(x=50, color='red', linestyle='--', linewidth=2, alpha=0.5)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '8_child_obesity_hotspots.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Chart 8: Child obesity hotspots")


def chart9_distribution_analysis(adult_df):
    """Chart 9: Distribution of Obesity Rates"""
    df_clean = adult_df[adult_df['All_Obesity'].notna()].copy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Histogram
    ax1.hist(df_clean['All_Obesity'], bins=20, color=COLORS['primary'],
            alpha=0.7, edgecolor='black', linewidth=1.2)
    ax1.axvline(df_clean['All_Obesity'].mean(), color='red', linestyle='--',
               linewidth=2, label=f'Mean: {df_clean["All_Obesity"].mean():.1f}%')
    ax1.axvline(df_clean['All_Obesity'].median(), color='green', linestyle='--',
               linewidth=2, label=f'Median: {df_clean["All_Obesity"].median():.1f}%')
    ax1.set_xlabel('Obesity Prevalence (%)', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Number of Countries', fontweight='bold', fontsize=12)
    ax1.set_title('Distribution of Adult Obesity Rates', fontweight='bold', fontsize=14)
    ax1.legend(fontsize=11)
    ax1.grid(alpha=0.3)

    # Box plot by income group
    income_groups = df_clean.groupby('Income_group')['All_Obesity'].apply(list)
    bp = ax2.boxplot([income_groups[ig] for ig in income_groups.index if len(income_groups[ig]) > 0],
                     labels=[ig for ig in income_groups.index if len(income_groups[ig]) > 0],
                     patch_artist=True, showmeans=True, meanline=True)

    # Color the boxes
    colors_list = [COLORS['warning'], COLORS['accent'], COLORS['success'], COLORS['primary']]
    for patch, color in zip(bp['boxes'], colors_list[:len(bp['boxes'])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax2.set_ylabel('Obesity Prevalence (%)', fontweight='bold', fontsize=12)
    ax2.set_title('Obesity Distribution by Income Group', fontweight='bold', fontsize=14)
    ax2.grid(alpha=0.3, axis='y')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=15, ha='right')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '9_distribution_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Chart 9: Distribution analysis")


def chart10_key_statistics_summary(adult_df, child_df):
    """Chart 10: Key Statistics Summary Dashboard"""
    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots(figsize=(18, 12), facecolor='white')
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.axis('off')

    # Calculate statistics
    adult_clean = adult_df[adult_df['All_Obesity'].notna()]
    child_clean = child_df[child_df['All_children'].notna()]

    stats = [
        ('Global Adult\nMean Obesity', f"{adult_clean['All_Obesity'].mean():.1f}%", COLORS['primary']),
        ('Global Child\nMean Obesity', f"{child_clean['All_children'].mean():.1f}%", COLORS['success']),
        ('Highest Adult\nObesity', f"{adult_clean['All_Obesity'].max():.1f}%\n{adult_clean.loc[adult_clean['All_Obesity'].idxmax(), 'Country']}", COLORS['warning']),
        ('Lowest Adult\nObesity', f"{adult_clean['All_Obesity'].min():.1f}%\n{adult_clean.loc[adult_clean['All_Obesity'].idxmin(), 'Country']}", COLORS['accent']),
        ('Countries with\n>30% Obesity', f"{len(adult_clean[adult_clean['All_Obesity'] > 30])}", COLORS['secondary']),
        ('Gender Gap\n(F - M)', f"+{(adult_clean['Females_Obesity'].mean() - adult_clean['Males_Obesity'].mean()):.1f}%", COLORS['female']),
        ('High Income\nMean', f"{adult_clean[adult_clean['Income_group']=='High income']['All_Obesity'].mean():.1f}%", COLORS['primary']),
        ('Low Income\nMean', f"{adult_clean[adult_clean['Income_group']=='Low income']['All_Obesity'].mean():.1f}%", COLORS['accent']),
        ('Pacific Islands\nMean', f"{adult_clean[adult_clean['Country'].isin(['Cook Islands', 'Nauru', 'Tonga', 'American Samoa'])]['All_Obesity'].mean():.1f}%", COLORS['warning'])
    ]

    # Draw stat boxes
    for idx, (label, value, color) in enumerate(stats):
        row = 2 - (idx // 3)  # Invert row to start from top
        col = idx % 3

        x = col * 1.0 + 0.05
        y = row * 1.0 + 0.05
        width = 0.9
        height = 0.9

        # Draw rectangle
        rect = Rectangle((x, y), width, height, facecolor=color,
                         edgecolor='black', linewidth=3, alpha=0.9)
        ax.add_patch(rect)

        # Add value text (larger, centered)
        ax.text(x + width/2, y + height*0.65, value,
               ha='center', va='center', fontsize=32,
               fontweight='bold', color='white')

        # Add label text (smaller, bottom)
        ax.text(x + width/2, y + height*0.25, label,
               ha='center', va='center', fontsize=14,
               fontweight='bold', color='white')

    # Add title
    fig.suptitle('Global Obesity Statistics Dashboard\nKey Findings at a Glance',
                fontweight='bold', fontsize=24, y=0.96)

    plt.savefig(CHARTS_DIR / '10_statistics_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Chart 10: Statistics dashboard")


def main():
    """Generate all charts"""
    print("\n" + "="*60)
    print("  OBESITY ANALYSIS - CHART GENERATION")
    print("="*60 + "\n")

    # Load data
    print("Loading data...")
    adult_df, child_df = load_data()
    print(f"✓ Loaded {len(adult_df)} adult records")
    print(f"✓ Loaded {len(child_df)} child records\n")

    print("Generating charts...")
    print("-" * 60)

    # Generate all charts
    chart1_top_countries_obesity(adult_df)
    chart2_gender_comparison(adult_df)
    chart3_income_group_analysis(adult_df)
    chart4_child_vs_adult_obesity(adult_df, child_df)
    chart5_pacific_islands_crisis(adult_df)
    chart6_regional_heatmap(adult_df)
    chart7_high_income_paradox(adult_df)
    chart8_child_obesity_hotspots(child_df)
    chart9_distribution_analysis(adult_df)
    chart10_key_statistics_summary(adult_df, child_df)

    print("-" * 60)
    print(f"\n✓ All charts generated successfully!")
    print(f"✓ Charts saved to: {CHARTS_DIR}\n")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
