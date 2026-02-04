"""
University of Akron Student Data Analysis
==========================================
This script performs comprehensive analysis of student applications and enrollment data
for the University of Akron across 5 academic years (2016-2021).

Date: December 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================
# DATA LOADING AND PREPROCESSING
# ============================================================================

def load_data():
    """
    Load all required datasets for analysis.
    
    Returns:
        tuple: (applications_df, enrollment_df, sat_act_df)
    """
    print("Loading datasets...")
    
    # Load Applications data
    applications_df = pd.read_csv('Applications _Data.csv')
    print(f"Applications data loaded: {len(applications_df):,} records")
    
    # Load Enrollment data
    enrollment_df = pd.read_csv('Enrollment_Data.csv')
    print(f"Enrollment data loaded: {len(enrollment_df):,} records")
    
    # Load SAT to ACT conversion chart
    sat_act_df = pd.read_csv('SAT to ACT Conversion Chart.csv')
    print(f"SAT-ACT conversion chart loaded: {len(sat_act_df):,} records")
    
    return applications_df, enrollment_df, sat_act_df


def preprocess_applications(df):
    """
    Clean and preprocess applications data.
    
    Args:
        df: Applications dataframe
        
    Returns:
        Preprocessed dataframe
    """
    print("\nPreprocessing applications data...")
    
    # Convert date columns
    df['Applied Date'] = pd.to_datetime(df['Applied Date'], errors='coerce')
    df['Confirmed Date'] = pd.to_datetime(df['Confirmed Date'], errors='coerce')
    
    # Create derived fields
    df['Application_Year'] = df['Applied Date'].dt.year
    df['Days_to_Confirmation'] = (df['Confirmed Date'] - df['Applied Date']).dt.days
    
    # Convert test scores to numeric
    df['ACT_SCORE'] = pd.to_numeric(df['ACT_SCORE'], errors='coerce')
    df['SAT_SCORE'] = pd.to_numeric(df['SAT_SCORE'], errors='coerce')
    
    # Convert GPA to numeric
    df['GPA'] = pd.to_numeric(df['GPA'], errors='coerce')
    
    # Convert scholarship amount to numeric
    df['Scholarship_Amount'] = pd.to_numeric(df['Scholarship_Amount'], errors='coerce')
    
    # Create standardized test score (ACT equivalent)
    df['Standardized_Test_Score'] = df['ACT_SCORE'].fillna(
        df['SAT_SCORE'].apply(lambda x: convert_sat_to_act(x) if pd.notna(x) else np.nan)
    )
    
    # Create enrollment indicator
    df['Enrolled'] = df['Confirmed Date'].notna()
    
    # Clean college names
    df['COLLEGE_DESCR'] = df['COLLEGE_DESCR'].str.strip()
    
    print(f"Preprocessing complete. Records: {len(df):,}")
    return df


def convert_sat_to_act(sat_score):
    """
    Convert SAT score to ACT equivalent using conversion chart.
    
    Args:
        sat_score: SAT composite score
        
    Returns:
        ACT equivalent score
    """
    # Simplified conversion (can be enhanced with lookup table)
    if pd.isna(sat_score):
        return np.nan
    
    # Approximate conversion formula
    if sat_score >= 1570:
        return 36
    elif sat_score >= 1530:
        return 35
    elif sat_score >= 1490:
        return 34
    elif sat_score >= 1450:
        return 33
    elif sat_score >= 1420:
        return 32
    elif sat_score >= 1390:
        return 31
    elif sat_score >= 1360:
        return 30
    elif sat_score >= 1330:
        return 29
    elif sat_score >= 1300:
        return 28
    elif sat_score >= 1260:
        return 27
    elif sat_score >= 1230:
        return 26
    elif sat_score >= 1200:
        return 25
    elif sat_score >= 1160:
        return 24
    elif sat_score >= 1130:
        return 23
    elif sat_score >= 1100:
        return 22
    elif sat_score >= 1060:
        return 21
    elif sat_score >= 1030:
        return 20
    elif sat_score >= 990:
        return 19
    elif sat_score >= 960:
        return 18
    elif sat_score >= 920:
        return 17
    elif sat_score >= 880:
        return 16
    else:
        return 15


def preprocess_enrollment(df):
    """
    Clean and preprocess enrollment data.
    
    Args:
        df: Enrollment dataframe
        
    Returns:
        Preprocessed dataframe
    """
    print("\nPreprocessing enrollment data...")
    
    # Convert numeric columns
    df['FirstTerm_CreditHours'] = pd.to_numeric(df['FirstTerm_CreditHours'], errors='coerce')
    df['FirstTerm_GPA'] = pd.to_numeric(df['FirstTerm_GPA'], errors='coerce')
    
    # Convert retention indicators
    df['OneYear_Retention'] = df['OneYear retention'].apply(
        lambda x: 1 if pd.notna(x) and str(x).strip() == '1' else 0
    )
    df['TwoYear_Retention'] = df['TwoYear retention'].apply(
        lambda x: 1 if pd.notna(x) and str(x).strip() == '1' else 0
    )
    
    # Clean college and department names
    df['COLLEGE_DESCR'] = df['COLLEGE_DESCR'].str.strip()
    df['DEPARTMENT_DESCR'] = df['DEPARTMENT_DESCR'].str.strip()
    
    print(f"Preprocessing complete. Records: {len(df):,}")
    return df


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_demographics(app_df):
    """
    Analyze student demographics including gender, ethnicity, and first-generation status.
    
    Args:
        app_df: Applications dataframe
        
    Returns:
        dict: Dictionary containing demographic statistics
    """
    print("\n" + "="*60)
    print("DEMOGRAPHIC ANALYSIS")
    print("="*60)
    
    results = {}
    
    # Gender distribution
    gender_dist = app_df['Gender'].value_counts(normalize=True) * 100
    results['gender'] = gender_dist.to_dict()
    print(f"\nGender Distribution:")
    for gender, pct in gender_dist.items():
        print(f"  {gender}: {pct:.2f}%")
    
    # Ethnicity distribution
    ethnicity_dist = app_df['Ethnicity'].value_counts(normalize=True) * 100
    results['ethnicity'] = ethnicity_dist.to_dict()
    print(f"\nTop 5 Ethnicity Groups:")
    for eth, pct in ethnicity_dist.head(5).items():
        print(f"  {eth}: {pct:.2f}%")
    
    # First-generation students
    first_gen_pct = app_df['First Generation'].mean() * 100
    results['first_gen_pct'] = first_gen_pct
    print(f"\nFirst-Generation Students: {first_gen_pct:.2f}%")
    
    # Pell eligibility
    pell_pct = (app_df['Pell_Eligibility'] == 'Y').sum() / len(app_df) * 100
    results['pell_pct'] = pell_pct
    print(f"Pell Eligible Students: {pell_pct:.2f}%")
    
    return results


def analyze_college_diversity(app_df):
    """
    Analyze diversity differences among colleges.
    
    Args:
        app_df: Applications dataframe
        
    Returns:
        DataFrame: Diversity metrics by college
    """
    print("\n" + "="*60)
    print("COLLEGE DIVERSITY ANALYSIS")
    print("="*60)
    
    # Filter out invalid colleges
    valid_colleges = app_df[app_df['COLLEGE_DESCR'].notna() & 
                           (app_df['COLLEGE_DESCR'] != '')]
    
    diversity_metrics = []
    
    for college in valid_colleges['COLLEGE_DESCR'].unique():
        college_data = valid_colleges[valid_colleges['COLLEGE_DESCR'] == college]
        
        metrics = {
            'College': college,
            'Total_Applications': len(college_data),
            'Female_Pct': (college_data['Gender'] == 'Female').sum() / len(college_data) * 100,
            'FirstGen_Pct': college_data['First Generation'].mean() * 100,
            'Pell_Pct': (college_data['Pell_Eligibility'] == 'Y').sum() / len(college_data) * 100,
            'White_Pct': (college_data['Ethnicity'] == 'White').sum() / len(college_data) * 100,
            'URM_Pct': college_data['Ethnicity'].isin([
                'Black/African American', 'Hispanic/Latino', 
                'American Indian/Alaska Native', 'Native Hawaiian/Pacific Islander'
            ]).sum() / len(college_data) * 100
        }
        diversity_metrics.append(metrics)
    
    diversity_df = pd.DataFrame(diversity_metrics)
    diversity_df = diversity_df.sort_values('Total_Applications', ascending=False)
    
    print("\nDiversity Metrics by College:")
    print(diversity_df.to_string(index=False))
    
    return diversity_df


def analyze_top_programs(app_df, enroll_df):
    """
    Identify top programs by application volume and enrollment.
    
    Args:
        app_df: Applications dataframe
        enroll_df: Enrollment dataframe
        
    Returns:
        tuple: (top_applications, top_enrollments)
    """
    print("\n" + "="*60)
    print("TOP PROGRAMS ANALYSIS")
    print("="*60)
    
    # Top colleges by applications
    top_app_colleges = app_df['COLLEGE_DESCR'].value_counts().head(10)
    print("\nTop 10 Colleges by Application Volume:")
    for college, count in top_app_colleges.items():
        print(f"  {college}: {count:,} applications")
    
    # Top departments by enrollment
    top_dept = enroll_df['DEPARTMENT_DESCR'].value_counts().head(10)
    print("\nTop 10 Departments by Enrollment:")
    for dept, count in top_dept.items():
        print(f"  {dept}: {count:,} enrollments")
    
    # Top colleges by enrollment
    top_enroll_colleges = enroll_df['COLLEGE_DESCR'].value_counts().head(10)
    print("\nTop 10 Colleges by Enrollment:")
    for college, count in top_enroll_colleges.items():
        print(f"  {college}: {count:,} enrollments")
    
    return top_app_colleges, top_enroll_colleges


def analyze_academic_quality(app_df):
    """
    Analyze academic quality indicators (GPA, test scores, scholarships).
    
    Args:
        app_df: Applications dataframe
        
    Returns:
        dict: Academic quality metrics
    """
    print("\n" + "="*60)
    print("ACADEMIC QUALITY INDICATORS")
    print("="*60)
    
    # Filter enrolled students only
    enrolled = app_df[app_df['Enrolled'] == True]
    
    metrics = {
        'avg_gpa': enrolled['GPA'].mean(),
        'median_gpa': enrolled['GPA'].median(),
        'avg_act': enrolled['Standardized_Test_Score'].mean(),
        'median_act': enrolled['Standardized_Test_Score'].median(),
        'avg_scholarship': enrolled['Scholarship_Amount'].mean(),
        'scholarship_recipients_pct': (enrolled['Scholarship_Amount'] > 0).sum() / len(enrolled) * 100
    }
    
    print(f"\nAverage GPA (Enrolled Students): {metrics['avg_gpa']:.3f}")
    print(f"Median GPA (Enrolled Students): {metrics['median_gpa']:.3f}")
    print(f"Average ACT Score (Enrolled Students): {metrics['avg_act']:.2f}")
    print(f"Median ACT Score (Enrolled Students): {metrics['median_act']:.2f}")
    print(f"Average Scholarship Amount: ${metrics['avg_scholarship']:,.2f}")
    print(f"Scholarship Recipients: {metrics['scholarship_recipients_pct']:.2f}%")
    
    return metrics


def analyze_enrollment_trends(app_df, enroll_df):
    """
    Identify trends in enrollment data over time.
    
    Args:
        app_df: Applications dataframe
        enroll_df: Enrollment dataframe
        
    Returns:
        dict: Trend analysis results
    """
    print("\n" + "="*60)
    print("ENROLLMENT TRENDS ANALYSIS")
    print("="*60)
    
    # Applications by year
    app_by_year = app_df.groupby('Year').agg({
        'ID': 'count',
        'Enrolled': 'sum'
    }).rename(columns={'ID': 'Applications', 'Enrolled': 'Enrollments'})
    app_by_year['Enrollment_Rate'] = (app_by_year['Enrollments'] / app_by_year['Applications']) * 100
    
    print("\nApplications and Enrollments by Year:")
    print(app_by_year.to_string())
    
    # Enrollment by year
    enroll_by_year = enroll_df.groupby('YEAR').agg({
        'ID': 'count',
        'FirstTerm_GPA': 'mean',
        'FirstTerm_CreditHours': 'mean'
    }).rename(columns={'ID': 'Enrollments', 'FirstTerm_GPA': 'Avg_GPA', 
                       'FirstTerm_CreditHours': 'Avg_CreditHours'})
    
    print("\nEnrollment Metrics by Year:")
    print(enroll_by_year.to_string())
    
    # Retention rates
    retention_by_year = enroll_df.groupby('YEAR').agg({
        'OneYear_Retention': 'mean',
        'TwoYear_Retention': 'mean'
    }) * 100
    
    print("\nRetention Rates by Year:")
    print(retention_by_year.to_string())
    
    return {
        'applications_trend': app_by_year,
        'enrollment_trend': enroll_by_year,
        'retention_trend': retention_by_year
    }


def analyze_retention(enroll_df):
    """
    Analyze student retention rates by various dimensions.
    
    Args:
        enroll_df: Enrollment dataframe
        
    Returns:
        dict: Retention analysis results
    """
    print("\n" + "="*60)
    print("RETENTION ANALYSIS")
    print("="*60)
    
    results = {}
    
    # Overall retention
    overall_1yr = enroll_df['OneYear_Retention'].mean() * 100
    overall_2yr = enroll_df['TwoYear_Retention'].mean() * 100
    
    print(f"\nOverall 1-Year Retention Rate: {overall_1yr:.2f}%")
    print(f"Overall 2-Year Retention Rate: {overall_2yr:.2f}%")
    
    results['overall_1yr'] = overall_1yr
    results['overall_2yr'] = overall_2yr
    
    # Retention by college
    retention_by_college = enroll_df.groupby('COLLEGE_DESCR').agg({
        'OneYear_Retention': 'mean',
        'TwoYear_Retention': 'mean',
        'ID': 'count'
    }).rename(columns={'ID': 'Count'})
    retention_by_college['OneYear_Retention'] *= 100
    retention_by_college['TwoYear_Retention'] *= 100
    
    print("\nRetention Rates by College:")
    print(retention_by_college.sort_values('OneYear_Retention', ascending=False).to_string())
    
    results['by_college'] = retention_by_college
    
    # Retention by full-time/part-time
    retention_by_ftpt = enroll_df.groupby('FTPT').agg({
        'OneYear_Retention': 'mean',
        'TwoYear_Retention': 'mean'
    }) * 100
    
    print("\nRetention Rates by Full-Time/Part-Time Status:")
    print(retention_by_ftpt.to_string())
    
    results['by_ftpt'] = retention_by_ftpt
    
    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function that runs all analyses.
    """
    print("="*60)
    print("UNIVERSITY OF AKRON STUDENT DATA ANALYSIS")
    print("="*60)
    
    # Load data
    app_df, enroll_df, sat_act_df = load_data()
    
    # Preprocess data
    app_df = preprocess_applications(app_df)
    enroll_df = preprocess_enrollment(enroll_df)
    
    # Run analyses
    demo_results = analyze_demographics(app_df)
    diversity_df = analyze_college_diversity(app_df)
    top_programs = analyze_top_programs(app_df, enroll_df)
    quality_metrics = analyze_academic_quality(app_df)
    trends = analyze_enrollment_trends(app_df, enroll_df)
    retention_results = analyze_retention(enroll_df)
    
    # Save results
    print("\n" + "="*60)
    print("Saving analysis results...")
    diversity_df.to_csv('diversity_metrics_by_college.csv', index=False)
    trends['applications_trend'].to_csv('applications_trends.csv')
    trends['enrollment_trend'].to_csv('enrollment_trends.csv')
    trends['retention_trend'].to_csv('retention_trends.csv')
    retention_results['by_college'].to_csv('retention_by_college.csv')
    
    print("\nAnalysis complete! Results saved to CSV files.")
    print("="*60)


if __name__ == "__main__":
    main()

