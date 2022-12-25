from collections import namedtuple

from django.db import connection


class BaseDBManager:
    model = None
    has_active_filter = True

    @staticmethod
    def namedtuplefetchall(cursor):
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]

    @staticmethod
    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()]

    def get_object(self, **filters):
        if "active" not in filters and self.has_active_filter:
            filters["active"] = True

        try:
            obj = self.model.objects.get(**filters)
            print(f"{self.model} found : %s" % obj)
            return obj
        except self.model.DoesNotExist:
            print(f"{self.model} not found in DB")
            return None
        except Exception as e:
            print(e)
            return None

    def get_object_without_active_check(self, **filters):
        try:
            obj = self.model.objects.get(**filters)
            print(f"{self.model} found : %s" % obj)
            return obj
        except self.model.DoesNotExist:
            print(f"{self.model} not found in DB")
            return None
        except Exception as e:
            print(e)
            return None

    def get_object_by_id(self, obj_id):

        print(f"Get {self.model} by id, id: {obj_id}")
        return self.model.objects.get(id=obj_id)

    def list_objects(self, apply_default_active_filter=True, select_for_update=False, get_first=False, q=None,
                     **filters):
        if "active" not in filters and self.has_active_filter and apply_default_active_filter:
            filters["active"] = True

        if select_for_update:
            objs = self.model.objects.select_for_update().filter(**filters)
        elif q:
            objs = self.model.objects.filter(q)
        else:
            objs = self.model.objects.filter(**filters)

        print(f"{self.model} objects found: {objs}")
        if not objs.exists():
            return objs
        elif objs.count() == 1 and get_first:
            return objs.first()
        else:
            return objs

    def create_object(self, **data):
        obj = self.model.objects.create(**data)
        print(f"Create {self.model} {obj}")
        return obj

    def update_objects(self, updates, query):
        query.update(**updates)
        return

    def bulk_update_obj(self, obj, **updates):
        for key, value in updates.items():
            setattr(obj, key, value)
        obj.save()

    def update_object_by_id(self, obj_id, **updates):
        query = self.model.objects.filter(id=obj_id)
        query.update(**updates)
        return query.first()

    def update_object_by_bulk_ids(self, obj_ids, **updates):
        query = self.model.objects.filter(id__in=obj_ids)
        query.update(**updates)
        return query.first()

    def create_in_bulk(self, data, batch_size=300):
        """
        data: List of dictionaries
        """
        payload = [self.model(**vals) for vals in data]
        obj = self.model.objects.bulk_create(payload, batch_size=batch_size)
        print(f"Bulk Create {self.model} {obj}")
        return obj

    def get_or_create(self, defaults={}, **data):
        obj, flag = self.model.objects.get_or_create(**data, defaults=defaults)
        print(f"Get or Create {self.model} {obj}")
        return obj

    def execute_query(self, query):

        objs = self.model.objects.raw(query)

        return objs

    def execute_query_through_cursor(self, query):
        results = []
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = dictfetchall(cursor)
        return results

    def execute_query_through_cursor_named_tuple(self, query):
        results = []
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = self.namedtuplefetchall(cursor)
        return results

    def execute_query_through_cursor_with_params(self, query, params):
        results = []
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = self.namedtuplefetchall(cursor)
        return results

    def execute_query_through_cursor_with_dict_params(self, query, params):
        results = []
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = self.dictfetchall(cursor)
        return results
