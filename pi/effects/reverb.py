import pedalboard

class ReverbEffect:
    def __init__(self):
        self.room_size = 0.5
        self.damping = 0.5
        self.wet_level = 0.8
        self.dry_level = 0.9
        self.width = 1.0
        self._plugin = pedalboard.Reverb(
            room_size=self.room_size,
            damping=self.damping,
            wet_level=self.wet_level,
            dry_level=self.dry_level,
            width=self.width,
        )

    def get_plugin(self):
        return self._plugin

    def to_dict(self):
        return {
            "room_size": self.room_size,
            "damping": self.damping,
            "wet_level": self.wet_level,
            "dry_level": self.dry_level,
            "width": self.width,
        }

    def from_dict(self, d):
        self.room_size = d.get("room_size", self.room_size)
        self.damping = d.get("damping", self.damping)
        self.wet_level = d.get("wet_level", self.wet_level)
        self.dry_level = d.get("dry_level", self.dry_level)
        self.width = d.get("width", self.width)
        self._plugin.room_size = self.room_size
        self._plugin.damping = self.damping
        self._plugin.wet_level = self.wet_level
        self._plugin.dry_level = self.dry_level
        self._plugin.width = self.width