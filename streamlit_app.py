import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def train_arima(df, top_activities):
    # Loop through each category for forecasting
    for category_to_forecast in top_activities:
        # Filter data for the specific category and the specified time range
        category_df = df[(df['PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN'] == category_to_forecast) & 
                         (df['Registration_Year'] >= 1990) & (df['Registration_Year'] <= 2020)]

        # Extract relevant features and target variable
        X = category_df[['Registration_Year']]
        y = category_df.groupby('Registration_Year').size()

        # Convert 'Registration_Year' to DateTime format
        y.index = pd.to_datetime(y.index, format='%Y')

        # Fit ARIMA model
        model = ARIMA(y, order=(1, 1, 1))  # Adjust order as needed
        fit_model = model.fit()

        # Forecast registrations for the next 5 years (2021-2025)
        forecast_steps = 5
        forecast_values = fit_model.forecast(steps=forecast_steps)

        # Plot the forecast
        plt.figure(figsize=(16, 6))
        plt.plot(y.index.year, y.values, marker='o', label='Historical Data')
        plt.plot(range(y.index.year.max() + 1, y.index.year.max() + 1 + forecast_steps), forecast_values, marker='o', label='Forecast')
        plt.title(f'Forecast of {category_to_forecast} registrations (2021-2025)')
        plt.xticks(np.arange(1990, 2026, 1),rotation=90)
        plt.xlabel('Year')
        plt.ylabel('Count of Registrations')
        plt.legend()
        st.pyplot(plt)

        # Display the forecasted values
        st.write(f"Forecasted registrations for {category_to_forecast} for 2021-2025:")
        st.write(forecast_values)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def train_arima(df, top_business_activities):
    # ARIMA model training code goes here
    pass

def main():
    st.title("Company Analysis App")

    # Create a list of file extensions to display in the dropdown
    file_extensions = [".csv", ".xlsx"]

    # Create the dropdown file selector
    selected_file = st.selectbox("Choose a file", file_extensions)

    if selected_file is not None:
        if selected_file == ".csv":
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        elif selected_file == ".xlsx":
            uploaded_file = st.file_uploader("Choose an XLSX file", type="xlsx")

        if uploaded_file is not None:
            if selected_file == ".csv":
                df = pd.read_csv(uploaded_file, encoding='ISO-8859-1', low_memory=False)
            elif selected_file == ".xlsx":
                df = pd.read_excel(uploaded_file)

            # Assuming df is your DataFrame
            # Filter out rows with unknown or invalid values in 'DATE_OF_REGISTRATION'
            df = df[pd.to_datetime(df['DATE_OF_REGISTRATION'], errors='coerce', dayfirst=True).notna()]

            # Convert 'DATE_OF_REGISTRATION' to datetime format
            df['DATE_OF_REGISTRATION'] = pd.to_datetime(df['DATE_OF_REGISTRATION'], errors='coerce', dayfirst=True)

            # Extract year from the registration date
            df['Registration_Year'] = df['DATE_OF_REGISTRATION'].dt.year

            df = df.drop(['DATE_OF_REGISTRATION', 'EMAIL_ADDR'], axis=1)
            st.write(df)

            # EDA - Trends over time
            plt.figure(figsize=(21, 9))
            sns.countplot(x='Registration_Year', data=df[(df['Registration_Year']<=2020) & (df['Registration_Year']>=1990)])
            plt.title('Company Registrations Over Time')
            plt.xlabel('Registration Year')
            plt.ylabel('Count')
            plt.xticks(rotation=90)
            st.pyplot(plt)

            # EDA - Company Status
            plt.figure(figsize=(12, 5))
            sns.countplot(x='Company_status', data=df[(df['Registration_Year']<=2020) & (df['Registration_Year']>=1990)])
            plt.title('Distribution of Company Status')
            plt.xlabel('Company Status')
            plt.ylabel('Count')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(plt)

            # EDA - Relationship between Authorized Capital and Paid-up Capital
            st.write("**Authorized Capital**: This is the maximum amount of share capital that a company is authorized to issue to shareholders.")
            st.write("**Paid-up Capital**: This is the amount of money a company has received from shareholders in exchange for shares.")
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x='AUTHORIZED_CAP', y='PAIDUP_CAPITAL', data=df[(df['Registration_Year']<=2020) & (df['Registration_Year']>=1990)])
            plt.title('Authorized Capital vs Paid-up Capital')
            plt.xlabel('Authorized Capital')
            plt.ylabel('Paid-up Capital')
            st.pyplot(plt)

            df['Company_Category'] = df['Company_Category'].replace(' ', np.nan)

            # EDA - Distribution of Company Categories
            plt.figure(figsize=(10, 6))
            sns.countplot(x='Company_Category', data=df[(df['Registration_Year']<=2020) & (df['Registration_Year']>=1990)])
            plt.title('Distribution of Company Categories')
            plt.xlabel('Company Category')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            st.pyplot(plt)

            # EDA - Distribution of Principal Business Activities
            plt.figure(figsize=(14, 6))
            sns.countplot(x='PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN', data=df[(df['Registration_Year']<=2020) & (df['Registration_Year']>=1990)], order=df['PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN'].value_counts().index)
            plt.title('Distribution of Principal Business Activities')
            plt.xlabel('Principal Business Activity')
            plt.ylabel('Count')
            plt.xticks(rotation=90, ha='right')
            st.pyplot(plt)

            # Find the top 5 business activities for each year
            top_activities_per_year = df.loc[(df['Registration_Year']>=1990) & (df['Registration_Year'] <= 2020)].groupby('Registration_Year')['PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN'].apply(lambda x: x.value_counts().nlargest(5).index.tolist())

            # Create a unique list of top activities over all years
            top_activities = []
            for activities in top_activities_per_year:
                top_activities += activities
            top_activities = list(set(top_activities))

            # Filter the dataframe to include only the top activities
            df_top_activities = df[df['PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN'].isin(top_activities)]

            # Find the top 5 activities over all years
            top_5_activities_overall = df_top_activities['PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN'].value_counts().nlargest(5).index.tolist()

            plt.figure(figsize=(16, 8), dpi=300)
            sns.countplot(x='Registration_Year', hue='PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN', data=df_top_activities[(df_top_activities['Registration_Year']>=1990) & (df_top_activities['Registration_Year']<=2020)], palette='Set1', hue_order=top_5_activities_overall)
            plt.title('Top 5 Principal Business Activities Over Time')
            plt.xlabel('Registration Year')
            plt.ylabel('Count')
            plt.xticks(rotation=90)
            plt.legend(title='Principal Business Activity', fontsize='small')
            st.pyplot(plt)

            # Filter companies registered between 2013 and 2020
            filtered_df = df[(df['Registration_Year'] >= 2013) & (df['Registration_Year'] <= 2020)]

            # Get the top 5 business activities
            top_business_activities = filtered_df['PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN'].value_counts().head(5)

            # Print the result
            st.write("Top 5 PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN from 2013 to 2020:")
            st.write(top_business_activities)

            # Convert columns to appropriate data types
            df.loc[:, 'AUTHORIZED_CAP'] = df['AUTHORIZED_CAP'].astype(float)
            df.loc[:, 'PAIDUP_CAPITAL'] = df['PAIDUP_CAPITAL'].astype(float)

            # Group by 'PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN' and calculate the mean of 'AUTHORIZED_CAP' and 'PAIDUP_CAPITAL'
            grouped_df = df.groupby('PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN')[['AUTHORIZED_CAP', 'PAIDUP_CAPITAL']].mean().reset_index()

            # Trend analysis of Authorized capital
            # Ensure the DataFrame is sorted by the time column
            df = df.sort_values(by='Registration_Year')

            # Calculate the percentage change in authorized capital for each activity over time
            st.write("**Capital Change**: This refers to the percentage change in a company's capital over time. It can be used to analyze trends and make financial decisions.")
            df['CAPITAL_CHANGE'] = df.groupby(['PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN', 'Registration_Year'])['AUTHORIZED_CAP'].pct_change().fillna(0)

            # Group by 'PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN' and calculate the mean of 'CAPITAL_CHANGE'
            activity_trend_df = df.groupby(['PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN','Registration_Year'])['CAPITAL_CHANGE'].mean().reset_index()

            # Print the new DataFrame with the trend analysis
            activity_trend_df2 = activity_trend_df.interpolate()
            st.write(activity_trend_df2)

            # Get all unique activities
            activities = df['PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN'].unique().tolist()

            # Let the user select the activities to compare
            selected_activities = st.multiselect("Select the activities to compare", activities)
            # Create an empty DataFrame to store the results
            results_df = pd.DataFrame(columns=['Activity_1', 'Activity_2', 'Comparison'])

            # Comparative Analysis: This compares the mean paid-up capital of all business activities.
            # It helps in understanding their relative performance and market standing.
            for i in range(len(grouped_df) - 1):
                for j in range(i + 1, len(grouped_df)):
                    if grouped_df.loc[i, 'PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN'] in selected_activities and grouped_df.loc[j, 'PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN'] in selected_activities:
                        activity1_capital = grouped_df.loc[i, 'PAIDUP_CAPITAL']
                        activity2_capital = grouped_df.loc[j, 'PAIDUP_CAPITAL']
                        comparison = activity1_capital / activity2_capital
                        new_row = pd.DataFrame({'Activity_1': [grouped_df.loc[i, 'PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN']],
                                               'Activity_2': [grouped_df.loc[j, 'PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN']],
                                               'Comparison': [comparison]})
                        results_df = pd.concat([results_df, new_row], ignore_index=True)

            # Print the results DataFrame
            st.write(results_df)

            # Liquidity Ratios: This calculates the liquidity ratio (authorized capital to paid-up capital) for each company.
            # It is crucial for assessing the financial health of a company.
            st.write("**Liquidity Ratios**: This calculates the liquidity ratio (authorized capital to paid-up capital) for each company. It is crucial for assessing the financial health of a company.")
            df.loc[:, 'LIQUIDITY_RATIO'] = df['AUTHORIZED_CAP'] / df['PAIDUP_CAPITAL']

            # create a smaller DataFrame to showcase the liquidity ratios
            # Selecting relevant columns for the smaller DataFrame
            liquidity_df = df[['Company_Name', 'AUTHORIZED_CAP', 'PAIDUP_CAPITAL', 'LIQUIDITY_RATIO']].copy()

            # Get all unique companies
            companies = df['Company_Name'].unique().tolist()

            # Let the user select the companies to compare
            selected_companies = st.multiselect("Select the companies to compare for liquidity ratios", companies)

            # Filter the DataFrame based on the selected companies
            liquidity_df = liquidity_df[liquidity_df['Company_Name'].isin(selected_companies)]

            # Displaying the smaller DataFrame
            st.write("Smaller DataFrame showcasing Liquidity Ratios.")
            st.write(liquidity_df)

            # Get the top 5 business activities over all years
            top_business_activities = filtered_df['PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN'].value_counts().head(5).index.tolist()

            # Now use this top 5 to train ARIMA
            train_arima(df, top_business_activities)

if __name__ == "__main__":
    main()
