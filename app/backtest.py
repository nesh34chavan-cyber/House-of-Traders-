from .schemas import BacktestResult, BacktestTrade, Candle


def run_sma_cross(
    candles: list[Candle],
    fast: int,
    slow: int,
    initial_equity: float,
    risk_fraction: float,
) -> BacktestResult:
    if fast >= slow:
        raise ValueError("fast period must be smaller than slow period")

    if len(candles) < slow + 2:
        return BacktestResult(
            trades=[],
            initial_equity=initial_equity,
            final_equity=initial_equity,
            return_pct=0.0,
            max_drawdown_pct=0.0,
            win_rate=0.0,
            profit_factor=0.0,
        )

    closes = [c.close for c in candles]

    equity = initial_equity
    peak_equity = equity
    max_drawdown = 0.0

    trades = []
    position = None

    def sma(values, period):
        return sum(values[-period:]) / period

    for i in range(slow, len(candles)):
        fast_now = sma(closes[: i + 1], fast)
        slow_now = sma(closes[: i + 1], slow)

        fast_prev = sma(closes[:i], fast)
        slow_prev = sma(closes[:i], slow)

        long_signal = (
            fast_prev <= slow_prev
            and fast_now > slow_now
        )

        short_signal = (
            fast_prev >= slow_prev
            and fast_now < slow_now
        )

        candle = candles[i]

        if position is None:
            if long_signal:
                position = {
                    "side": "LONG",
                    "entry": candle.close,
                    "entry_time": candle.timestamp,
                }

            elif short_signal:
                position = {
                    "side": "SHORT",
                    "entry": candle.close,
                    "entry_time": candle.timestamp,
                }

            continue

        should_exit = (
            position["side"] == "LONG" and short_signal
        ) or (
            position["side"] == "SHORT" and long_signal
        )

        if not should_exit:
            continue

        entry = position["entry"]
        exit_price = candle.close

        if position["side"] == "LONG":
            price_change = exit_price - entry
        else:
            price_change = entry - exit_price

        risk_amount = equity * risk_fraction
        stop_distance = abs(entry * 0.01)

        units = (
            risk_amount / stop_distance
            if stop_distance > 0
            else 0
        )

        pnl = price_change * units
        equity += pnl

        trades.append(
            BacktestTrade(
                entry_time=position["entry_time"],
                exit_time=candle.timestamp,
                side=position["side"],
                entry=entry,
                exit=exit_price,
                pnl=pnl,
            )
        )

        peak_equity = max(peak_equity, equity)

        drawdown = (
            (peak_equity - equity) / peak_equity
            if peak_equity > 0
            else 0
        )

        max_drawdown = max(max_drawdown, drawdown)

        position = None

    if position is not None:
        candle = candles[-1]

        entry = position["entry"]
        exit_price = candle.close

        if position["side"] == "LONG":
            price_change = exit_price - entry
        else:
            price_change = entry - exit_price

        risk_amount = equity * risk_fraction
        stop_distance = abs(entry * 0.01)

        units = (
            risk_amount / stop_distance
            if stop_distance > 0
            else 0
        )

        pnl = price_change * units
        equity += pnl

        trades.append(
            BacktestTrade(
                entry_time=position["entry_time"],
                exit_time=candle.timestamp,
                side=position["side"],
                entry=entry,
                exit=exit_price,
                pnl=pnl,
            )
        )

        peak_equity = max(peak_equity, equity)

        drawdown = (
            (peak_equity - equity) / peak_equity
            if peak_equity > 0
            else 0
        )

        max_drawdown = max(max_drawdown, drawdown)

    wins = [trade for trade in trades if trade.pnl > 0]
    gross_profit = sum(
        trade.pnl for trade in trades if trade.pnl > 0
    )
    gross_loss = abs(
        sum(trade.pnl for trade in trades if trade.pnl < 0)
    )

    win_rate = (
        len(wins) / len(trades)
        if trades
        else 0.0
    )

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else 0.0
    )

    return BacktestResult(
        trades=trades,
        initial_equity=initial_equity,
        final_equity=equity,
        return_pct=(
            (equity - initial_equity)
            / initial_equity
            * 100
        ),
        max_drawdown_pct=max_drawdown * 100,
        win_rate=win_rate,
        profit_factor=profit_factor,
      )
