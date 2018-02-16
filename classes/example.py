class Example:
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['summary', 'description', 'value',
                   'externalValue', 'extensions']

        d = parse_dict(dikt=dikt, allowed=allowed)

        self.summary = d['summary']
        self.description = d['description']
        self.value = d['value']
        self.externalValue = d['externalValue']
        self.extensions = d['extensions']
