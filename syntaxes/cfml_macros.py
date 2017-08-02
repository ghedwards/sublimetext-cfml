from YAMLMacros.lib.syntax import meta, expect, pop_on, stack

def attribute_string(char, scope, value_scope):
    return {
        'match': char,
        'scope': 'punctuation.definition.string.begin.cfml',
        'set': [
            {
                'meta_scope': 'meta.string.quoted.{scope}.cfml string.quoted.{scope}.cfml'.format(scope = scope)
            },
            {
                'meta_content_scope': value_scope
            },
            {
                'match': char * 2,
                'scope': 'constant.character.escape.quote.cfml',
            },
            {
                'match': char,
                'scope': 'punctuation.definition.string.end.cfml',
                'pop': True
            }
        ]
    }

def attribute(name, value_scope, name_scope=None, meta_scope=None):
    syntax = {
        'match': r'(?i:\b%s\b)' % name,
        'scope': 'entity.other.attribute-name.cfml' + (' ' + name_scope if name_scope else ''),
        'push': [
            {
                'match': '=',
                'scope': 'punctuation.separator.key-value.cfml',
                'set': [
                    attribute_string("'", "single", value_scope),
                    attribute_string('"', "double", value_scope),
                    {
                        'match': '(?=[^\s</>{;])',
                        'set': [
                            {
                                'meta_scope': 'meta.string.unquoted.cfml string.unquoted.cfml ' + value_scope
                            },
                            {
                                'match': '(?=[\s</>{;])',
                                'pop': True
                            }
                        ]
                    },
                    {
                        'match': '(?=\S)',
                        'pop': True
                    }
                ]
            },
            {
                'match': '(?=\S)',
                'pop': True
            }
        ]
    }

    if meta_scope:
        syntax['push'] = [meta(meta_scope), syntax['push']]

    return syntax
