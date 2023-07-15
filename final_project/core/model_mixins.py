class ChoicesEnumMixin:

    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]
#TODO this wont work for numbers, extend in another mixin
    @classmethod
    def max_type_length(cls):
        return max(len(name) for name, _ in cls.choices())