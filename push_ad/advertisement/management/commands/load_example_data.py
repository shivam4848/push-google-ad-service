from django.core.management.base import BaseCommand
from google.cloud import bigquery

from advertisement.db_manager.bq_example_data import BQExampleDataDBManager
from push_ad.bq_utils import BQOperations


class Command(BaseCommand):
    help = 'Advertisement Command'

    def handle(self, *args, **options):
        bq_ops_obj = BQOperations()
        query = """SELECT * FROM `bigqueryroject-372608.test_datasetid.test_table` LIMIT 1000;"""
        data = bq_ops_obj.hit_bq_query(query, is_result_in_dict=True)
        db_manager = BQExampleDataDBManager()
        self.stdout.write(self.style.SUCCESS(f"Length of fetched data -> {len(data)}"))
        db_manager.create_in_bulk(data)
        self.stdout.write(self.style.SUCCESS('Successfully Done'))
