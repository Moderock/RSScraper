
from YahooFinance import YahooFinance
from sklearn.linear_model import LinearRegression
import polars as pl


myYFA = YahooFinance('AZN.L')
# analysis = myYFA.Analysis(myYFA.headers, myYFA.ticker)
# analysis.get_data()
# print(analysis.growth_estimates)

# key_stats = myYFA.KeyStatistics(myYFA.headers, myYFA.ticker)
# key_stats.get_data()
# print(key_stats.cash_flow_statement)

cashflow = myYFA.CashFlow(myYFA.headers, myYFA.ticker)
cashflow.get_data()
free_cash_flow_row = cashflow.cash_flow.filter(pl.col("Breakdown") == "Free cash flow")
free_cash_flow = free_cash_flow_row.row(1)[2:6]
# free_cash_flow = ('6,567,000', '7,237,000', '3,763,000', '2,193,000')
values = [int(val.replace(',', '')) for val in free_cash_flow]

print(values)

years = list(range(len(values) - 1, -1, -1))  # Most recent year is 0

# 4. Create DataFrame
df = pl.DataFrame({'years': years, 'values': values})

# 5. Fit linear regression
model = LinearRegression()
model.fit(df[['years']], df['values'])

# 6. Generate predictions for future years
future_years = [[i] for i in range(len(values), len(values) + 5)]  # Next 3 years
forecasted_values = model.predict(future_years)

# 7. Print forecasted values
print("Forecasted values for the next 3 years:")
for year, value in zip(range(len(values), len(values) + 5), forecasted_values):
    print(f"Year {year}: {int(value)}")
