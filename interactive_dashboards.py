"""
Interactive Dashboard Script
============================
Creates interactive Plotly dashboards for the University of Akron student data
analysis. Produces HTML files that support hover tooltips, zooming, and legend
interaction for exploration during the presentation.

Date: December 2025
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def load_processed_data():
    """Load and lightly preprocess data for interactive visualizations."""
    app_df = pd.read_csv("Applications _Data.csv")
    enroll_df = pd.read_csv("Enrollment_Data.csv")

    # Dates and flags
    app_df["Applied Date"] = pd.to_datetime(app_df["Applied Date"], errors="coerce")
    app_df["Confirmed Date"] = pd.to_datetime(app_df["Confirmed Date"], errors="coerce")
    app_df["Enrolled"] = app_df["Confirmed Date"].notna()

    # Numerics
    app_df["GPA"] = pd.to_numeric(app_df["GPA"], errors="coerce")
    app_df["ACT_SCORE"] = pd.to_numeric(app_df["ACT_SCORE"], errors="coerce")
    app_df["Scholarship_Amount"] = pd.to_numeric(
        app_df["Scholarship_Amount"], errors="coerce"
    )

    enroll_df["FirstTerm_GPA"] = pd.to_numeric(
        enroll_df["FirstTerm_GPA"], errors="coerce"
    )
    enroll_df["FirstTerm_CreditHours"] = pd.to_numeric(
        enroll_df["FirstTerm_CreditHours"], errors="coerce"
    )
    enroll_df["OneYear_Retention"] = enroll_df["OneYear retention"].apply(
        lambda x: 1 if pd.notna(x) and str(x).strip() == "1" else 0
    )

    return app_df, enroll_df


def create_executive_dashboard_interactive():
    """Interactive executive dashboard (HTML)."""
    app_df, enroll_df = load_processed_data()

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Applications vs Enrollments by Year",
            "Enrollment Rate by Year",
            "Top 5 Colleges by Enrollment",
            "Average GPA Trend (Enrolled Students)",
        ),
        horizontal_spacing=0.12,
        vertical_spacing=0.22,  # extra padding between rows
    )

    # Applications vs Enrollments
    app_by_year = app_df.groupby("Year").agg({"ID": "count", "Enrolled": "sum"}).reset_index()
    fig.add_trace(
        go.Scatter(
            x=app_by_year["Year"],
            y=app_by_year["ID"],
            mode="lines+markers",
            name="Applications",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=app_by_year["Year"],
            y=app_by_year["Enrolled"],
            mode="lines+markers",
            name="Enrollments",
        ),
        row=1,
        col=1,
    )

    # Enrollment rate
    app_by_year["Enrollment_Rate"] = (
        app_by_year["Enrolled"] / app_by_year["ID"] * 100
    )
    fig.add_trace(
        go.Bar(
            x=app_by_year["Year"],
            y=app_by_year["Enrollment_Rate"],
            name="Enrollment Rate (%)",
            hovertemplate="Year %{x}<br>Rate %{y:.1f}%",
        ),
        row=1,
        col=2,
    )

    # Top colleges
    top_colleges = (
        enroll_df["COLLEGE_DESCR"]
        .value_counts()
        .head(5)
        .rename_axis("College")
        .reset_index(name="Enrollments")
    )
    fig.add_trace(
        go.Bar(
            x=top_colleges["Enrollments"],
            y=top_colleges["College"],
            orientation="h",
            name="Top Colleges",
        ),
        row=2,
        col=1,
    )

    # GPA trend
    enrolled = app_df[app_df["Enrolled"]]
    gpa_by_year = (
        enrolled.groupby("Year")["GPA"].mean().reset_index(name="Average_GPA")
    )
    fig.add_trace(
        go.Scatter(
            x=gpa_by_year["Year"],
            y=gpa_by_year["Average_GPA"],
            mode="lines+markers",
            name="Avg GPA",
            hovertemplate="Year %{x}<br>GPA %{y:.2f}",
        ),
        row=2,
        col=2,
    )

    fig.update_layout(
        title_text=(
            "Executive Dashboard (Interactive)<br>"
            "Student Analytics Overview (2016–2021)"
        ),
        height=800,
        showlegend=True,
        legend_title_text="Metric",
        template="plotly_white",
        # generous margins so titles, axes labels, and legends never overlap
        margin=dict(t=120, l=80, r=60, b=90),
    )

    fig.update_xaxes(title_text="Academic Year", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_xaxes(title_text="Academic Year", row=1, col=2)
    fig.update_yaxes(title_text="Enrollment Rate (%)", row=1, col=2)
    fig.update_xaxes(title_text="Enrollments", row=2, col=1)
    fig.update_yaxes(title_text="College", row=2, col=1)
    fig.update_xaxes(title_text="Academic Year", row=2, col=2)
    fig.update_yaxes(title_text="Average GPA", row=2, col=2)

    fig.write_html("Executive_Dashboard_Interactive.html")
    print("Interactive Executive Dashboard saved as 'Executive_Dashboard_Interactive.html'")


def create_admissions_dashboard_interactive():
    """Interactive admissions dashboard (HTML)."""
    app_df, enroll_df = load_processed_data()
    enrolled = app_df[app_df["Enrolled"]]

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Application Volume by Month",
            "Enrollment Rate by College",
            "ACT Score Distribution (Enrolled)",
            "GPA vs Scholarship (Enrolled)",
        ),
        horizontal_spacing=0.12,
        vertical_spacing=0.22,
    )

    # Applications by month
    app_df["Applied_Month"] = app_df["Applied Date"].dt.month
    monthly_apps = (
        app_df.groupby("Applied_Month")["ID"].count().reset_index(name="Applications")
    )
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    fig.add_trace(
        go.Bar(
            x=[month_labels[m - 1] for m in monthly_apps["Applied_Month"]],
            y=monthly_apps["Applications"],
            name="Applications",
        ),
        row=1,
        col=1,
    )

    # Enrollment rate by college
    enr_rate = (
        app_df.groupby("COLLEGE_DESCR")
        .agg(Apps=("ID", "count"), Enr=("Enrolled", "sum"))
        .reset_index()
    )
    enr_rate["Enrollment_Rate"] = enr_rate["Enr"] / enr_rate["Apps"] * 100
    enr_rate = enr_rate.sort_values("Enrollment_Rate", ascending=False).head(10)
    fig.add_trace(
        go.Bar(
            x=enr_rate["Enrollment_Rate"],
            y=enr_rate["COLLEGE_DESCR"],
            orientation="h",
            name="Enrollment Rate",
            hovertemplate="%{y}<br>%{x:.1f}% enrollment rate",
        ),
        row=1,
        col=2,
    )

    # ACT distribution
    fig.add_trace(
        go.Histogram(
            x=enrolled["ACT_SCORE"],
            nbinsx=20,
            name="ACT Score",
            hovertemplate="ACT %{x}<br>Count %{y}",
        ),
        row=2,
        col=1,
    )

    # GPA vs Scholarship scatter
    scatter_data = enrolled.dropna(subset=["GPA", "Scholarship_Amount"])
    fig.add_trace(
        go.Scatter(
            x=scatter_data["GPA"],
            y=scatter_data["Scholarship_Amount"],
            mode="markers",
            marker=dict(size=5, opacity=0.6),
            name="GPA vs Scholarship",
            hovertemplate="GPA %{x:.2f}<br>Scholarship $%{y:.0f}",
        ),
        row=2,
        col=2,
    )

    fig.update_layout(
        title_text="Admissions Dashboard (Interactive)<br>Application and Enrollment Analytics",
        height=800,
        template="plotly_white",
        showlegend=False,
        margin=dict(t=120, l=80, r=60, b=90),
    )

    fig.update_xaxes(title_text="Month", row=1, col=1)
    fig.update_yaxes(title_text="Applications", row=1, col=1)
    fig.update_xaxes(title_text="Enrollment Rate (%)", row=1, col=2)
    fig.update_yaxes(title_text="College", row=1, col=2)
    fig.update_xaxes(title_text="ACT Score", row=2, col=1)
    fig.update_yaxes(title_text="Count", row=2, col=1)
    fig.update_xaxes(title_text="GPA", row=2, col=2)
    fig.update_yaxes(title_text="Scholarship Amount ($)", row=2, col=2)

    fig.write_html("Admissions_Dashboard_Interactive.html")
    print("Interactive Admissions Dashboard saved as 'Admissions_Dashboard_Interactive.html'")


def create_college_dean_dashboard_interactive():
    """Interactive college-deans dashboard (HTML)."""
    app_df, enroll_df = load_processed_data()

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Enrollment Trends by College",
            "Average First-Term GPA by College",
            "Average First-Term Credit Hours by College",
            "Top 10 Departments by Enrollment",
        ),
        horizontal_spacing=0.12,
        vertical_spacing=0.22,
    )

    # Enrollment trends (top 5 colleges)
    top_colleges = (
        enroll_df["COLLEGE_DESCR"].value_counts().head(5).index.tolist()
    )
    for college in top_colleges:
        sub = enroll_df[enroll_df["COLLEGE_DESCR"] == college]
        series = sub.groupby("YEAR")["ID"].count().reset_index(name="Enrollments")
        fig.add_trace(
            go.Scatter(
                x=series["YEAR"],
                y=series["Enrollments"],
                mode="lines+markers",
                name=college,
            ),
            row=1,
            col=1,
        )

    # Avg GPA by college
    gpa_by_college = (
        enroll_df.groupby("COLLEGE_DESCR")["FirstTerm_GPA"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig.add_trace(
        go.Bar(
            x=gpa_by_college["FirstTerm_GPA"],
            y=gpa_by_college["COLLEGE_DESCR"],
            orientation="h",
            name="Avg First-Term GPA",
        ),
        row=1,
        col=2,
    )

    # Avg credit hours
    ch_by_college = (
        enroll_df.groupby("COLLEGE_DESCR")["FirstTerm_CreditHours"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig.add_trace(
        go.Bar(
            x=ch_by_college["FirstTerm_CreditHours"],
            y=ch_by_college["COLLEGE_DESCR"],
            orientation="h",
            name="Avg Credit Hours",
        ),
        row=2,
        col=1,
    )

    # Top departments by enrollment
    top_depts = (
        enroll_df["DEPARTMENT_DESCR"]
        .value_counts()
        .head(10)
        .rename_axis("DEPARTMENT_DESCR")
        .reset_index(name="Enrollments")
    )
    fig.add_trace(
        go.Bar(
            x=top_depts["Enrollments"],
            y=top_depts["DEPARTMENT_DESCR"],
            orientation="h",
            name="Top Departments",
        ),
        row=2,
        col=2,
    )

    fig.update_layout(
        title_text="College Deans Dashboard (Interactive)<br>College Performance Metrics",
        height=800,
        template="plotly_white",
        margin=dict(t=120, l=80, r=60, b=90),
    )

    fig.update_xaxes(title_text="Academic Year", row=1, col=1)
    fig.update_yaxes(title_text="Enrollments", row=1, col=1)
    fig.update_xaxes(title_text="Average GPA", row=1, col=2)
    fig.update_yaxes(title_text="College", row=1, col=2)
    fig.update_xaxes(title_text="Average Credit Hours", row=2, col=1)
    fig.update_yaxes(title_text="College", row=2, col=1)
    fig.update_xaxes(title_text="Enrollments", row=2, col=2)
    fig.update_yaxes(title_text="Department", row=2, col=2)

    fig.write_html("College_Deans_Dashboard_Interactive.html")
    print("Interactive College Deans Dashboard saved as 'College_Deans_Dashboard_Interactive.html'")


def create_diversity_dashboard_interactive():
    """Interactive diversity dashboard (HTML)."""
    app_df, enroll_df = load_processed_data()
    enrolled = app_df[app_df["Enrolled"]]

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Ethnicity Distribution by Year",
            "First-Generation % by College",
            "Pell Eligibility % by College",
            "Diversity Index Trend (Simpson's Index)",
        ),
        horizontal_spacing=0.12,
        vertical_spacing=0.22,
    )

    # Ethnicity over time (stacked area)
    eth_year = (
        enrolled.groupby(["Year", "Ethnicity"])
        .size()
        .reset_index(name="Count")
    )
    for eth in eth_year["Ethnicity"].unique():
        sub = eth_year[eth_year["Ethnicity"] == eth]
        fig.add_trace(
            go.Scatter(
                x=sub["Year"],
                y=sub["Count"],
                stackgroup="one",
                name=str(eth),
                hovertemplate="Year %{x}<br>%{y} students",
            ),
            row=1,
            col=1,
        )

    # First-gen % by college
    fg = (
        enrolled.groupby("COLLEGE_DESCR")["First Generation"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .mul(100)
        .reset_index(name="FirstGenPct")
    )
    fig.add_trace(
        go.Bar(
            x=fg["FirstGenPct"],
            y=fg["COLLEGE_DESCR"],
            orientation="h",
            name="First-Generation %",
        ),
        row=1,
        col=2,
    )

    # Pell % by college
    pell = (
        enrolled.groupby("COLLEGE_DESCR")["Pell_Eligibility"]
        .apply(lambda x: (x == "Y").sum() / len(x) * 100)
        .sort_values(ascending=False)
        .head(10)
        .reset_index(name="PellPct")
    )
    fig.add_trace(
        go.Bar(
            x=pell["PellPct"],
            y=pell["COLLEGE_DESCR"],
            orientation="h",
            name="Pell %",
        ),
        row=2,
        col=1,
    )

    # Diversity index
    diversity_index = []
    for year in sorted(enrolled["Year"].unique()):
        year_data = enrolled[enrolled["Year"] == year]
        counts = year_data["Ethnicity"].value_counts()
        total = counts.sum()
        diversity = 1 - np.sum((counts / total) ** 2)
        diversity_index.append({"Year": year, "Diversity_Index": diversity})
    div_df = pd.DataFrame(diversity_index)
    fig.add_trace(
        go.Scatter(
            x=div_df["Year"],
            y=div_df["Diversity_Index"],
            mode="lines+markers",
            name="Diversity Index",
            hovertemplate="Year %{x}<br>Index %{y:.3f}",
        ),
        row=2,
        col=2,
    )

    fig.update_layout(
        title_text="Diversity and Inclusion Dashboard (Interactive)<br>Student Demographics Analysis",
        height=800,
        template="plotly_white",
        margin=dict(t=120, l=80, r=60, b=90),
    )

    fig.update_xaxes(title_text="Academic Year", row=1, col=1)
    fig.update_yaxes(title_text="Students (stacked)", row=1, col=1)
    fig.update_xaxes(title_text="First-Generation %", row=1, col=2)
    fig.update_yaxes(title_text="College", row=1, col=2)
    fig.update_xaxes(title_text="Pell %", row=2, col=1)
    fig.update_yaxes(title_text="College", row=2, col=1)
    fig.update_xaxes(title_text="Academic Year", row=2, col=2)
    fig.update_yaxes(title_text="Diversity Index (0–1)", row=2, col=2)

    fig.write_html("Diversity_Dashboard_Interactive.html")
    print("Interactive Diversity Dashboard saved as 'Diversity_Dashboard_Interactive.html'")


def main():
    """Generate all interactive dashboards."""
    print("=" * 60)
    print("GENERATING INTERACTIVE DASHBOARDS")
    print("=" * 60)

    create_executive_dashboard_interactive()
    create_admissions_dashboard_interactive()
    create_college_dean_dashboard_interactive()
    create_diversity_dashboard_interactive()

    print("\n" + "=" * 60)
    print("All interactive dashboards generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()


