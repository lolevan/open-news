class MyMixin(object):
    mixin_pro = ''

    def get_prop(self):
        return self.mixin_pro.upper()

    @staticmethod
    def get_upper(s):
        if isinstance(s, str):
            return s.upper()
        else:
            return s.title.upper()
