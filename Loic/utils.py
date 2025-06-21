def validate_input(value, field_name):
    try:
        num = float(value)
        if num <= 0:
            raise ValueError(f"{field_name} must be a positive number")
        return num
    except ValueError:
        raise ValueError(f"Invalid value for {field_name}. Please enter a valid positive number")

def format_bins(bins):
    return "\n".join(f"Bin {i+1}: {bin} (Total: {sum(bin)})" for i, bin in enumerate(bins))