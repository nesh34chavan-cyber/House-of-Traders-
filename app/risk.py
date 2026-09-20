def calculate_position_size(
    equity: float,
    risk_fraction: float,
    entry: float,
    stop: float,
    point_value: float,
) -> dict:
    if equity <= 0:
        raise ValueError("equity must be positive")

    if risk_fraction <= 0 or risk_fraction > 0.10:
        raise ValueError(
            "risk_fraction must be between 0 and 0.10"
        )

    if entry <= 0 or stop <= 0:
        raise ValueError(
            "entry and stop must be positive"
        )

    if point_value <= 0:
        raise ValueError(
            "point_value must be positive"
        )

    risk_amount = equity * risk_fraction
    stop_distance = abs(entry - stop)

    if stop_distance == 0:
        raise ValueError(
            "entry and stop cannot be equal"
        )

    units = risk_amount / (
        stop_distance * point_value
    )

    return {
        "risk_amount": risk_amount,
        "stop_distance": stop_distance,
        "units": units,
        "risk_fraction": risk_fraction,
    }
