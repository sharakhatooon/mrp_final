import pandas as pd
import chardet

def detect_encoding(file):
    with open(file, "rb") as f:
        result = chardet.detect(f.read(5000))
    return result['encoding']

def read_csv_safely(file, usecols=None):
    encodings = ['utf-8', 'ISO-8859-1', 'windows-1252']
    for enc in encodings:
        try:
            return pd.read_csv(file, encoding=enc, usecols=usecols)
        except UnicodeDecodeError:
            continue
    print(f"Unable to read {file} due to encoding issues.")
    return None

# Load files
patients = read_csv_safely("files/patients.csv", usecols=["Id"])
encounters = read_csv_safely("files/encounters.csv", usecols=["Id", "PATIENT", "PROVIDER"])
providers = read_csv_safely("files/providers.csv", usecols=["Id"])
medications = read_csv_safely("files/medications.csv", usecols=["PATIENT", "ENCOUNTER"])
procedures = read_csv_safely("files/procedures.csv", usecols=["PATIENT", "ENCOUNTER"])
observations = read_csv_safely("files/observations.csv", usecols=["PATIENT", "ENCOUNTER"])
careplans = read_csv_safely("files/careplans.csv", usecols=["PATIENT", "ENCOUNTER"])
conditions = read_csv_safely("files/conditions.csv", usecols=["PATIENT", "ENCOUNTER"])
allergies = read_csv_safely("files/allergies.csv", usecols=["PATIENT", "ENCOUNTER"])

def check_fk(table_name, fk_column, fk_values, pk_column, pk_values):
    if fk_values is None or pk_values is None:
        print(f"Skipping {table_name}: Data not loaded properly.")
        return
    
    missing_fk = fk_values[~fk_values.isin(pk_values)]
    if not missing_fk.empty:
        print(f"{table_name}: {fk_column} contains {len(missing_fk)} missing references to {pk_column}.")
    else:
        print(f"{table_name}: {fk_column} is valid.")

def check_nulls(table, table_name):
    null_counts = table.isnull().sum()
    null_columns = null_counts[null_counts > 0]
    if not null_columns.empty:
        print(f"{table_name}: Null values found in columns {null_columns.to_dict()}")
    else:
        print(f"{table_name}: No null values detected.")

def check_duplicates(table, table_name, pk_column):
    if table.duplicated(subset=[pk_column]).sum() > 0:
        print(f"{table_name}: Duplicate values found in {pk_column}.")
    else:
        print(f"{table_name}: No duplicates in {pk_column}.")

def check_data_types(table, table_name, id_columns):
    for col in id_columns:
        if not table[col].astype(str).str.match(r'^[A-Za-z0-9\-]+$').all():
            print(f"{table_name}: {col} contains invalid characters.")

# Perform checks
tables = {
    "patients": (patients, "Id"),
    "encounters": (encounters, "Id"),
    "providers": (providers, "Id"),
    "medications": (medications, None),
    "procedures": (procedures, None),
    "observations": (observations, None),
    "careplans": (careplans, None),
    "conditions": (conditions, None),
    "allergies": (allergies, None),
}

for table_name, (table, pk_column) in tables.items():
    if table is not None:
        print(f"Checking {table_name} ({len(table)} rows)...")
        check_nulls(table, table_name)
        if pk_column:
            check_duplicates(table, table_name, pk_column)
            check_data_types(table, table_name, [pk_column])

# Foreign Key Validations
check_fk("encounters", "PATIENT", encounters["PATIENT"], "Id", patients["Id"])
check_fk("encounters", "PROVIDER", encounters["PROVIDER"], "Id", providers["Id"])
check_fk("medications", "PATIENT", medications["PATIENT"], "Id", patients["Id"])
check_fk("medications", "ENCOUNTER", medications["ENCOUNTER"], "Id", encounters["Id"])
check_fk("procedures", "PATIENT", procedures["PATIENT"], "Id", patients["Id"])
check_fk("procedures", "ENCOUNTER", procedures["ENCOUNTER"], "Id", encounters["Id"])
check_fk("observations", "PATIENT", observations["PATIENT"], "Id", patients["Id"])
check_fk("observations", "ENCOUNTER", observations["ENCOUNTER"], "Id", encounters["Id"])
check_fk("careplans", "PATIENT", careplans["PATIENT"], "Id", patients["Id"])
check_fk("careplans", "ENCOUNTER", careplans["ENCOUNTER"], "Id", encounters["Id"])
check_fk("conditions", "PATIENT", conditions["PATIENT"], "Id", patients["Id"])
check_fk("conditions", "ENCOUNTER", conditions["ENCOUNTER"], "Id", encounters["Id"])
check_fk("allergies", "PATIENT", allergies["PATIENT"], "Id", patients["Id"])
check_fk("allergies", "ENCOUNTER", allergies["ENCOUNTER"], "Id", encounters["Id"])
