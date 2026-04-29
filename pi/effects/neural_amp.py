import json
import numpy as np
import torch
import nam.models

class NeuralAmpEffect:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.gain = 1.0
        self.master = 1.0
        self._model = None

        if model_path:
            self._load_model(model_path)

    def _load_model(self, model_path):
        try:
            with open(model_path, "r") as fp:
                config = json.load(fp)
            self._model = nam.models.init_from_nam(config)
            self._model.eval()
            print(f"Model loaded: {model_path}")
        except Exception as e:
            print(f"Failed to load model: {e}")

    def process(self, audio_block):
        if self._model is None:
            return audio_block
        with torch.no_grad():
            x = torch.from_numpy(audio_block.flatten()).float()
            y = self._model(x)
            return y.numpy()
        
    def to_dict(self):
        return {
            "model_path": self.model_path,
            "gain": self.gain,
            "master": self.master,
        }

    def from_dict(self, d):
        self.model_path = d.get("model_path", self.model_path)
        self.gain = d.get("gain", self.gain)
        self.master = d.get("master", self.master)