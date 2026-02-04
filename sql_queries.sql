-- ============================================================================
-- University of Akron Student Data Analysis - SQL Queries
-- ============================================================================
-- This file contains SQL queries for extracting insights from the student data
-- These queries can be adapted for various database systems (SQL Server, PostgreSQL, etc.)
--
-- Date: December 2025
-- ============================================================================

-- ============================================================================
-- 1. DEMOGRAPHIC ANALYSIS QUERIES
-- ============================================================================

-- 1.1 Gender Distribution
SELECT 
    Gender,
    COUNT(*) AS Total_Applications,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Applications) AS Percentage
FROM Applications
GROUP BY Gender
ORDER BY Total_Applications DESC;

-- 1.2 Ethnicity Distribution
SELECT 
    Ethnicity,
    COUNT(*) AS Total_Applications,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Applications) AS Percentage
FROM Applications
WHERE Ethnicity IS NOT NULL AND Ethnicity != ''
GROUP BY Ethnicity
ORDER BY Total_Applications DESC;

-- 1.3 First-Generation Student Statistics
SELECT 
    [First Generation] AS FirstGeneration,
    COUNT(*) AS Count,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Applications) AS Percentage,
    AVG(GPA) AS Avg_GPA,
    AVG(ACT_SCORE) AS Avg_ACT
FROM Applications
WHERE [First Generation] IS NOT NULL
GROUP BY [First Generation];

-- 1.4 Pell Eligibility Statistics
SELECT 
    Pell_Eligibility,
    COUNT(*) AS Count,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Applications) AS Percentage,
    AVG(GPA) AS Avg_GPA,
    AVG(Scholarship_Amount) AS Avg_Scholarship
FROM Applications
WHERE Pell_Eligibility IS NOT NULL
GROUP BY Pell_Eligibility;

-- ============================================================================
-- 2. COLLEGE AND PROGRAM ANALYSIS
-- ============================================================================

-- 2.1 Top Colleges by Application Volume
SELECT 
    COLLEGE_DESCR,
    COUNT(*) AS Total_Applications,
    SUM(CASE WHEN Confirmed_Date IS NOT NULL THEN 1 ELSE 0 END) AS Total_Enrollments,
    SUM(CASE WHEN Confirmed_Date IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS Enrollment_Rate
FROM Applications
WHERE COLLEGE_DESCR IS NOT NULL AND COLLEGE_DESCR != ''
GROUP BY COLLEGE_DESCR
ORDER BY Total_Applications DESC;

-- 2.2 Top Departments by Enrollment
SELECT 
    DEPARTMENT_DESCR,
    COLLEGE_DESCR,
    COUNT(*) AS Total_Enrollments,
    AVG(FirstTerm_GPA) AS Avg_FirstTerm_GPA,
    AVG(FirstTerm_CreditHours) AS Avg_CreditHours
FROM Enrollment
WHERE DEPARTMENT_DESCR IS NOT NULL AND DEPARTMENT_DESCR != ''
GROUP BY DEPARTMENT_DESCR, COLLEGE_DESCR
ORDER BY Total_Enrollments DESC;

-- 2.3 Enrollment by College and Year
SELECT 
    COLLEGE_DESCR,
    YEAR,
    COUNT(*) AS Enrollment_Count,
    AVG(FirstTerm_GPA) AS Avg_GPA,
    AVG(FirstTerm_CreditHours) AS Avg_CreditHours
FROM Enrollment
WHERE COLLEGE_DESCR IS NOT NULL
GROUP BY COLLEGE_DESCR, YEAR
ORDER BY YEAR DESC, Enrollment_Count DESC;

-- ============================================================================
-- 3. ACADEMIC QUALITY INDICATORS
-- ============================================================================

-- 3.1 Average GPA and Test Scores by College (Enrolled Students Only)
SELECT 
    a.COLLEGE_DESCR,
    COUNT(*) AS Enrolled_Count,
    AVG(a.GPA) AS Avg_GPA,
    AVG(a.ACT_SCORE) AS Avg_ACT,
    AVG(a.SAT_SCORE) AS Avg_SAT,
    AVG(a.Scholarship_Amount) AS Avg_Scholarship
FROM Applications a
WHERE a.Confirmed_Date IS NOT NULL
    AND a.COLLEGE_DESCR IS NOT NULL
GROUP BY a.COLLEGE_DESCR
ORDER BY Avg_GPA DESC;

-- 3.2 Academic Performance by First-Generation Status
SELECT 
    [First Generation] AS FirstGeneration,
    COUNT(*) AS Count,
    AVG(GPA) AS Avg_GPA,
    AVG(ACT_SCORE) AS Avg_ACT,
    AVG(Scholarship_Amount) AS Avg_Scholarship,
    SUM(CASE WHEN Confirmed_Date IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS Enrollment_Rate
FROM Applications
WHERE [First Generation] IS NOT NULL
GROUP BY [First Generation];

-- 3.3 Scholarship Distribution Analysis
SELECT 
    CASE 
        WHEN Scholarship_Amount = 0 OR Scholarship_Amount IS NULL THEN 'No Scholarship'
        WHEN Scholarship_Amount < 1000 THEN '< $1,000'
        WHEN Scholarship_Amount < 3000 THEN '$1,000 - $3,000'
        WHEN Scholarship_Amount < 5000 THEN '$3,000 - $5,000'
        WHEN Scholarship_Amount < 10000 THEN '$5,000 - $10,000'
        ELSE '> $10,000'
    END AS Scholarship_Range,
    COUNT(*) AS Student_Count,
    AVG(GPA) AS Avg_GPA,
    AVG(ACT_SCORE) AS Avg_ACT
FROM Applications
WHERE Confirmed_Date IS NOT NULL
GROUP BY 
    CASE 
        WHEN Scholarship_Amount = 0 OR Scholarship_Amount IS NULL THEN 'No Scholarship'
        WHEN Scholarship_Amount < 1000 THEN '< $1,000'
        WHEN Scholarship_Amount < 3000 THEN '$1,000 - $3,000'
        WHEN Scholarship_Amount < 5000 THEN '$3,000 - $5,000'
        WHEN Scholarship_Amount < 10000 THEN '$5,000 - $10,000'
        ELSE '> $10,000'
    END
ORDER BY MIN(Scholarship_Amount);

-- ============================================================================
-- 4. ENROLLMENT TRENDS ANALYSIS
-- ============================================================================

-- 4.1 Applications and Enrollments by Year
SELECT 
    Year,
    COUNT(*) AS Total_Applications,
    SUM(CASE WHEN Confirmed_Date IS NOT NULL THEN 1 ELSE 0 END) AS Total_Enrollments,
    SUM(CASE WHEN Confirmed_Date IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS Enrollment_Rate
FROM Applications
GROUP BY Year
ORDER BY Year;

-- 4.2 Enrollment Trends by Month (Application Date)
SELECT 
    YEAR(Applied_Date) AS Year,
    MONTH(Applied_Date) AS Month,
    COUNT(*) AS Application_Count,
    SUM(CASE WHEN Confirmed_Date IS NOT NULL THEN 1 ELSE 0 END) AS Enrollment_Count
FROM Applications
WHERE Applied_Date IS NOT NULL
GROUP BY YEAR(Applied_Date), MONTH(Applied_Date)
ORDER BY Year, Month;

-- 4.3 Year-over-Year Growth in Applications
WITH YearlyApplications AS (
    SELECT 
        Year,
        COUNT(*) AS Application_Count
    FROM Applications
    GROUP BY Year
)
SELECT 
    a.Year,
    a.Application_Count,
    LAG(a.Application_Count) OVER (ORDER BY a.Year) AS Previous_Year_Count,
    a.Application_Count - LAG(a.Application_Count) OVER (ORDER BY a.Year) AS Year_Over_Year_Change,
    (a.Application_Count - LAG(a.Application_Count) OVER (ORDER BY a.Year)) * 100.0 / 
        LAG(a.Application_Count) OVER (ORDER BY a.Year) AS YoY_Percentage_Change
FROM YearlyApplications a
ORDER BY a.Year;

-- ============================================================================
-- 5. RETENTION ANALYSIS
-- ============================================================================

-- 5.1 Overall Retention Rates
SELECT 
    COUNT(*) AS Total_Enrolled,
    SUM([OneYear retention]) AS One_Year_Retained,
    SUM([TwoYear retention]) AS Two_Year_Retained,
    SUM([OneYear retention]) * 100.0 / COUNT(*) AS One_Year_Retention_Rate,
    SUM([TwoYear retention]) * 100.0 / COUNT(*) AS Two_Year_Retention_Rate
FROM Enrollment
WHERE [OneYear retention] IS NOT NULL;

-- 5.2 Retention Rates by College
SELECT 
    COLLEGE_DESCR,
    COUNT(*) AS Total_Enrolled,
    SUM([OneYear retention]) AS One_Year_Retained,
    SUM([TwoYear retention]) AS Two_Year_Retained,
    SUM([OneYear retention]) * 100.0 / COUNT(*) AS One_Year_Retention_Rate,
    SUM([TwoYear retention]) * 100.0 / COUNT(*) AS Two_Year_Retention_Rate,
    AVG(FirstTerm_GPA) AS Avg_FirstTerm_GPA
FROM Enrollment
WHERE COLLEGE_DESCR IS NOT NULL
    AND [OneYear retention] IS NOT NULL
GROUP BY COLLEGE_DESCR
ORDER BY One_Year_Retention_Rate DESC;

-- 5.3 Retention Rates by Full-Time/Part-Time Status
SELECT 
    FTPT,
    COUNT(*) AS Total_Enrolled,
    SUM([OneYear retention]) AS One_Year_Retained,
    SUM([TwoYear retention]) AS Two_Year_Retained,
    SUM([OneYear retention]) * 100.0 / COUNT(*) AS One_Year_Retention_Rate,
    SUM([TwoYear retention]) * 100.0 / COUNT(*) AS Two_Year_Retention_Rate
FROM Enrollment
WHERE FTPT IS NOT NULL
    AND [OneYear retention] IS NOT NULL
GROUP BY FTPT;

-- 5.4 Retention Rates by First-Term GPA Ranges
SELECT 
    CASE 
        WHEN FirstTerm_GPA >= 3.5 THEN '3.5 - 4.0'
        WHEN FirstTerm_GPA >= 3.0 THEN '3.0 - 3.5'
        WHEN FirstTerm_GPA >= 2.5 THEN '2.5 - 3.0'
        WHEN FirstTerm_GPA >= 2.0 THEN '2.0 - 2.5'
        WHEN FirstTerm_GPA >= 0 THEN '0 - 2.0'
        ELSE 'No GPA'
    END AS GPA_Range,
    COUNT(*) AS Total_Enrolled,
    SUM([OneYear retention]) * 100.0 / COUNT(*) AS One_Year_Retention_Rate,
    SUM([TwoYear retention]) * 100.0 / COUNT(*) AS Two_Year_Retention_Rate
FROM Enrollment
WHERE FirstTerm_GPA IS NOT NULL
    AND [OneYear retention] IS NOT NULL
GROUP BY 
    CASE 
        WHEN FirstTerm_GPA >= 3.5 THEN '3.5 - 4.0'
        WHEN FirstTerm_GPA >= 3.0 THEN '3.0 - 3.5'
        WHEN FirstTerm_GPA >= 2.5 THEN '2.5 - 3.0'
        WHEN FirstTerm_GPA >= 2.0 THEN '2.0 - 2.5'
        WHEN FirstTerm_GPA >= 0 THEN '0 - 2.0'
        ELSE 'No GPA'
    END
ORDER BY MIN(FirstTerm_GPA) DESC;

-- ============================================================================
-- 6. DIVERSITY ANALYSIS BY COLLEGE
-- ============================================================================

-- 6.1 Gender Distribution by College
SELECT 
    COLLEGE_DESCR,
    Gender,
    COUNT(*) AS Count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY COLLEGE_DESCR) AS Percentage
FROM Applications
WHERE COLLEGE_DESCR IS NOT NULL
    AND Confirmed_Date IS NOT NULL
    AND Gender IS NOT NULL
GROUP BY COLLEGE_DESCR, Gender
ORDER BY COLLEGE_DESCR, Count DESC;

-- 6.2 Ethnicity Distribution by College
SELECT 
    COLLEGE_DESCR,
    Ethnicity,
    COUNT(*) AS Count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY COLLEGE_DESCR) AS Percentage
FROM Applications
WHERE COLLEGE_DESCR IS NOT NULL
    AND Confirmed_Date IS NOT NULL
    AND Ethnicity IS NOT NULL
GROUP BY COLLEGE_DESCR, Ethnicity
ORDER BY COLLEGE_DESCR, Count DESC;

-- 6.3 First-Generation and Pell Eligibility by College
SELECT 
    COLLEGE_DESCR,
    COUNT(*) AS Total_Enrolled,
    SUM([First Generation]) * 100.0 / COUNT(*) AS FirstGen_Percentage,
    SUM(CASE WHEN Pell_Eligibility = 'Y' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS Pell_Percentage,
    SUM(CASE WHEN Ethnicity IN ('Black/African American', 'Hispanic/Latino', 
                                'American Indian/Alaska Native', 'Native Hawaiian/Pacific Islander') 
        THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS URM_Percentage
FROM Applications
WHERE COLLEGE_DESCR IS NOT NULL
    AND Confirmed_Date IS NOT NULL
GROUP BY COLLEGE_DESCR
ORDER BY Total_Enrolled DESC;

-- ============================================================================
-- 7. ACADEMIC PERFORMANCE ANALYSIS
-- ============================================================================

-- 7.1 First-Term Performance by College
SELECT 
    e.COLLEGE_DESCR,
    COUNT(*) AS Student_Count,
    AVG(e.FirstTerm_GPA) AS Avg_FirstTerm_GPA,
    AVG(e.FirstTerm_CreditHours) AS Avg_CreditHours,
    SUM(e.[OneYear retention]) * 100.0 / COUNT(*) AS Retention_Rate
FROM Enrollment e
WHERE e.COLLEGE_DESCR IS NOT NULL
GROUP BY e.COLLEGE_DESCR
ORDER BY Avg_FirstTerm_GPA DESC;

-- 7.2 Correlation between High School GPA and First-Term GPA
SELECT 
    CASE 
        WHEN a.GPA >= 3.5 THEN '3.5 - 4.0'
        WHEN a.GPA >= 3.0 THEN '3.0 - 3.5'
        WHEN a.GPA >= 2.5 THEN '2.5 - 3.0'
        WHEN a.GPA >= 2.0 THEN '2.0 - 2.5'
        WHEN a.GPA >= 0 THEN '0 - 2.0'
        ELSE 'No GPA'
    END AS HS_GPA_Range,
    COUNT(*) AS Student_Count,
    AVG(e.FirstTerm_GPA) AS Avg_FirstTerm_GPA,
    AVG(e.FirstTerm_CreditHours) AS Avg_CreditHours,
    SUM(e.[OneYear retention]) * 100.0 / COUNT(*) AS Retention_Rate
FROM Applications a
INNER JOIN Enrollment e ON a.ID = e.ID
WHERE a.GPA IS NOT NULL
    AND e.FirstTerm_GPA IS NOT NULL
GROUP BY 
    CASE 
        WHEN a.GPA >= 3.5 THEN '3.5 - 4.0'
        WHEN a.GPA >= 3.0 THEN '3.0 - 3.5'
        WHEN a.GPA >= 2.5 THEN '2.5 - 3.0'
        WHEN a.GPA >= 2.0 THEN '2.0 - 2.5'
        WHEN a.GPA >= 0 THEN '0 - 2.0'
        ELSE 'No GPA'
    END
ORDER BY MIN(a.GPA) DESC;

-- ============================================================================
-- 8. TIME-TO-ENROLLMENT ANALYSIS
-- ============================================================================

-- 8.1 Average Days from Application to Confirmation
SELECT 
    COLLEGE_DESCR,
    COUNT(*) AS Enrollment_Count,
    AVG(DATEDIFF(day, Applied_Date, Confirmed_Date)) AS Avg_Days_to_Confirmation,
    MIN(DATEDIFF(day, Applied_Date, Confirmed_Date)) AS Min_Days,
    MAX(DATEDIFF(day, Applied_Date, Confirmed_Date)) AS Max_Days
FROM Applications
WHERE Confirmed_Date IS NOT NULL
    AND Applied_Date IS NOT NULL
    AND COLLEGE_DESCR IS NOT NULL
GROUP BY COLLEGE_DESCR
ORDER BY Avg_Days_to_Confirmation;

-- 8.2 Application Timing Analysis
SELECT 
    YEAR(Applied_Date) AS Year,
    MONTH(Applied_Date) AS Month,
    COUNT(*) AS Application_Count,
    SUM(CASE WHEN Confirmed_Date IS NOT NULL THEN 1 ELSE 0 END) AS Enrollment_Count,
    SUM(CASE WHEN Confirmed_Date IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS Enrollment_Rate
FROM Applications
WHERE Applied_Date IS NOT NULL
GROUP BY YEAR(Applied_Date), MONTH(Applied_Date)
ORDER BY Year, Month;

-- ============================================================================
-- END OF SQL QUERIES
-- ============================================================================

