from django.core.management import BaseCommand
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers


class Command(BaseCommand):
    help = 'Advertisement Command'

    def handle(self, *args, **options):
        try:
            customer_id = ""
            ad_group_id = ""
            cpc_bid_micro_amount = ""
            client = GoogleAdsClient.load_from_storage(version="v12")
            ad_group_service = client.get_service("AdGroupService")
            ad_group_operation = client.get_type("AdGroupOperation")
            ad_group = ad_group_operation.update
            ad_group.resource_name = ad_group_service.ad_group_path(customer_id, ad_group_id)
            ad_group.status = client.enums.AdGroupStatusEnum.PAUSED
            ad_group.cpc_bid_micros = cpc_bid_micro_amount
            client.copy_from(ad_group_operation.update_mask, protobuf_helpers.field_mask(None, ad_group._pb), )
            # Update the ad group.
            ad_group_response = ad_group_service.mutate_ad_groups(customer_id=customer_id,
                                                                  operations=[ad_group_operation])
            self.stdout.write(self.style.SUCCESS(f"Updated ad group {ad_group_response.results[0].resource_name}."))
        except GoogleAdsException as ex:
            self.stdout.write(self.style.ERROR(
                f'Request with ID "{ex.request_id}" failed with status "{ex.error.code().name}" and includes the following errors:'))
            for error in ex.failure.errors:
                self.stdout.write(self.style.ERROR(f'\tError with message "{error.message}".'))
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        self.stdout.write(self.style.ERROR(f"\t\tOn field: {field_path_element.field_name}"))
            sys.exit(1)
