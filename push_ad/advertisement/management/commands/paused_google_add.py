import sys

from django.core.management import BaseCommand
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers


class Command(BaseCommand):
    help = 'Paused Ad Command'

    def handle(self, *args, **options):
        try:
            client = GoogleAdsClient.load_from_storage(version="v12")
            customer_id = ""
            ad_group_id = ""
            ad_id = ""
            operation = "Paused"
            # operation = "UnPaused"
            ad_group_ad_service = client.get_service("AdGroupAdService")
            ad_group_ad_operation = client.get_type("AdGroupAdOperation")
            ad_group_ad = ad_group_ad_operation.update
            ad_group_ad.resource_name = ad_group_ad_service.ad_group_ad_path(customer_id, ad_group_id, ad_id)
            ad_group_ad.status = client.enums.AdGroupStatusEnum.PAUSED if operation == "Paused" else client.enums.AdGroupStatusEnum.ENABLED
            client.copy_from(ad_group_ad_operation.update_mask, protobuf_helpers.field_mask(None, ad_group_ad._pb), )
            ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id,
                                                                           operations=[ad_group_ad_operation])
            self.stdout.write(
                self.style.SUCCESS(f"Paused ad group ad {ad_group_ad_response.results[0].resource_name}."))
        except GoogleAdsException as ex:
            self.stdout.write(self.style.ERROR(
                f'Request with ID "{ex.request_id}" failed with status "{ex.error.code().name}" and includes the following errors:'))
            for error in ex.failure.errors:
                self.stdout.write(self.style.ERROR(f'\tError with message "{error.message}".'))
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        self.stdout.write(self.style.ERROR(f"\t\tOn field: {field_path_element.field_name}"))
            sys.exit(1)
