# Analysis Methodology
## University of *** Student Data Analysis

**Date:** December 2025

---

## 1. Data Sources and Description

### 1.1 Datasets Used

1. **Applications Data** (`Applications _Data.csv`)
   - Contains student application information
   - ~93,600 records
   - Fields: ID, application dates, demographics, academic metrics, financial aid

2. **Enrollment Data** (`Enrollment_Data.csv`)
   - Contains enrollment and retention information
   - ~18,000 records
   - Fields: ID, year, department, college, academic performance, retention

3. **SAT to ACT Conversion Chart** (`SAT to ACT Conversion Chart.csv`)
   - Reference for standardizing test scores
   - Used to create unified test score metric

4. **Dataset Definitions** (`Dataset Definitions.csv`)
   - Data dictionary
   - Field descriptions and definitions

### 1.2 Data Characteristics

- **Time Period**: Academic years 2016-2021 (5 years)
- **Data Type**: Synthetic dataset designed to resemble real UA data
- **Scope**: All applications and enrollments during the period
- **Completeness**: Some fields contain missing values

---

## 2. Data Preprocessing

### 2.1 Data Loading

- CSV files loaded using pandas `read_csv()`
- Encoding handled automatically
- Date parsing with error handling

### 2.2 Data Cleaning

#### Applications Data:
1. **Date Fields**
   - `Applied Date`: Converted to datetime format
   - `Confirmed Date`: Converted to datetime format
   - Missing dates handled with `errors='coerce'`

2. **Derived Fields**
   - `Application_Year`: Extracted from application date
   - `Days_to_Confirmation`: Calculated difference between application and confirmation dates
   - `Enrolled`: Binary indicator (True if Confirmed Date exists)

3. **Numeric Fields**
   - `GPA`: Converted to numeric, missing values preserved
   - `ACT_SCORE`: Converted to numeric
   - `SAT_SCORE`: Converted to numeric
   - `Scholarship_Amount`: Converted to numeric, 0 for missing

4. **Test Score Standardization**
   - Created `Standardized_Test_Score` field
   - ACT scores used directly
   - SAT scores converted to ACT equivalent using conversion chart
   - Missing values preserved

5. **Text Fields**
   - `COLLEGE_DESCR`: Stripped whitespace
   - `Gender`, `Ethnicity`: Standardized formatting

#### Enrollment Data:
1. **Numeric Fields**
   - `FirstTerm_CreditHours`: Converted to numeric
   - `FirstTerm_GPA`: Converted to numeric

2. **Retention Indicators**
   - `OneYear_Retention`: Converted to binary (1/0)
   - `TwoYear_Retention`: Converted to binary (1/0)
   - Handled various formats (1, '1', blank, etc.)

3. **Text Fields**
   - `COLLEGE_DESCR`: Stripped whitespace
   - `DEPARTMENT_DESCR`: Stripped whitespace

### 2.3 Data Validation

- Checked for duplicate IDs
- Validated date ranges
- Verified numeric ranges (GPA 0-4, ACT 1-36, etc.)
- Identified and documented missing data patterns

---

## 3. Analysis Methods

### 3.1 Descriptive Statistics

#### Central Tendency Measures:
- **Mean**: Used for continuous variables (GPA, test scores, credit hours)
- **Median**: Used for skewed distributions
- **Mode**: Used for categorical variables

#### Dispersion Measures:
- Standard deviation for continuous variables
- Counts and percentages for categorical variables

### 3.2 Demographic Analysis

#### Methods:
1. **Frequency Analysis**
   - Counts and percentages by category
   - Cross-tabulations for multi-dimensional analysis

2. **Diversity Metrics**
   - **Simpson's Diversity Index**: Calculated as 1 - Σ(p_i²)
     - Where p_i is the proportion of each category
     - Range: 0 (no diversity) to 1 (maximum diversity)

3. **URM Calculation**
   - Underrepresented Minority categories:
     - Black/African American
     - Hispanic/Latino
     - American Indian/Alaska Native
     - Native Hawaiian/Pacific Islander

### 3.3 Trend Analysis

#### Time Series Analysis:
1. **Year-over-Year Comparisons**
   - Absolute changes
   - Percentage changes
   - Growth rates

2. **Seasonal Patterns**
   - Monthly application patterns
   - Application timing analysis

3. **Visualization**
   - Line charts for trends
   - Bar charts for comparisons
   - Stacked charts for composition changes

### 3.4 Retention Analysis

#### Methods:
1. **Retention Rate Calculation**
   - One-Year: (Retained Year 1 / Total Enrolled) × 100
   - Two-Year: (Retained Year 2 / Total Enrolled) × 100

2. **Stratified Analysis**
   - By college
   - By student characteristics
   - By academic performance

3. **Predictor Analysis**
   - Correlation between first-term GPA and retention
   - Credit hours and retention
   - Demographics and retention

### 3.5 Academic Quality Analysis

#### Methods:
1. **Performance Metrics**
   - Average GPA by college/department
   - Test score distributions
   - Academic performance trends

2. **Scholarship Analysis**
   - Distribution of scholarship amounts
   - Scholarship recipients by characteristics
   - Correlation with academic metrics

3. **Predictive Indicators**
   - High school GPA as predictor
   - Test scores as predictor
   - Combined metrics

### 3.6 Comparative Analysis

#### Methods:
1. **College Comparisons**
   - Side-by-side metrics
   - Ranking and percentiles
   - Best practice identification

2. **Cohort Comparisons**
   - First-generation vs. non-first-generation
   - Pell-eligible vs. non-Pell-eligible
   - Full-time vs. part-time

---

## 4. Statistical Techniques

### 4.1 Aggregation Methods

- **Grouping**: GroupBy operations for categorical analysis
- **Pivoting**: Cross-tabulation for multi-dimensional views
- **Windowing**: Year-over-year calculations using window functions

### 4.2 Missing Data Handling

- **Missing Completely at Random (MCAR)**: Assumed for most fields
- **Preservation**: Missing values preserved where appropriate
- **Exclusion**: Missing values excluded from specific calculations
- **Documentation**: Missing data patterns documented

### 4.3 Data Transformation

1. **Binning**
   - GPA ranges for analysis
   - Scholarship amount ranges
   - Test score ranges

2. **Standardization**
   - Test score conversion (SAT to ACT)
   - Date standardization
   - Text field normalization

---

## 5. Visualization Methods

### 5.1 Dashboard Design Principles

1. **Stakeholder-Specific**
   - Executive: High-level metrics
   - Admissions: Application-focused
   - College Deans: College-specific
   - Diversity: Inclusion metrics

2. **Visual Hierarchy**
   - Most important metrics prominently displayed
   - Supporting details in secondary positions
   - Consistent color scheme

3. **Chart Selection**
   - **Line Charts**: Trends over time
   - **Bar Charts**: Comparisons
   - **Pie Charts**: Composition (limited use)
   - **Histograms**: Distributions
   - **Stacked Charts**: Multi-category composition

### 5.2 Color Scheme

- Consistent color palette across dashboards
- Color-blind friendly choices
- Meaningful color associations

### 5.3 Dashboard Layout

- Grid-based layouts for organization
- Multiple related charts per dashboard
- Clear titles and labels
- Legends where appropriate

---

## 6. Quality Assurance

### 6.1 Data Quality Checks

1. **Completeness**
   - Record counts verified
   - Expected vs. actual record counts
   - Missing data patterns identified

2. **Accuracy**
   - Date ranges validated
   - Numeric ranges checked
   - Logical consistency verified

3. **Consistency**
   - College names standardized
   - Department names standardized
   - Format consistency

### 6.2 Analysis Validation

1. **Cross-Validation**
   - Multiple methods for same metric
   - Comparison with expected values
   - Sanity checks

2. **Reproducibility**
   - Code documented
   - Steps clearly defined
   - Random seed set where applicable

3. **Sensitivity Analysis**
   - Impact of missing data assessed
   - Outlier handling reviewed
   - Assumptions documented

---

## 7. Limitations and Assumptions

### 7.1 Data Limitations

1. **Synthetic Data**
   - Dataset is synthetic, not real student data
   - May not capture all real-world complexities
   - Patterns may differ from actual data

2. **Missing Data**
   - Some fields have missing values
   - Missing data patterns may affect analysis
   - Assumptions about missing data documented

3. **Time Period**
   - Limited to 5 academic years
   - May not capture longer-term trends
   - External factors not included

### 7.2 Methodological Assumptions

1. **Retention Calculation**
   - Assumes retention data is accurate
   - May not capture all retention scenarios

2. **Test Score Conversion**
   - SAT to ACT conversion is approximate
   - Individual variations not captured

3. **Enrollment Definition**
   - Enrollment defined as having Confirmed Date
   - May not capture all enrollment scenarios

### 7.3 Analytical Assumptions

1. **Causality**
   - Correlations identified, not causations
   - Multiple factors may influence outcomes

2. **Generalization**
   - Findings specific to this dataset
   - May not generalize to other contexts

---

## 8. Reproducibility

### 8.1 Code Organization

- Modular functions
- Clear variable names
- Comprehensive comments
- Documentation strings

### 8.2 Version Control

- Code versioning recommended
- Data versioning documented
- Analysis date recorded

### 8.3 Dependencies

- Python version: 3.7+
- Package versions documented
- Environment setup instructions provided

---

## 9. Ethical Considerations

### 9.1 Data Privacy

- Synthetic dataset used (not real student data)
- No personally identifiable information in outputs
- Data sharing restrictions followed

### 9.2 Analysis Ethics

- Objective analysis approach
- No bias in interpretation
- Transparent methodology
- Honest reporting of limitations

---

## 10. Future Enhancements

### 10.1 Additional Analyses

- Longitudinal student tracking
- Program-level detailed analysis
- Financial aid impact analysis
- Post-graduation outcomes

### 10.2 Methodological Improvements

- Advanced statistical modeling
- Predictive analytics
- Machine learning applications
- Real-time dashboard updates

---

## References

- University of *** Dataset Definitions
- SAT to ACT Conversion Chart
- Standard statistical methods for educational data analysis
- Best practices for higher education analytics

---

**End of Methodology Documentation**

