class XXLState:
    def __init__(self):
        self.active_torpedo = False
        self.last_direction = None
        self.signal_confidence = 0.0
        self.atr_condition = 0.0
        self.cooldown_active = False
        self.last_ema_cross = None
