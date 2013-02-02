class LegacyRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "legacy":
            return "legacy"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "legacy":
            return "legacy"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return False

    def allow_syncdb(self, db, model):
        return False
