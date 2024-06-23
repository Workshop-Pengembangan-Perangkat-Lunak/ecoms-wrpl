class DeliveryRouter:
    route_app_labels = {"delivery", "contenttypes"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read delivery and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "delivery_db"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write delivery and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "delivery_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the delivery or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the delivery and contenttypes apps only appear in the
        'delivery_db' database.
        """
        if app_label in self.route_app_labels:
            return db == "delivery_db"
        return None




