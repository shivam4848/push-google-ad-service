import os

from django.core.management.base import BaseCommand
from google.cloud import bigquery

from advertisement.db_manager.bq_example_data import BQExampleDataDBManager

SERVICE_ACCOUNT_JSON = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
bucket_name = 'push_bq_bucket'
project = 'bigqueryroject-372608'
dataset_id = "test_datasetid"
table_id = "test_table"
destination_uri = "gs://{}/{}".format(bucket_name, "extracted_stories_data.csv")


class Command(BaseCommand):
    help = 'Advertisement Command'

    def handle(self, *args, **options):
        client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
        query = """SELECT * FROM `bigqueryroject-372608.test_datasetid.test_table` LIMIT 1000;"""
        self.stdout.write(self.style.SUCCESS(f"Query -> {query}"))
        df = client.query(query).to_dataframe()
        data = df.to_dict("records")
        db_manager = BQExampleDataDBManager()
        self.stdout.write(self.style.SUCCESS(f"Length of fetched data -> {len(data)}"))
        db_manager.create_in_bulk(data)
        self.stdout.write(self.style.SUCCESS('Successfully Done'))
