from advertisement.models import BQExampleData
from push_ad.base_db_magaer import BaseDBManager


class BQExampleDataDBManager(BaseDBManager):
    model = BQExampleData
    has_active_filter = False
