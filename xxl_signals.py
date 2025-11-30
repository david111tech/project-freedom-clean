class XXLSignals:
    def compute_signal_confidence(self, ema_fast, ema_slow, atr, volatility_score):
        """Master weighting of signal confidence."""
        trend_strength = abs(ema_fast - ema_slow)
        confidence = trend_strength / (atr + 1e-6)

        confidence *= (1 + volatility_score)  # dynamic weighting

        return max(0.0, min(confidence, 1.0))

    def should_launch(self, state: "XXLState"):
        return (
            state.signal_confidence > 0.65 and
            not state.cooldown_active
        )

    def should_exit(self, ema_fast, ema_slow):
        return ema_fast < ema_slow  # simple protective exit
