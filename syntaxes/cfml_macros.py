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


def function_call_params(meta_scope, named_param_scope, delimiter_scope):
    syntax = {
        'match': r'\(',
        'scope': 'punctuation.section.group.begin.cfml',
        'set': [
            {
                'meta_scope': meta_scope
            },
            {
                'match': r'\)',
                'scope': 'punctuation.section.group.end.cfml',
                'pop': True
            },
            {
                'match': ',',
                'scope': delimiter_scope
            },
            {
                'match': r'\b({{identifier}})\s*(=)(?!=)',
                'captures': {
                    '1': named_param_scope,
                    '2': 'keyword.operator.assignment.cfml'
                },
                'push': 'expression-no-comma'
            },
            {
                'match': r'(?=\S)',
                'push': 'expression-no-comma'
            }
        ]
    }

    return cfml_syntax.order_output(syntax)
