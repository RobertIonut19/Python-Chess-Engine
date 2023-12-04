def validate_data(data, rules):
    errors = []

    for rule in rules:
        column_name = rule['column']
        data_type = rule['type']
        required = rule.get('required', False)

        for row in data:
            if required and column_name not in row:
                errors.append(f"Missing value in column '{column_name}' in row {row}")
            elif column_name in row:
                value = row[column_name]
                try:
                    if data_type == int:
                        int(value)  # Attempt to convert to int
                    elif data_type == float:
                        float(value)  # Attempt to convert to float
                    elif not isinstance(value, data_type):
                        raise ValueError()  # Trigger an exception for other types

                except ValueError:
                    errors.append(f"Invalid {data_type.__name__} value in column '{column_name}' in row {row}")


    return errors
