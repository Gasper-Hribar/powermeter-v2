def bound_min_max(value: float, min_value: float, max_value: float) -> float:
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    return value