# University of Akron Student Data Analysis Project

## Project Overview

This project provides comprehensive analysis of student applications, enrollments, demographics, and retention patterns at the University of Akron across 5 academic years (2016-2021). The analysis is designed to support decision-making for various university stakeholders including the Provost's Office, Admissions Office, College Deans, and faculty.

## Project Structure

```
Data Analysis Project/
│
├── Applications _Data.csv              # Student application data
├── Enrollment_Data.csv                 # Student enrollment and retention data
├── Dataset Definitions.csv             # Data dictionary
├── SAT to ACT Conversion Chart.csv     # Test score conversion reference
├── Technical Round-Instructions.csv     # Project requirements
│
├── data_analysis.py                    # Main analysis script
├── dashboard_visualizations.py         # Dashboard generation script
├── interactive_dashboards.py           # Interactive HTML Dashboard script
├── sql_queries.sql                     # SQL queries for data extraction
│
├── KEY_FINDINGS_AND_INSIGHTS.md        # Summary of key findings
├── README.md                           # This file
├── METHODOLOGY.md                      # Analysis methodology documentation
│
├── dashboard_portal.html               # Central Dashboard Portal to access Dashboards in Dashboards/
│ 
└── Dashboards/
│    ├── Executive_Dashboard.png
│    ├── Admissions_Dashboard.png
│    ├── College_Deans_Dashboard.png
│    ├── Diversity_Dashboard.png
│    ├── Admissions_Dashboard_Interactive.html
│    ├── Executive_Dashboard_Interactive.html
│    ├── College_Deans_Dashboard_Interactive.html
│    └── Diversity_Dashboard_Interactive.html
│
│
└── Generated Files/
    ├── diversity_metrics_by_college.csv
    ├── applications_trends.csv
    ├── enrollment_trends.csv
    ├── retention_trends.csv
    └── retention_by_college.csv
```

## Requirements

### Python Packages
```bash
pip install pandas numpy matplotlib seaborn
```

Required packages:
- `pandas` (>= 1.3.0) - Data manipulation and analysis
- `numpy` (>= 1.21.0) - Numerical computing
- `matplotlib` (>= 3.4.0) - Basic plotting
- `seaborn` (>= 0.11.0) - Statistical visualizations

### Data Files
All CSV data files must be in the same directory as the analysis scripts:
- `Applications _Data.csv`
- `Enrollment_Data.csv`
- `Dataset Definitions.csv`
- `SAT to ACT Conversion Chart.csv`

## Usage Instructions

### 1. Running the Main Analysis

Execute the main analysis script to perform comprehensive data analysis:

```bash
python data_analysis.py
```

This script will:
- Load and preprocess all data files
- Perform demographic analysis
- Analyze college diversity
- Identify top programs
- Calculate academic quality indicators
- Analyze enrollment trends
- Calculate retention rates
- Generate CSV output files with results

### 2. Generating Dashboards

Create visualization dashboards for different stakeholders:

```bash
python dashboard_visualizations.py
```

This script generates four dashboard images:
- **Executive_Dashboard.png** - High-level metrics for senior leadership
- **Admissions_Dashboard.png** - Admissions-focused metrics
- **College_Deans_Dashboard.png** - College-specific performance metrics
- **Diversity_Dashboard.png** - Diversity and inclusion metrics

### 3. Using SQL Queries

The `sql_queries.sql` file contains SQL queries that can be adapted for various database systems. These queries can be used to:
- Extract specific insights from the data
- Create custom reports
- Perform ad-hoc analysis
- Integrate with existing database systems

**Note**: The queries are written in standard SQL and may need minor adjustments for specific database systems (SQL Server, PostgreSQL, MySQL, etc.).

## Key Deliverables

### 1. Code Files
- **data_analysis.py**: Comprehensive Python analysis with detailed comments
- **dashboard_visualizations.py**: Visualization generation script
- **sql_queries.sql**: SQL queries for data extraction

### 2. Analysis Results
- **KEY_FINDINGS_AND_INSIGHTS.md**: Comprehensive summary of findings
- CSV files with detailed metrics and trends

### 3. Visualizations
- Four stakeholder-specific dashboards (PNG format, 300 DPI)
- Ready for presentation and reporting

### 4. Documentation
- **README.md**: This file - project overview and usage
- **METHODOLOGY.md**: Detailed methodology documentation
- **PRESENTATION_CONTENT.md**: Content for PowerPoint presentation

## Analysis Components

### 1. Demographic Analysis
- Gender distribution
- Ethnicity breakdown
- First-generation student statistics
- Pell eligibility analysis

### 2. College and Program Analysis
- Top colleges by application and enrollment volume
- Top departments by enrollment
- Enrollment trends by college

### 3. Academic Quality Indicators
- High school GPA analysis
- Standardized test scores (ACT/SAT)
- Scholarship distribution
- Academic performance by student characteristics

### 4. Diversity Analysis
- Diversity metrics by college
- URM (Underrepresented Minority) representation
- Gender distribution across colleges
- Socioeconomic diversity indicators

### 5. Enrollment Trends
- Year-over-year application and enrollment trends
- Seasonal application patterns
- Enrollment rate analysis
- College-specific trends

### 6. Retention Analysis
- Overall retention rates (1-year and 2-year)
- Retention by college
- Retention by student characteristics
- Full-time vs. part-time retention

### 7. First-Term Performance
- Average first-term GPA
- Credit hour patterns
- Predictors of academic success
- Early warning indicators

## Output Files

### CSV Output Files
- `diversity_metrics_by_college.csv` - Diversity statistics by college
- `applications_trends.csv` - Application trends by year
- `enrollment_trends.csv` - Enrollment metrics by year
- `retention_trends.csv` - Retention rates by year
- `retention_by_college.csv` - Retention statistics by college

### Dashboard Images
- `Executive_Dashboard.png` - Executive-level overview
- `Admissions_Dashboard.png` - Admissions metrics
- `College_Deans_Dashboard.png` - College performance
- `Diversity_Dashboard.png` - Diversity metrics

## Methodology

See `METHODOLOGY.md` for detailed information about:
- Data preprocessing steps
- Analysis techniques
- Statistical methods
- Assumptions and limitations

## Key Findings

See `KEY_FINDINGS_AND_INSIGHTS.md` for comprehensive summary of:
- Enrollment trends
- Demographic patterns
- Top programs
- Academic quality indicators
- Diversity metrics
- Retention patterns
- Strategic recommendations

## Presentation

See `PRESENTATION_CONTENT.md` for:
- PowerPoint slide content
- Presentation outline
- Key talking points
- Visual recommendations

## Data Dictionary

Refer to `Dataset Definitions.csv` for detailed field descriptions:
- Applications dataset fields
- Enrollment dataset fields
- Data types and formats
- Field definitions

## Best Practices

### Code Quality
- All code includes comprehensive comments
- Functions are well-documented
- Error handling included where appropriate
- Code follows Python best practices (PEP 8)

### Analysis Standards
- Transparent methodology
- Reproducible analysis
- Clear documentation
- Stakeholder-appropriate outputs

### Data Handling
- Missing data handled appropriately
- Data validation performed
- Date conversions standardized
- Numeric conversions with error handling

## Troubleshooting

### Common Issues

1. **File Not Found Error**
   - Ensure all CSV files are in the same directory as the scripts
   - Check file names match exactly (including spaces)

2. **Import Errors**
   - Install required packages: `pip install pandas numpy matplotlib seaborn`
   - Check Python version (3.7+ recommended)

3. **Memory Issues**
   - The dataset is large (~93K applications, ~18K enrollments)
   - Ensure sufficient system memory
   - Consider processing in chunks if needed

4. **Date Parsing Errors**
   - Some date formats may vary
   - The code handles common date formats automatically

## Contact and Support

For questions about this analysis:
- Review the documentation files
- Check the code comments for explanations
- Refer to the methodology document

## Project Timeline

- **Analysis Period**: Academic Years 2016-2021
- **Project Date**: December 2025
- **Submission Deadline**: December 23, 2025, 11:59 PM EST

## License and Usage

This analysis is for the University of Akron technical interview process. The synthetic dataset should not be shared externally per project instructions.

---

**Last Updated**: December 2025

