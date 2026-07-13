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
# fig.show()

fig.write_html("results\\gdp_vs_enrollement_scatter_gdp_scaled_points.html")
fig.write_image("results\\gdp_vs_enrollement_scatter_gdp_scaled_points.png")

fig2 = px.scatter(
    df_joined, 
    x="students5_estimated_sum", 
    y="gdp", 
    color="region",        # Different colors per group
    hover_data=["gdp", "country", "year"], # Additional info on mouse hover
    trendline="lowess"
)
fig2.data[1].visible = 'legendonly' # Hides trendline by default
# fig2.show()

fig2.write_html("results\\gdp_vs_enrollement_scatter_with_trends.html")
fig2.write_image("results\\gdp_vs_enrollement_scatter_with_trends.png")

df_agg_across_year = df_joined.groupby(['country']).\
        agg(students5_estimated_mean=('students5_estimated', 'mean'),
            students5_estimated_std=('students5_estimated', 'std'),
            students5_estimated_sum=('students5_estimated', 'sum')).reset_index()

test = df_joined.groupby("country")['students5_estimated_sum'].mean()
test2 = df_joined.groupby("country")['gdp'].mean()
fig3 = px.scatter(
    x=test2, 
    y=test, 
    # color="region",        # Different colors per group
    # hover_data=["gdp", "country", "year"], # Additional info on mouse hover
    # trendline="lowess"
)
# fig3.show()

fig3.write_html("results\\gdp_vs_enrollement_1_point_per_country.html")
fig3.write_image("results\\gdp_vs_enrollement_1_point_per_country.png")