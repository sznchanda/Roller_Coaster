# Project: Roller Coaster Graph build by Steeve Nchanda

# Step 1: Preset all the Required Libraries 
import pandas as pd
import sys
from sympy import sympify, symbols, pi, plotting

# Step 2: Asking the user to enter the csv input file name and define the svg output file name
roller_coaster_formula_file = input("Enter with the extension '.csv' file that contains your roller coaster formula  ")
roller_coaster_file_name = input("Enter with the extension '.svg' file name you want your roller coaster image to be saved in  ")

# Step 3: Read and Validate CSV:  Use pandas to read the CSV file and validate its contents according to the specified criteria.
def read_and_validate_csv(formula_file):
    try:
        # 1. Check for Empty CSV
        df = pd.read_csv(formula_file)
        if df.empty:
            print("Error: Empty CSV file.")
            sys.exit(1)

        # 2. Check for Invalid CSV Format
        # (Pandas will raise ParserError if the CSV format is invalid)

        # 3. Verify Required Columns
        required_columns = ['formula', 'start_x', 'end_x']
        for column in required_columns:
            if column not in df.columns:
                print(f"Error: '{column}' column is missing.")
                sys.exit(1)

        # 4. Validate 'formula' Column
        for formula in df['formula']:
            if not is_valid_formula(formula):
                print(f"Error: Invalid formula - {formula}")
                sys.exit(1)

        # 5. Validate 'start_x' and 'end_x' Columns
        for _, row in df.iterrows():
            validate_x_value(row['start_x'])
            validate_x_value(row['end_x'])

        # 6. Validate Additional Columns (Optional)
        # Additional columns can be ignored

        return df
    
    except pd.errors.ParserError:
        print("Error: Invalid CSV format.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def is_valid_formula(formula):
    try:
        x = symbols('x')
        sympify(formula, locals={'x': x})
        return True
    except:
        return False

# Step 4: Define Helper Functions: Create functions to: Check if a formula is valid using sympy. 
#         Verify if the ending value of x is larger than the starting value.
#         Ensure the starting value of x in each row matches the ending value in the previous row. 
#         Check if formulas meet at the same location for a smooth transition.
def validate_x_value(x_value):
    try:
        # Check if x_value can be interpreted as a number
        float(x_value)
    except ValueError:
        try:
            # Check if x_value can be interpreted as a symbolic expression
            sympify(x_value)
        except:
            print(f"Error: Invalid value for 'x'. Must be a number or a valid expression - {x_value}")
            sys.exit(1)

def validate_formula_column(df):
    if 'formula' not in df.columns:
        print("Error: 'formula' column is missing.")
        sys.exit(1)

    for formula in df['formula']:
        if not is_valid_formula(formula):
            print(f"Error: Invalid formula - {formula}")
            sys.exit(1)


def validate_x_values(df):
    for i, row in df.iterrows():
        start_x, end_x = row['start_x'], row['end_x']

        # Convert 'start_x' and 'end_x' to numeric values using sympify
        start_x_numeric = float(sympify(start_x))
        end_x_numeric = float(sympify(end_x))

        print(f"Row {i + 1}: start_x = {start_x_numeric}, end_x = {end_x_numeric}")

        if not start_x_numeric < end_x_numeric:
            print(f"Error: Ending value of x must be larger than the starting value. Row {i + 1}: {row}")
            sys.exit(1)


def validate_continuity(df):
    for i in range(1, len(df)):
        current_start_x = df.iloc[i]['start_x']
        previous_end_x = df.iloc[i-1]['end_x']

        # Convert 'current_start_x' and 'previous_end_x' to numeric values using sympify
        current_start_x_numeric = float(sympify(current_start_x))
        previous_end_x_numeric = float(sympify(previous_end_x))

        if current_start_x_numeric != previous_end_x_numeric:
            print("Error: Starting value of x in each row must match the ending value of x in the previous row.")
            sys.exit(1)


def validate_smooth_transition(df):
    for i in range(1, len(df)):
        formula1, formula2 = sympify(df.iloc[i-1]['formula']), sympify(df.iloc[i]['formula'])
        start_x, end_x = sympify(df.iloc[i-1]['end_x']), sympify(df.iloc[i]['start_x'])
        x = symbols('x')
        point1 = formula1.subs(x, end_x)
        point2 = formula2.subs(x, start_x)
        if point1 != point2:
            print("Error: Formulas do not meet at the same location for a smooth transition.")
            sys.exit(1)


def validate_csv(df):
    validate_formula_column(df)
    validate_x_values(df)
    validate_continuity(df)
    validate_smooth_transition(df)

roller_coaster_df = read_and_validate_csv(roller_coaster_formula_file)
validate_csv(roller_coaster_df)

# Step 5: Generate Roller Coaster Shape: Use sympy to evaluate formulas and generate the roller coaster shape.
def generate_roller_coaster_shape(df):
    x = symbols('x')
    plt1 = None

    for index, row in df.iterrows():
        formula = sympify(row['formula'])  
        start_x = float(sympify(row['start_x']))
        end_x = float(sympify(row['end_x']))
        if index == 0:
            plt1 = plotting.plot(formula, (x, start_x, end_x), show = False)
        else:
            plt2 = plotting.plot(formula, (x, start_x, end_x), show = False)
            plt1.append(plt2[0])
    plt1.save(roller_coaster_file_name)
    plt1.show()


roller_coaster_shape = generate_roller_coaster_shape(roller_coaster_df)
