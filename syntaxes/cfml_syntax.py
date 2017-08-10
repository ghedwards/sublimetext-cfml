import sublime
from ruamel.yaml.comments import CommentedMap

ORDERED_KEYS = ['meta_scope', 'meta_content_scope', 'match', 'scope', 'captures', 'push', 'set', 'pop']

def order_output(syntax):
    if isinstance(syntax, dict):
        ordered_syntax = CommentedMap()
        for key in ORDERED_KEYS:
            if key in syntax:
                ordered_syntax[key] = order_output(syntax[key])
        for key in syntax:
            if key not in ORDERED_KEYS:
                ordered_syntax[key] = order_output(syntax[key])
        return ordered_syntax
    if isinstance(syntax, list):
        return [order_output(item) for item in syntax]
    return syntax

def attribute_value_string(char, scope, value_scope):
    syntax = {
        'match': char,
        'scope': 'punctuation.definition.string.begin.cfml',
        'set': [
            [
                {
                    'meta_scope': 'meta.string.quoted.{scope}.cfml string.quoted.{scope}.cfml'.format(scope = scope)
                },
                {
                    'match': char,
                    'scope': 'punctuation.definition.string.end.cfml',
                    'pop': True
                }
            ]
        ]
    }

    if '.' in value_scope and 'scope:' not in value_scope:
        # we have a scope name
        syntax['set'].append([
            {
                'meta_content_scope': value_scope
            },
            {
                'match': char * 2,
                'scope': 'constant.character.escape.quote.cfml',
            },
            {
                'match': r'(?=%s)' % char,
                'pop': True
            }
        ])
    else:
        # this is a context
        syntax['set'].append([
            {'include': value_scope},
            {'include': 'else-pop'}
        ])

    return syntax

def attribute_value_unquoted(value_scope):
    syntax = {
        'match': r'(?=[A-Za-z0-9\-_.$])',
        'set': [
            meta('meta.string.unquoted.cfml string.unquoted.cfml')
        ]
    }

    if '.' in value_scope and 'scope:' not in value_scope:
        # we have a scope name
        syntax['set'].append([
            {
                'meta_scope': value_scope
            },
            {
                'match': r'(?=[^A-Za-z0-9\-_.$])',
                'pop': True
            }
        ])
    else:
        # this is a context
        syntax['set'].append([
            {'include': value_scope},
            {'include': 'else-pop'}
        ])

    return syntax


def load_tag_list():
    tags_to_filter = [
        'abort',
        'admin',
        'case',
        'catch',
        'component',
        'continue',
        'defaultcase',
        'else',
        'elseif',
        'exit',
        'finally',
        'function',
        'if',
        'interface',
        'rethrow',
        'retry',
        'return',
        'script',
        'servlet',
        'servletparam',
        'set',
        'sleep',
        'switch',
        'try',
        'while'
    ]
    tags = sublime.load_resource("Packages/CFML/src/basecompletions/json/cfml_tags.json")
    tags = sublime.decode_value(tags).keys()
    return [t.lower()[2:] for t in tags if t not in tags_to_filter]
