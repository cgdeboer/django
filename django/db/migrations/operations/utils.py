def is_referenced_by_foreign_key(state, model_name_lower, field, field_name):
    for state_app_label, state_model in state.models:
        for _, f in state.models[state_app_label, state_model].fields:
            if (f.related_model and
                    '%s.%s' % (state_app_label, model_name_lower) == f.related_model.lower() and
                    hasattr(f, 'to_fields')):
                if (f.to_fields[0] is None and field.primary_key) or field_name in f.to_fields:
                    return True
    return False


def verbose_describe(operation, backwards):
    if hasattr(operation, "code"):
        action = operation.code.__doc__ if backwards is not True else operation.reverse_code.__doc__
        prefix = ""
    elif hasattr(operation, "sql"):
        action = operation.sql if backwards is not True else operation.reverse_sql
        prefix = ""
    else:
        action = "No further Detail"
        prefix = "Undo "
    if action is None:
        error = True
        action = "IRREVERSIBLE"
    else:
        action = "{}".format(action.replace("\n", ""))
        error = False
    action = action if len(action) < 40 else '{}...'.format(action[:37])
    return '{}{} --> {}'.format(prefix, operation.describe(), action), error
