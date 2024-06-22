class BankRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'ecoms' and model._meta.model_name == 'bank_customer':
            return 'bank'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'ecoms' and model._meta.model_name == 'bank_customer':
            return 'bank'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'ecoms' and obj1._meta.model_name == 'bank_customer' or \
           obj2._meta.app_label == 'ecoms' and obj2._meta.model_name == 'bank_customer':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'ecoms' and model_name == 'bank_customer':
            return db == 'bank'
        return None
    
    
    
