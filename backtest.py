def run_sma_cross(candles, fast, slow, initial_equity, risk_fraction):
    if len(candles) < slow + 2:
        return {"trades": [], "initial_equity": initial_equity, "final_equity": initial_equity,
                "return_pct": 0, "max_drawdown_pct": 0, "win_rate": 0, "profit_factor": 0}
    eq, peak, maxdd = initial_equity, initial_equity, 0.0
    trades, side, entry = [], None, None
    closes = [c.close for c in candles]

    def sma(i, n):
        return sum(closes[i-n+1:i+1]) / n

    gross_win = gross_loss = 0.0
    for i in range(slow, len(candles)):
        f0, f1 = sma(i-1, fast), sma(i, fast)
        s0, s1 = sma(i-1, slow), sma(i, slow)
        sig = "LONG" if f0 <= s0 and f1 > s1 else "SHORT" if f0 >= s0 and f1 < s1 else None
        if sig and side and sig != side:
            pnl = candles[i].close - entry if side == "LONG" else entry - candles[i].close
            trades.append({"entry_time": candles[i-1].timestamp, "exit_time": candles[i].timestamp,
                           "side": side, "entry": entry, "exit": candles[i].close, "pnl": pnl})
            eq += pnl
            gross_win += max(pnl, 0)
            gross_loss += max(-pnl, 0)
            side = None
        if sig and side is None:
            side, entry = sig, candles[i].close
        peak = max(peak, eq)
        maxdd = max(maxdd, (peak-eq)/peak*100)

    if side:
        pnl = candles[-1].close-entry if side == "LONG" else entry-candles[-1].close
        trades.append({"entry_time": candles[-2].timestamp, "exit_time": candles[-1].timestamp,
                       "side": side, "entry": entry, "exit": candles[-1].close, "pnl": pnl})
        eq += pnl
        gross_win += max(pnl, 0)
        gross_loss += max(-pnl, 0)

    wins = sum(t["pnl"] > 0 for t in trades)
    return {"trades": trades, "initial_equity": initial_equity, "final_equity": eq,
            "return_pct": (eq/initial_equity-1)*100, "max_drawdown_pct": maxdd,
            "win_rate": wins/len(trades) if trades else 0,
            "profit_factor": gross_win/gross_loss if gross_loss else 0}
