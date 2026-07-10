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


        for value, subset in self.df.groupby('country'):
           print(subset['year']==2010, subset['year']==2000)

        fig2 = px.choropleth(
            self.df,
            locations="country",
            locationmode='country names',
            color="students5_estimated_sum",
        )
        fig2.show()


    def main(self):
        historyObj.test_print()
        historyObj.plot_line_chart()

if __name__ == "__main__":
    historyObj = HistoricalEventFinder(r'c:\Users\james\Documents\Repos\cbds-take-home\enrollments.csv')
    historyObj.main()