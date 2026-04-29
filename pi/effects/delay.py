import pedalboard

class DelayEffect:
    def __init__(self):
        self.delay_seconds = 0.3
        self.feedback = 0.4
        self.mix = 0.5
        self._plugin = pedalboard.Delay(
            delay_seconds=self.delay_seconds,
            feedback=self.feedback,
            mix=self.mix,
        )

    def get_plugin(self):
        return self._plugin

    def to_dict(self):
        return {
            "delay_seconds": self.delay_seconds,
            "feedback": self.feedback,
            "mix": self.mix,
        }

    def from_dict(self, d):
        self.delay_seconds = d.get("delay_seconds", self.delay_seconds)
        self.feedback = d.get("feedback", self.feedback)
        self.mix = d.get("mix", self.mix)
        self._plugin.delay_seconds = self.delay_seconds
        self._plugin.feedback = self.feedback
        self._plugin.mix = self.mix