import requests
import pandas as pd
from bs4 import BeautifulSoup


class HTMLTableParser:

    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [(table, self.parse_html_table(table)) for table in soup.find_all('table')]

    def parse_html_table(self, table):
        n_columns = 0
        n_rows = 0
        columns_names = []

        for row in table.find_all('tr'):
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    n_columns = len(td_tags)

            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(columns_names) ==0:
                for th in th_tags:
                    columns_names.append(th.get_text())

        if len(columns_names) > 0 and len(columns_names) != n_columns:
            raise Exception('Column titles do not match the number of columns')

        columns = columns_names if len(columns_names) > 0 else range(0, n_columns)
        df = pd.DataFrame(columns=columns, index=range(0, n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_maker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker, column_maker] = column.get_text()
                column_maker += 1
            if len(columns) > 0:
                row_marker += 1

        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass

        return df