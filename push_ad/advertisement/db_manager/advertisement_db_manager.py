from advertisement.models import Advertisement
from push_ad.base_db_magaer import BaseDBManager


class AdvertisementDBManager(BaseDBManager):
    model = Advertisement
    has_active_filter = False
