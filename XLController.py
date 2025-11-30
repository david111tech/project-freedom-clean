class XXLController:
    def __init__(self, logic, signals, state):
        self.logic = logic
        self.signals = signals
        self.state = state

    def process_tick(self, data):
        """Runs for every new candle/tick."""
        launch = self.logic.evaluate_launch(self.state, self.signals, data)
        if launch:
            return launch

        exit_ = self.logic.evaluate_exit(self.state, self.signals, data)
        if exit_:
            return exit_

        return None
                    "hit": hit,
                }

                event = ("{:.1f}s".format(now - self.start_time),
                         "GATLING HIT" if hit else "GATLING MISS",
                         f"Target {t.id} at {distance:.1f}m, angle {angle:.1f}°, price_dir {price_dir}")

                await self.event_queue.put(event)