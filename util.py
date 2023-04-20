def get_limits(color):
    """
    Returns the lower and upper limits in the HSV color space for a given color.
    """
    if color == [0, 255, 255]:  # yellow
        return (20, 100, 100), (30, 255, 255)
    elif color == [0, 255, 0]:  # green
        return (40, 100, 100), (80, 255, 255)
    elif color == [0, 0, 255]:  # red
        return (0, 100, 100), (10, 255, 255)
    elif color == [255, 0, 0]:  # blue
        return (110, 100, 100), (130, 255, 255)
    else:
        return None
