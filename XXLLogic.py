class XXLLogic:
    def evaluate_launch(self, state, signals, data):
        state.signal_confidence = signals.compute_signal_confidence(
            data["ema_fast"],
            data["ema_slow"],
            data["atr"],
            data["volatility"],
        )

        if signals.should_launch(state):
            state.active_torpedo = True
            state.last_direction = data["direction"]
            return "LAUNCH"

        return None

    def evaluate_exit(self, state, signals, data):
        if not state.active_torpedo:
            return None

        if signals.should_exit(data["ema_fast"], data["ema_slow"]):
            state.active_torpedo = False
            return "EXIT"

        return None
