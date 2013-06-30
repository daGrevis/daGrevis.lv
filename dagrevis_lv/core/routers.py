class DefaultRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label != "legacy":
            return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label != "legacy":
            return "default"

    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label != "legacy"
                and obj2._meta.app_label != "legacy"):
            return True

    def allow_syncdb(self, db, model):
        if model._meta.app_label != "legacy":
            return True
