import base64
import io
from typing import Tuple

import numpy as np
import librosa
import soundfile as sf


class VoiceClassifier:
    """
    Wrapper around your actual audio classifier.
    Replace the `predict` method with real model inference.
    """

    def __init__(self):
        # TODO: load your trained model here
        # Example:
        #   import joblib
        #   self.model = joblib.load("models/voice_classifier.joblib")
        self.model = None

    def _decode_audio(self, audio_base64: str, sr: int = 16000) -> np.ndarray:
        decoded = base64.b64decode(audio_base64)
        buffer = io.BytesIO(decoded)

        # Try reading as audio file
        try:
            y, file_sr = sf.read(buffer)
            if file_sr != sr:
                y = librosa.resample(y, orig_sr=file_sr, target_sr=sr)
        except Exception:
            # Fallback to librosa if needed
            buffer.seek(0)
            y, _ = librosa.load(buffer, sr=sr, mono=True)

        return y

    def _extract_features(self, y: np.ndarray, sr: int = 16000) -> np.ndarray:
        # Example: MFCC features mean+std
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        features = np.concatenate([mfcc.mean(axis=1), mfcc.std(axis=1)])
        return features.reshape(1, -1)

    def predict(self, audio_base64: str, language_code: str) -> Tuple[str, float, str]:
        """
        Returns (label, confidence, detail)

        Replace the inside of this with your real classifier.
        """
        # Decode & feature extraction (you can keep or change this)
        y = self._decode_audio(audio_base64)
        features = self._extract_features(y)

        # TODO: use your model here instead of dummy logic.
        # Example:
        #   proba = self.model.predict_proba(features)[0]
        #   idx = int(np.argmax(proba))
        #   label = "AI_GENERATED" if idx == 1 else "HUMAN"
        #   confidence = float(proba[idx])
        # For now, just a placeholder based on simple energy heuristic:
        energy = float(np.mean(y ** 2))
        if energy > 0.01:
            label = "HUMAN"
            confidence = 0.65
        else:
            label = "AI_GENERATED"
            confidence = 0.60

        detail = f"Energy={energy:.6f}, language={language_code}"
        return label, confidence, detail


# Single global instance
classifier = VoiceClassifier()