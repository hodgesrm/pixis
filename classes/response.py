from .parse import parse_dict


class Response:
    def __init__(self, dikt):
        allowed = ['description', 'headers', 'content',
                   'links', 'extensions']
        required = ['description']
        mappings = ['headers', 'content', 'links']

        d = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       mappings=mappings)

        self.description = d['description']
        self.headers = d['headers']
        self.content = d['content']
        self.links = d['links']
        self.extensions = d['extensions']
