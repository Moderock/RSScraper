import requests
from bs4 import BeautifulSoup
import polars as pl


class YahooFinance:
    def __init__(self, ticker):
        self.ticker = ticker
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    class Analysis:
        def __init__(self, headers, ticker):
            self.url = f"https://uk.finance.yahoo.com/quote/{ticker}/"
            self.headers = headers
            self.earnings_estimate = None
            self.revenue_estimate = None
            self.earnings_history = None
            self.eps_trend = None
            self.eps_revisions = None
            self.growth_estimates = None

        def get_data(self):
            try:
                response = requests.get(self.url + 'analysis', headers=self.headers)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')
                tables = soup.find_all("table", {"class": "W(100%) M(0) BdB Bdc($seperatorColor) Mb(25px)"})
                for table in tables:
                    header = table.find_all('th')
                    # analysis
                    if header[0].text.strip() == "Earnings estimate":
                        self.earnings_estimate = self._add_to_df(header, table)
                    elif header[0].text.strip() == "Revenue estimate":
                        self.revenue_estimate = self._add_to_df(header, table)
                    elif header[0].text.strip() == "Earnings history":
                        self.earnings_history = self._add_to_df(header, table)
                    elif header[0].text.strip() == "EPS trend":
                        self.eps_trend = self._add_to_df(header, table)
                    elif header[0].text.strip() == "EPS revisions":
                        self.eps_revisions = self._add_to_df(header, table)
                    elif header[0].text.strip() == "Growth estimates":
                        self.growth_estimates = self._add_to_df(header, table)

            except Exception as e:
                print(f"{e}")

        def _add_to_df(self, header, table):
            data = []
            header_names = [h.text.strip() for h in header]
            for row in table.find_all('tr'):
                row_data = [td.text.strip() for td in row.find_all('td')]
                if row_data:
                    data.append(row_data)

            pl_df = pl.DataFrame(data, orient="row", schema=header_names)
            return pl_df

    class CashFlow:
        def __init__(self, headers, ticker):
            self.url = f"https://uk.finance.yahoo.com/quote/{ticker}/cash-flow"
            self.headers = headers
            self.cash_flow = None

        def get_data(self):
            try:
                response = requests.get(self.url, headers=self.headers)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Find the annual cash flow statement table using the updated structure
                main_div = soup.find("div", {"class": "W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)"})
                headings = main_div.find("div", {"class": "D(tbhg)"})
                headers = headings.find_all("span")
                header_names = [h.text.strip() for h in headers]

                body = main_div.find("div", {"class": "D(tbrg)"})
                details = body.find_all("div", {"class": "D(tbr)"})
                data = []
                for detail in details:
                    title =  detail.find("div", {"class": "Va(m)"}).text.strip()
                    values = [v.text.strip() for v in detail.find_all("div", {"class": "Ta(c)"})]
                    values.insert(0, title)
                    data.append(values)

                pl_df = pl.DataFrame(data, orient="row", schema=header_names)
                self.cash_flow = pl_df

            except (requests.exceptions.RequestException, AttributeError, IndexError) as e:
                print(f"Error fetching or parsing data: {e}")
                return None

    class KeyStatistics:
        def __init__(self, headers, ticker):
            self.url = f"https://uk.finance.yahoo.com/quote/{ticker}/key-statistics"
            self.headers = headers
            self.valuation_measures = None
            self.stock_price_history = None
            self.share_statistics = None
            self.dividends_splits = None
            self.fiscal_year = None
            self.profitability = None
            self.management_effectiveness = None
            self.income_statement = None
            self.balance_sheet = None
            self.cash_flow_statement = None

        def get_data(self):
            try:
                response = requests.get(self.url, headers=self.headers)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')
                tables = soup.find_all("table")

                for t, table in enumerate(tables):
                    data = []
                    for row in table.find_all('tr'):
                        row_data = [td.text.strip() for td in row.find_all('td')]
                        data.append(row_data)
                    pl_df = pl.DataFrame(data, orient="row")

                    if t == 0:
                        self.valuation_measures = pl_df
                    elif t == 1:
                        self.stock_price_history = pl_df
                    elif t == 2:
                        self.share_statistics = pl_df
                    elif t == 3:
                        self.dividends_splits = pl_df
                    elif t == 4:
                        self.fiscal_year = pl_df
                    elif t == 5:
                        self.profitability = pl_df
                    elif t == 6:
                        self.management_effectiveness = pl_df
                    elif t == 7:
                        self.income_statement = pl_df
                    elif t == 8:
                        self.balance_sheet = pl_df
                    elif t == 9:
                        self.cash_flow_statement = pl_df

            except (requests.exceptions.RequestException, AttributeError, IndexError) as e:
                print(f"Error fetching or parsing data: {e}")
                return None


