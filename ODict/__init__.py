import sys


class ODict(object):
    def __init__(self, d):
        d = self.parse_dict(d)
        self.__dict__ = d

    def parse_dict(self, d):
        if isinstance(d, dict):
            result = {}
            for key, item in d.items():
                if isinstance(item, list):
                    d[key] = self.parse_list(item)
                if isinstance(item, dict):
                    d[key] = ODict(item)

        return d

    def parse_list(self, d):
        result = []
        for item in d:
            if isinstance(item, dict):
                result.append(ODict(item))
            else:
                result.append(item)
        return result


sys.modules[__name__] = ODict
