def validate_rectangle_input(width, height):
    """Validate rectangle dimensions"""
    try:
        w = int(width)
        h = int(height)
        if w <= 0 or h <= 0:
            raise ValueError("Dimensions must be positive integers")
        return w, h
    except ValueError:
        raise ValueError("Invalid rectangle dimensions")

def validate_container_input(width, height):
    """Validate container dimensions"""
    try:
        w = int(width)
        h = int(height)
        if w <= 0 or h <= 0:
            raise ValueError("Container dimensions must be positive integers")
        return w, h
    except ValueError:
        raise ValueError("Invalid container dimensions")