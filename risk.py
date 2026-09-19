from app.models.schemas import RiskRequest, RiskResponse

def calculate_position_size(req: RiskRequest) -> RiskResponse:
    risk_amount = req.equity * req.risk_fraction
    stop_distance = abs(req.entry - req.stop)
    units = risk_amount / (stop_distance * req.point_value) if stop_distance > 0 else 0.0
    return RiskResponse(
        risk_amount=round(risk_amount, 8),
        stop_distance=round(stop_distance, 8),
        units=round(units, 8),
        risk_fraction=req.risk_fraction,
    )
