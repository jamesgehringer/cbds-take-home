import pandas as pd
import plotly.express as px

class HistoricalEventFinder:

    def __init__(self, file):
        self.df = pd.read_csv(file)
        
        # Drop rows with missing data in column: 'students5_estimated'
        self.df = self.df.dropna(subset=['students5_estimated'])

        # Performed 3 aggregations grouped on columns: 'country', 'year'
        self.df = self.df.groupby(['country', 'year']).\
            agg(students5_estimated_mean=('students5_estimated', 'mean'),
                students5_estimated_std=('students5_estimated', 'std'),
                students5_estimated_sum=('students5_estimated', 'sum')).reset_index()

    def test_print(self):
        print(self.df)

    def plot_line_chart(self):
        fig = px.line(
                self.df, 
                x="year", 
                y="students5_estimated_sum", 
                color="country", # Creates a separate line for each unique value in this column
                title="Line Graph Separated by Column Values"
            )

                # Add a vertical shaded block between X-coordinates 2 and 3
        fig.add_vrect(
            x0=2000, x1=2010, 
            fillcolor="red", 
            opacity=0.5, 
            layer="below", 
            line_width=0
        )

        # 4. Display the chart
        fig.show()

        change_during_event = pd.DataFrame(columns=["country", "rate_of_change"])
        for value, subset in self.df.groupby('country'):
            try:
                print(subset["country"].iloc[0], subset.query("year == 2010")['students5_estimated_sum'].iloc[0]-subset.query("year == 2000")['students5_estimated_sum'].iloc[0])
                rate = subset.query("year == 2010")['students5_estimated_sum'].iloc[0]-subset.query("year == 2000")['students5_estimated_sum'].iloc[0]
                new_row = pd.DataFrame([{'country':subset["country"].iloc[0], 'rate_of_change':rate.astype('float64')}])
                change_during_event = pd.concat([change_during_event, new_row], ignore_index=True)
            except IndexError:
                print(f"{subset["country"].iloc[0]} does not have enough data")
        
        change_during_event['rate_of_change'] = pd.to_numeric(change_during_event['rate_of_change'], errors='coerce')
        
        fig2 = px.choropleth(
            change_during_event,
            locations="country",
            locationmode='country names',
            color="rate_of_change",
            color_continuous_scale="Viridis",
            range_color=(0, 6000000),
        )
        fig2.show()


    def main(self):
        historyObj.test_print()
        historyObj.plot_line_chart()

if __name__ == "__main__":
    historyObj = HistoricalEventFinder(r'c:\Users\james\Documents\Repos\cbds-take-home\enrollments.csv')
    historyObj.main()