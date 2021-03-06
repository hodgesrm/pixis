import collections  # for OrderedDict
import os

import jinja2

from pixis.config import Config
from pixis.template_context import TEMPLATE_CONTEXT

"""
entrypoints into our code generation, for us and users
"""

iterators_mapping = collections.OrderedDict()
iterator_functions_mapping = collections.OrderedDict()


def stage_iterator(x_iterator, x_iterator_functions):
    iterator_name = x_iterator.__name__
    iterators_mapping[iterator_name] = x_iterator
    iterator_functions_mapping[iterator_name] = x_iterator_functions


def emit_template(template_path, output_dir, output_name):
    try:
        # check for their custom templates
        template_name = template_path.split('/')[-1]
        template_loader = jinja2.FileSystemLoader(os.getcwd() + os.path.sep + Config.TEMPLATES)
        env = jinja2.Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=True, line_comment_prefix='//*')
        template = env.get_template(template_name)  # template_path is something like: flask_server/model.j2, so we have to do a name comparison here
        print("outputed file \" " + output_name + " \" from user defined template")
    except jinja2.exceptions.TemplateNotFound:
        # check for template in our package
        try:
            template_loader = jinja2.PackageLoader('pixis', 'templates')
            env = jinja2.Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=True, line_comment_prefix='//*')
            template = env.get_template(template_path)
        except jinja2.exceptions.TemplateNotFound as err:
            raise ValueError('Template does not exist\n' + err)

    env.globals['cfg'] = Config

    output_dir.mkdir(parents=True, exist_ok=True) 
    
    output_file = output_dir / output_name

    # directory = os.path.dirname(output_file)
    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    with output_file.open('w') as outfile:
        outfile.write(template.render(TEMPLATE_CONTEXT))


def run_iterators():
    # run each iterator once
    for iterator_name, iterator in iterators_mapping.items():
        iterator(iterator_functions_mapping[iterator_name])


def invocation_iterator(invocation_iterator_functions):
    for f in invocation_iterator_functions:
        f()


def specification_iterator(specification_iterator_functions):
    for f in specification_iterator_functions:
        f()


def schemas_iterator(schemas_iterator_functions):
    for schema_name, schema in TEMPLATE_CONTEXT['schemas'].items():
        TEMPLATE_CONTEXT['_current_schema'] = schema_name
        for f in schemas_iterator_functions:
            f()


def paths_iterator(paths_iterator_functions):
    for tag, paths in TEMPLATE_CONTEXT['paths'].items():
        TEMPLATE_CONTEXT['_current_tag'] = tag
        for f in paths_iterator_functions:
            f()
