import pandas as pd
import plotly.express as px


df_enrollement = pd.read_csv(r'c:\Users\james\Documents\Repos\cbds-take-home\data\enrollments.csv')
df_gdp = pd.read_csv(r'c:\Users\james\Documents\Repos\cbds-take-home\data\Countries GDP 1960-2020.csv')


df_gdp = df_gdp.melt(id_vars=["Country Name", "Country Code"],
            var_name="year",
            value_name="gdp").sort_values(by='Country Name').reset_index()
df_gdp["year"] = df_gdp["year"].astype('float64')

df_joined = pd.merge(df_enrollement, df_gdp, left_on=["year", "countrycode"], right_on=["year", "Country Code"])

df_agg = df_joined.groupby(['country', 'year']).\
        agg(students5_estimated_mean=('students5_estimated', 'mean'),
            students5_estimated_std=('students5_estimated', 'std'),
            students5_estimated_sum=('students5_estimated', 'sum')).reset_index()

df_joined = pd.merge(df_joined, df_agg, on=["country", "year"])

fig = px.scatter(
    df_joined, 
    x="year", 
    y="students5_estimated_sum", 
    color="region",        # Different colors per group
    size="gdp",     # Bubble size based on values
    hover_data=["gdp", "country"] # Additional info on mouse hover
)
fig.show()