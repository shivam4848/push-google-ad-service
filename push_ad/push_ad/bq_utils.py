import os

from google.cloud import bigquery


class BQOperations:

    def __init__(self, table_id=None):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), 'push_ad', 'creds_json', 'BQ.json')
        self.client = bigquery.Client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
        self.table_id = table_id

    def hit_bq_query(self, query, is_result_in_dict=False):
        df = self.client.query(query).to_dataframe()
        return df.to_dict("records") if is_result_in_dict else df

    def get_list_data_from_table(self, query):
        pass

    def insert_data_from_table(self, rows_to_insert):
        errors = self.client.insert_rows_json(self.table_id, rows_to_insert, row_ids=[None] * len(rows_to_insert))
        if not errors == []:
            print("New rows have been added.")
        else:
            raise ("Encountered errors while inserting rows: {}".format(errors))
