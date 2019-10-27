class StringMixin:

    @staticmethod
    def capitalize(string: str):
        # return string.capitalize()
        return string[0].upper() + string[1:].lower()
