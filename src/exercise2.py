import pandas as pd
import plotly.express as px


df_enrollement = pd.read_csv(r'data\enrollments.csv')
df_gdp = pd.read_csv(r'data\Countries GDP 1960-2020.csv')

# To combine these two datasets, we need the gdp data years in rows not columns
df_gdp = df_gdp.melt(id_vars=["Country Name", "Country Code"],
            var_name="year",
            value_name="gdp").sort_values(by='Country Name').reset_index()
# Make sure to set it to a numeric so it matches the enrollment data
df_gdp["year"] = df_gdp["year"].astype('float64')

# To join, we are just going to merge by year and country code
#  I almost did country name, but there would have been some extra steps that country code seemed to account for
#  This will also only join the data for the years that are in the enrollment data
df_joined = pd.merge(df_enrollement, df_gdp, left_on=["year", "countrycode"], right_on=["year", "Country Code"])

# Made a per coutry sum of enrollment numbers, similar to the other code
df_agg = df_joined.groupby(['country', 'year']).\
        agg(students5_estimated_mean=('students5_estimated', 'mean'),
            students5_estimated_std=('students5_estimated', 'std'),
            students5_estimated_sum=('students5_estimated', 'sum')).reset_index()

# Joining it back in so we have the sums with the gdp data
df_joined = pd.merge(df_joined, df_agg, on=["country", "year"])

# Made an inital plot of enrollment by year, with the points scaled by gdp, splitting up by region, based on some of what I saw on the world map
fig = px.scatter(
    df_joined, 
    x="year", 
    y="students5_estimated_sum", 
    color="region",        # Different colors per group
    size="gdp",     # Bubble size based on values
    hover_data=["gdp", "country"] # Additional info on mouse hover
)
# fig.show()

# Save the figures
fig.write_html("results\\gdp_vs_enrollement_scatter_gdp_scaled_points.html")
fig.write_image("results\\gdp_vs_enrollement_scatter_gdp_scaled_points.png", width=1200, height=800, scale=2)

# Plotting by year and scaling by gdp didn't quite get after the question
# Plotting here just by enrollment by gdp
# Later, I split by region again after noticing the potential trends
fig2 = px.scatter(
    df_joined, 
    x="students5_estimated_sum", 
    y="gdp", 
    color="region",        # Different colors per group
    hover_data=["gdp", "country", "year"], # Additional info on mouse hover
    trendline="lowess"
)

# fig2.show()

# Save the figures
fig2.write_html("results\\gdp_vs_enrollement_scatter_with_trends.html")
fig2.write_image("results\\gdp_vs_enrollement_scatter_with_trends.png", width=1200, height=800, scale=2)

# Did a final test and collapsed across year
df_agg_across_year = df_joined.groupby(['country']).\
        agg(students5_estimated_mean=('students5_estimated', 'mean'),
            students5_estimated_std=('students5_estimated', 'std'),
            students5_estimated_sum=('students5_estimated', 'sum')).reset_index()

# Pulled out just the columns I needed for this quick test and averaged 1 value per country
test = df_joined.groupby("country")['students5_estimated_sum'].mean()
test2 = df_joined.groupby("country")['gdp'].mean()

# Plotted with gdp data averaged across years
fig3 = px.scatter(
    x=test2, 
    y=test, 
    # color="region",        # Different colors per group
    # hover_data=["gdp", "country", "year"], # Additional info on mouse hover
    # trendline="lowess"
)
# fig3.show()

fig3.write_html("results\\gdp_vs_enrollement_1_point_per_country.html")
fig3.write_image("results\\gdp_vs_enrollement_1_point_per_country.png", width=1200, height=800, scale=2)