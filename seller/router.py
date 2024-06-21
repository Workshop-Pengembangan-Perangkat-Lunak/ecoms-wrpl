class SellerRouter:
    route_app_labels = {"seller", "contenttypes"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read seller and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "seller_db"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write seller and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "seller_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the seller or contenttypes apps is
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
        Make sure the seller and contenttypes apps only appear in the
        'seller_db' database.
        """
        if app_label in self.route_app_labels:
            return db == "seller_db"
        return None




