class ResponseNormalizer:

    DEFAULTS = {

        "html": "",

        "css": "",

        "js": ""

    }

    @classmethod
    def normalize(cls, data):

        result = cls.DEFAULTS.copy()

        result.update(data)

        return result