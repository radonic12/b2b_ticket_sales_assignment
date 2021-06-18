from datetime import datetime

def validate_string(input, file_name, file_type, column_name):
    try:
        str(input)
        return input
    except:
        raise ValueError(f'input={input} is not castable as string for file={file_name} of type={file_type} and column={column_name}. Error thrown at {datetime.now()}')

def validate_int(input, file_name, file_type, column_name):
    try:
        int(input)
        return input
    except:
        raise ValueError(f'input={input} is not castable as int for file={file_name} of type={file_type} and column={column_name}. Error thrown at {datetime.now()}')

def validate_float(input, file_name, file_type, column_name):
    try:
        float(input)
        return input
    except:
        raise ValueError(f'input={input} is not castable as float for file={file_name} of type={file_type} and column={column_name}. Error thrown at {datetime.now()}')

def validate_date(input, file_name, file_type, column_name):
    try:
        input = str(input)
        if len(input) == 7:
            input = f'0{input}'
        datetime.strptime(input, '%m%d%Y')
        return datetime.strptime(input, '%m%d%Y')
    except:
        raise ValueError(f'input={input} is not castable as date make sure the format is MMDDYYYY for file={file_name} of type={file_type} and column={column_name}. Error thrown at {datetime.now()}')