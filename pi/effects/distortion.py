import pedalboard

class DistortionEffect:
    def __init__(self):
        self.drive_db = 25.0
        self._plugin = pedalboard.Distortion(
            drive_db=self.drive_db,
        )

    def get_plugin(self):
        return self._plugin

    def to_dict(self):
        return {
            "drive_db": self.drive_db,
        }

    def from_dict(self, d):
        self.drive_db = d.get("drive_db", self.drive_db)
        self._plugin.drive_db = self.drive_db