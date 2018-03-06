class FooDBRouter(object): 
    def db_for_read(self, model, **hints):
        #"Point all operations on homepage models to 'foodb'"
        if model._meta.app_label == 'homepage':
            return 'foodb'
        return 'default'

    def db_for_write(self, model, **hints):
        #"Point all operations on homepage models to 'foodb'"
        if model._meta.app_label == 'homepage':
            return 'foodb'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        #"Allow any relation if a both models in homepage app"
        if obj1._meta.app_label == 'homepage' and obj2._meta.app_label == 'homepage':
            return True
        # Allow if neither is homepage app
        elif 'homepage' not in [obj1._meta.app_label, obj2._meta.app_label]: 
            return True
        return False
    
    def allow_syncdb(self, db, model):
        if db == 'foodb' or model._meta.app_label == "homepage":
            return False # we're not using syncdb on our legacy database
        else: # but all other models/databases are fine
            return True
