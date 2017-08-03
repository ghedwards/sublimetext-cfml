from CFML.syntaxes import cfml_syntax

def attribute(name, value_scope, name_scope=None, meta_scope=None):
    syntax = {
        'match': r'(?i:\b(?:%s)\b)' % name,
        'scope': 'entity.other.attribute-name.cfml' + (' ' + name_scope if name_scope else ''),
        'push': [
            {
                'match': '=',
                'scope': 'punctuation.separator.key-value.cfml',
                'set': [
                    cfml_syntax.attribute_value_string("'", "single", value_scope),
                    cfml_syntax.attribute_value_string('"', "double", value_scope),
                    cfml_syntax.attribute_value_unquoted(value_scope),
                    {
                        'include': 'else-pop'
                    }
                ]
            },
            {
                'include': 'else-pop'
            }
        ]
    }

    if meta_scope:
        syntax['push'] = [cfml_syntax.meta(meta_scope), syntax['push']]

    return cfml_syntax.order_output(syntax)
