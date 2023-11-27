from csv_validator import csv_reader, validate_data

# Example CSV file and validation rules
csv_file_path = 'file.csv'
validation_rules = [
    {'column': 'Nume', 'type': str, 'required': True},
    {'column': 'Varsta', 'type': int},
    {'column': 'Email', 'type': str, 'required': True},
]

# Read CSV file
csv_data = csv_reader.read_csv(csv_file_path)

# Validate data
validation_errors = validate_data.validate_data(csv_data, validation_rules)

# Display validation errors
if validation_errors:
    print("Validation Errors:")
    for error in validation_errors:
        print(error)
else:
    print("Data is valid.")
