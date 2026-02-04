"""
Dashboard Visualization Script
===============================
Creates comprehensive visualizations for the University of Akron student data analysis.
Generates dashboards suitable for presentation to various stakeholders.

Date: December 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Color palette for consistent theming
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'accent': '#2ca02c',
    'highlight': '#d62728',
    'neutral': '#9467bd'
}


def load_processed_data():
    """Load and preprocess data for visualization."""
    # Load raw data
    app_df = pd.read_csv('Applications _Data.csv')
    enroll_df = pd.read_csv('Enrollment_Data.csv')
    
    # Basic preprocessing (simplified version)
    app_df['Applied Date'] = pd.to_datetime(app_df['Applied Date'], errors='coerce')
    app_df['Confirmed Date'] = pd.to_datetime(app_df['Confirmed Date'], errors='coerce')
    app_df['Enrolled'] = app_df['Confirmed Date'].notna()
    app_df['GPA'] = pd.to_numeric(app_df['GPA'], errors='coerce')
    app_df['ACT_SCORE'] = pd.to_numeric(app_df['ACT_SCORE'], errors='coerce')
    app_df['Scholarship_Amount'] = pd.to_numeric(app_df['Scholarship_Amount'], errors='coerce')
    
    enroll_df['FirstTerm_GPA'] = pd.to_numeric(enroll_df['FirstTerm_GPA'], errors='coerce')
    enroll_df['FirstTerm_CreditHours'] = pd.to_numeric(enroll_df['FirstTerm_CreditHours'], errors='coerce')
    enroll_df['OneYear_Retention'] = enroll_df['OneYear retention'].apply(
        lambda x: 1 if pd.notna(x) and str(x).strip() == '1' else 0
    )
    
    return app_df, enroll_df


def create_executive_dashboard():
    """
    Create executive-level dashboard with key metrics and trends.
    Suitable for Provost's Office and senior leadership.
    """
    app_df, enroll_df = load_processed_data()
    
    # Use GridSpec with tight_layout so plots flexibly avoid overlap, and
    # reserve a band at the top for the dashboard title via the rect argument.
    fig = plt.figure(figsize=(18, 10))
    gs = GridSpec(3, 3, figure=fig)
    
    # Title
    fig.suptitle(
        'University of Akron: Executive Dashboard\nStudent Analytics Overview (2016-2021)',
        fontsize=18,
        fontweight='bold',
        y=0.98,
    )
    
    # 1. Applications and Enrollments Over Time
    ax1 = fig.add_subplot(gs[0, :2])
    app_by_year = app_df.groupby('Year').agg({
        'ID': 'count',
        'Enrolled': 'sum'
    })
    app_by_year.plot(kind='line', ax=ax1, marker='o', linewidth=2, 
                     color=[COLORS['primary'], COLORS['secondary']])
    ax1.set_title('Applications and Enrollments by Year', fontweight='bold')
    ax1.set_xlabel('Academic Year')
    ax1.set_ylabel('Count')
    ax1.legend(['Applications', 'Enrollments'])
    ax1.grid(True, alpha=0.3)
    
    # 2. Enrollment Rate Trend
    ax2 = fig.add_subplot(gs[0, 2])
    enrollment_rate = (app_df.groupby('Year')['Enrolled'].sum() / 
                      app_df.groupby('Year')['ID'].count() * 100)
    enrollment_rate.plot(kind='bar', ax=ax2, color=COLORS['accent'])
    ax2.set_title('Enrollment Rate (%)', fontweight='bold')
    ax2.set_xlabel('Academic Year')
    ax2.set_ylabel('')  # remove vertical axis label to avoid overlap between plots
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Top 5 Colleges by Enrollment
    ax3 = fig.add_subplot(gs[1, 0])
    top_colleges = enroll_df['COLLEGE_DESCR'].value_counts().head(5)
    top_colleges.plot(kind='barh', ax=ax3, color=COLORS['primary'])
    ax3.set_title('Top 5 Colleges by Enrollment', fontweight='bold')
    ax3.set_xlabel('Number of Students')
    
    # 4. Gender Distribution
    ax4 = fig.add_subplot(gs[1, 1])
    gender_dist = app_df['Gender'].value_counts()
    # Use legend instead of text labels on the pie to avoid overlapping text
    # Matplotlib pie returns (patches, texts, autotexts); we only need the wedges
    wedges, _texts, _autotexts = ax4.pie(
        gender_dist.values,
        labels=None,
        autopct='%1.1f%%',
        startangle=90
    )
    ax4.legend(
        wedges,
        gender_dist.index,
        title='Gender',
        bbox_to_anchor=(1.05, 0.5),
        loc='center left',
        fontsize=8
    )
    ax4.set_title('Gender Distribution', fontweight='bold')
    
    # 5. Ethnicity Distribution (Top 5)
    ax5 = fig.add_subplot(gs[1, 2])
    ethnicity_dist = app_df['Ethnicity'].value_counts().head(5)
    ethnicity_dist.plot(kind='bar', ax=ax5, color=COLORS['accent'])
    ax5.set_title('Top 5 Ethnicity Groups', fontweight='bold')
    ax5.set_xlabel('Ethnicity')
    ax5.set_ylabel('Count')
    ax5.tick_params(axis='x', rotation=45)
    
    # 6. Average GPA Trend
    ax6 = fig.add_subplot(gs[2, 0])
    enrolled = app_df[app_df['Enrolled'] == True]
    gpa_by_year = enrolled.groupby('Year')['GPA'].mean()
    gpa_by_year.plot(kind='line', ax=ax6, marker='o', color=COLORS['highlight'], linewidth=2)
    ax6.set_title('Average GPA Trend (Enrolled Students)', fontweight='bold')
    ax6.set_xlabel('Academic Year')
    ax6.set_ylabel('GPA')
    ax6.grid(True, alpha=0.3)
    
    # 7. First-Year Retention Rate
    ax7 = fig.add_subplot(gs[2, 1])
    retention_by_year = enroll_df.groupby('YEAR')['OneYear_Retention'].mean() * 100
    retention_by_year.plot(kind='bar', ax=ax7, color=COLORS['neutral'])
    ax7.set_title('1-Year Retention Rate by Year', fontweight='bold')
    ax7.set_xlabel('Academic Year')
    ax7.set_ylabel('Retention Rate (%)')
    ax7.tick_params(axis='x', rotation=45)
    
    # 8. Scholarship Distribution
    ax8 = fig.add_subplot(gs[2, 2])
    enrolled_with_scholarship = enrolled[enrolled['Scholarship_Amount'] > 0]
    scholarship_ranges = pd.cut(enrolled_with_scholarship['Scholarship_Amount'], 
                                bins=[0, 1000, 3000, 5000, 10000, float('inf')],
                                labels=['<$1K', '$1K-$3K', '$3K-$5K', '$5K-$10K', '>$10K'])
    scholarship_ranges.value_counts().plot(kind='bar', ax=ax8, color=COLORS['secondary'])
    ax8.set_title('Scholarship Amount Distribution', fontweight='bold')
    ax8.set_xlabel('Scholarship Range')
    ax8.set_ylabel('Number of Students')
    ax8.tick_params(axis='x', rotation=45)

    fig.tight_layout(rect=[0.03, 0.05, 0.97, 0.90])
    plt.savefig('Executive_Dashboard.png', dpi=300, bbox_inches='tight')
    print("Executive Dashboard saved as 'Executive_Dashboard.png'")
    plt.close()


def create_admissions_dashboard():
    """
    Create dashboard focused on admissions metrics.
    Suitable for Admissions Office.
    """
    app_df, enroll_df = load_processed_data()
    
    fig = plt.figure(figsize=(18, 10))
    gs = GridSpec(3, 3, figure=fig)
    
    fig.suptitle(
        'Admissions Office Dashboard\nApplication and Enrollment Analytics',
        fontsize=18,
        fontweight='bold',
        y=0.98,
    )
    
    # 1. Application Volume by Month
    ax1 = fig.add_subplot(gs[0, :2])
    app_df['Applied_Month'] = app_df['Applied Date'].dt.month
    monthly_apps = app_df.groupby('Applied_Month')['ID'].count()
    monthly_apps.plot(kind='bar', ax=ax1, color=COLORS['primary'])
    ax1.set_title('Application Volume by Month', fontweight='bold')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Number of Applications')
    ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
    
    # 2. Enrollment Rate by College
    ax2 = fig.add_subplot(gs[0, 2])
    college_enrollment_rate = (app_df.groupby('COLLEGE_DESCR')['Enrolled'].sum() / 
                               app_df.groupby('COLLEGE_DESCR')['ID'].count() * 100)
    college_enrollment_rate = college_enrollment_rate.sort_values(ascending=False).head(8)
    college_enrollment_rate.plot(kind='barh', ax=ax2, color=COLORS['accent'])
    ax2.set_title('Enrollment Rate by College (%)', fontweight='bold')
    ax2.set_xlabel('Enrollment Rate (%)')
    ax2.set_ylabel('')  # hide COLLEGE_DESCR label that can overlap central plot
    
    # 3. Test Score Distribution
    ax3 = fig.add_subplot(gs[1, 0])
    enrolled = app_df[app_df['Enrolled'] == True]
    act_scores = enrolled['ACT_SCORE'].dropna()
    ax3.hist(act_scores, bins=20, color=COLORS['primary'], edgecolor='black', alpha=0.7)
    ax3.set_title('ACT Score Distribution (Enrolled)', fontweight='bold')
    ax3.set_xlabel('ACT Score')
    ax3.set_ylabel('Frequency')
    ax3.axvline(act_scores.mean(), color=COLORS['highlight'], linestyle='--', 
                linewidth=2, label=f'Mean: {act_scores.mean():.1f}')
    ax3.legend()
    
    # 4. GPA Distribution
    ax4 = fig.add_subplot(gs[1, 1])
    gpa_scores = enrolled['GPA'].dropna()
    ax4.hist(gpa_scores, bins=30, color=COLORS['secondary'], edgecolor='black', alpha=0.7)
    ax4.set_title('GPA Distribution (Enrolled)', fontweight='bold')
    ax4.set_xlabel('GPA')
    ax4.set_ylabel('Frequency')
    ax4.axvline(gpa_scores.mean(), color=COLORS['highlight'], linestyle='--', 
                linewidth=2, label=f'Mean: {gpa_scores.mean():.2f}')
    ax4.legend()
    
    # 5. First-Generation vs Non-First-Generation Enrollment
    ax5 = fig.add_subplot(gs[1, 2])
    first_gen_enroll = enrolled.groupby('First Generation')['Enrolled'].count()
    first_gen_enroll.plot(kind='bar', ax=ax5, color=[COLORS['primary'], COLORS['secondary']])
    ax5.set_title('Enrollment by First-Generation Status', fontweight='bold')
    ax5.set_xlabel('First Generation')
    ax5.set_ylabel('Number Enrolled')
    ax5.set_xticklabels(['No', 'Yes'], rotation=0)
    
    # 6. Applications by Year
    ax6 = fig.add_subplot(gs[2, 0])
    apps_by_year = app_df.groupby('Year')['ID'].count()
    apps_by_year.plot(kind='bar', ax=ax6, color=COLORS['neutral'])
    ax6.set_title('Total Applications by Year', fontweight='bold')
    ax6.set_xlabel('Academic Year')
    ax6.set_ylabel('Number of Applications')
    ax6.tick_params(axis='x', rotation=45)
    
    # 7. Pell Eligibility Distribution
    ax7 = fig.add_subplot(gs[2, 1])
    pell_dist = enrolled['Pell_Eligibility'].value_counts()
    if pell_dist.empty:
        # Handle edge case where there is no Pell data after filtering
        ax7.text(0.5, 0.5, 'No Pell eligibility data available',
                 ha='center', va='center', fontsize=10)
        ax7.axis('off')
    else:
        # Map raw values (e.g., 'Y', missing/other) to readable labels and
        # ensure label list length matches the data length
        label_map = {
            'Y': 'Eligible',
            'N': 'Not Eligible',
            '': 'Not Eligible'
        }
        labels = [label_map.get(val, str(val)) for val in pell_dist.index]
        colors = [COLORS['primary'], COLORS['accent']]
        ax7.pie(
            pell_dist.values,
            labels=labels,
            autopct='%1.1f%%',
            colors=colors[:len(pell_dist)],
            startangle=90
        )
        ax7.set_title('Pell Eligibility (Enrolled Students)', fontweight='bold')
    
    # 8. Days to Confirmation Distribution
    ax8 = fig.add_subplot(gs[2, 2])
    enrolled['Days_to_Confirmation'] = (enrolled['Confirmed Date'] - 
                                       enrolled['Applied Date']).dt.days
    days_to_confirm = enrolled['Days_to_Confirmation'].dropna()
    ax8.hist(days_to_confirm, bins=30, color=COLORS['secondary'], edgecolor='black', alpha=0.7)
    ax8.set_title('Days from Application to Confirmation', fontweight='bold')
    ax8.set_xlabel('Days')
    ax8.set_ylabel('Frequency')
    ax8.axvline(days_to_confirm.mean(), color=COLORS['highlight'], linestyle='--', 
                linewidth=2, label=f'Mean: {days_to_confirm.mean():.0f} days')
    ax8.legend()

    fig.tight_layout(rect=[0.03, 0.05, 0.97, 0.90])
    plt.savefig('Admissions_Dashboard.png', dpi=300, bbox_inches='tight')
    print("Admissions Dashboard saved as 'Admissions_Dashboard.png'")
    plt.close()


def create_college_dean_dashboard():
    """
    Create dashboard focused on college-specific metrics.
    Suitable for College Deans.
    """
    app_df, enroll_df = load_processed_data()
    
    # Get top colleges
    top_colleges = enroll_df['COLLEGE_DESCR'].value_counts().head(5).index
    
    fig, axes = plt.subplots(2, 3, figsize=(20, 10))
    fig.suptitle(
        'College Deans Dashboard\nCollege Performance Metrics',
        fontsize=18,
        fontweight='bold',
        y=0.98,
    )
    
    # 1. Enrollment by College Over Time
    ax1 = axes[0, 0]
    for college in top_colleges[:5]:
        college_enroll = enroll_df[enroll_df['COLLEGE_DESCR'] == college]
        enroll_by_year = college_enroll.groupby('YEAR')['ID'].count()
        ax1.plot(enroll_by_year.index, enroll_by_year.values, marker='o', label=college, linewidth=2)
    ax1.set_title('Enrollment Trends by College', fontweight='bold')
    ax1.set_xlabel('Academic Year')
    ax1.set_ylabel('Number of Students')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # 2. Average First-Term GPA by College
    ax2 = axes[0, 1]
    gpa_by_college = enroll_df.groupby('COLLEGE_DESCR')['FirstTerm_GPA'].mean().sort_values(ascending=False).head(10)
    gpa_by_college.plot(kind='barh', ax=ax2, color=COLORS['primary'])
    ax2.set_title('Average First-Term GPA by College', fontweight='bold')
    ax2.set_xlabel('Average GPA')
    ax2.set_ylabel('')  # remove default COLLEGE_DESCR label to prevent overlap
    
    # 3. Retention Rate by College
    ax3 = axes[0, 2]
    retention_by_college = enroll_df.groupby('COLLEGE_DESCR')['OneYear_Retention'].mean().sort_values(ascending=False).head(10) * 100
    retention_by_college.plot(kind='barh', ax=ax3, color=COLORS['accent'])
    ax3.set_title('1-Year Retention Rate by College (%)', fontweight='bold')
    ax3.set_xlabel('Retention Rate (%)')
    
    # 4. Diversity Metrics - Gender by College
    ax4 = axes[1, 0]
    enrolled = app_df[app_df['Enrolled'] == True]
    gender_by_college = enrolled.groupby(['COLLEGE_DESCR', 'Gender']).size().unstack(fill_value=0)
    gender_by_college = gender_by_college.div(gender_by_college.sum(axis=1), axis=0) * 100
    gender_by_college = gender_by_college.sort_values('Female', ascending=False).head(10)
    gender_by_college.plot(kind='barh', stacked=True, ax=ax4, 
                          color=[COLORS['primary'], COLORS['secondary']])
    ax4.set_title('Gender Distribution by College (%)', fontweight='bold')
    ax4.set_xlabel('Percentage')
    ax4.legend(title='Gender', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 5. Average Credit Hours by College
    ax5 = axes[1, 1]
    credit_hours_by_college = enroll_df.groupby('COLLEGE_DESCR')['FirstTerm_CreditHours'].mean().sort_values(ascending=False).head(10)
    credit_hours_by_college.plot(kind='barh', ax=ax5, color=COLORS['neutral'])
    ax5.set_title('Average First-Term Credit Hours by College', fontweight='bold')
    ax5.set_xlabel('Average Credit Hours')
    ax5.set_ylabel('')  # remove default COLLEGE_DESCR label to prevent overlap
    
    # 6. Top Departments by Enrollment
    ax6 = axes[1, 2]
    top_depts = enroll_df['DEPARTMENT_DESCR'].value_counts().head(10)
    top_depts.plot(kind='barh', ax=ax6, color=COLORS['secondary'])
    ax6.set_title('Top 10 Departments by Enrollment', fontweight='bold')
    ax6.set_xlabel('Number of Students')

    fig.tight_layout(rect=[0.03, 0.05, 0.97, 0.90])
    plt.savefig('College_Deans_Dashboard.png', dpi=300, bbox_inches='tight')
    print("College Deans Dashboard saved as 'College_Deans_Dashboard.png'")
    plt.close()


def create_diversity_dashboard():
    """
    Create dashboard focused on diversity and inclusion metrics.
    """
    app_df, enroll_df = load_processed_data()
    enrolled = app_df[app_df['Enrolled'] == True]
    
    fig = plt.figure(figsize=(18, 10))
    gs = GridSpec(3, 3, figure=fig)
    
    fig.suptitle(
        'Diversity and Inclusion Dashboard\nStudent Demographics Analysis',
        fontsize=18,
        fontweight='bold',
        y=0.98,
    )
    
    # 1. Ethnicity Distribution Over Time
    ax1 = fig.add_subplot(gs[0, :2])
    ethnicity_by_year = enrolled.groupby(['Year', 'Ethnicity']).size().unstack(fill_value=0)
    ethnicity_by_year.plot(kind='bar', stacked=True, ax=ax1, 
                          colormap='Set3', width=0.8)
    ax1.set_title('Ethnicity Distribution by Year', fontweight='bold')
    ax1.set_xlabel('Academic Year')
    ax1.set_ylabel('Number of Students')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. First-Generation Percentage by College
    ax2 = fig.add_subplot(gs[0, 2])
    first_gen_by_college = enrolled.groupby('COLLEGE_DESCR')['First Generation'].mean().sort_values(ascending=False).head(8) * 100
    first_gen_by_college.plot(kind='barh', ax=ax2, color=COLORS['accent'])
    ax2.set_title('First-Generation % by College', fontweight='bold')
    ax2.set_xlabel('Percentage (%)')
    ax2.set_ylabel('')  # hide COLLEGE_DESCR label to avoid overlap
    # Reduce y-label font size and nudge plot slightly right to avoid overlap with center panel
    ax2.tick_params(axis='y', labelsize=8)
    pos2 = ax2.get_position()
    ax2.set_position([pos2.x0 + 0.03, pos2.y0, pos2.width - 0.03, pos2.height])
    
    # 3. Pell Eligibility by College
    ax3 = fig.add_subplot(gs[1, 0])
    pell_by_college = (enrolled.groupby('COLLEGE_DESCR')['Pell_Eligibility']
                      .apply(lambda x: (x == 'Y').sum() / len(x) * 100)
                      .sort_values(ascending=False).head(8))
    pell_by_college.plot(kind='barh', ax=ax3, color=COLORS['primary'])
    ax3.set_title('Pell Eligibility % by College', fontweight='bold')
    ax3.set_xlabel('Percentage (%)')
    ax3.set_ylabel('')  # hide COLLEGE_DESCR label
    ax3.tick_params(axis='y', labelsize=8)
    
    # 4. URM Representation by College
    ax4 = fig.add_subplot(gs[1, 1])
    urm_categories = ['Black/African American', 'Hispanic/Latino', 
                      'American Indian/Alaska Native', 'Native Hawaiian/Pacific Islander']
    urm_by_college = (enrolled.groupby('COLLEGE_DESCR')['Ethnicity']
                     .apply(lambda x: x.isin(urm_categories).sum() / len(x) * 100)
                     .sort_values(ascending=False).head(8))
    urm_by_college.plot(kind='barh', ax=ax4, color=COLORS['secondary'])
    ax4.set_title('URM Representation % by College', fontweight='bold')
    ax4.set_xlabel('Percentage (%)')
    ax4.set_ylabel('')  # hide COLLEGE_DESCR label
    ax4.tick_params(axis='y', labelsize=8)
    pos4 = ax4.get_position()
    ax4.set_position([pos4.x0 + 0.01, pos4.y0, pos4.width, pos4.height])
    
    # 5. Gender Distribution by College
    ax5 = fig.add_subplot(gs[1, 2])
    gender_by_college = enrolled.groupby(['COLLEGE_DESCR', 'Gender']).size().unstack(fill_value=0)
    gender_by_college = gender_by_college.div(gender_by_college.sum(axis=1), axis=0) * 100
    gender_by_college = gender_by_college.sort_values('Female', ascending=False).head(8)
    gender_by_college.plot(kind='barh', stacked=True, ax=ax5, 
                          color=[COLORS['primary'], COLORS['secondary']])
    ax5.set_title('Gender Distribution by College (%)', fontweight='bold')
    ax5.set_xlabel('Percentage')
    ax5.legend(title='Gender', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax5.tick_params(axis='y', labelsize=8)
    
    # 6. Diversity Index Over Time
    ax6 = fig.add_subplot(gs[2, :])
    diversity_index = []
    for year in sorted(enrolled['Year'].unique()):
        year_data = enrolled[enrolled['Year'] == year]
        ethnicity_counts = year_data['Ethnicity'].value_counts()
        # Calculate Simpson's Diversity Index
        total = ethnicity_counts.sum()
        diversity = 1 - sum((ethnicity_counts / total) ** 2)
        diversity_index.append({'Year': year, 'Diversity_Index': diversity})
    
    diversity_df = pd.DataFrame(diversity_index)
    diversity_df.plot(x='Year', y='Diversity_Index', kind='line', 
                     marker='o', ax=ax6, color=COLORS['highlight'], linewidth=2)
    ax6.set_title('Diversity Index Trend (Simpson\'s Index)', fontweight='bold')
    ax6.set_xlabel('Academic Year')
    ax6.set_ylabel('Diversity Index (0-1)')
    ax6.grid(True, alpha=0.3)
    ax6.set_ylim(0, 1)

    fig.tight_layout(rect=[0.03, 0.05, 0.97, 0.90])
    plt.savefig('Diversity_Dashboard.png', dpi=300, bbox_inches='tight')
    print("Diversity Dashboard saved as 'Diversity_Dashboard.png'")
    plt.close()


def main():
    """Generate all dashboards."""
    print("="*60)
    print("GENERATING DASHBOARDS")
    print("="*60)
    
    create_executive_dashboard()
    create_admissions_dashboard()
    create_college_dean_dashboard()
    create_diversity_dashboard()
    
    print("\n" + "="*60)
    print("All dashboards generated successfully!")
    print("="*60)


if __name__ == "__main__":
    main()

