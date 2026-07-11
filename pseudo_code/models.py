"""Simple data structures used by the pseudo-code."""

from dataclasses import dataclass


@dataclass
class Pose:
    x: float
    y: float
    theta: float


@dataclass
class AnalysisResult:
    reference: str
    colour: str
    pose: Pose
    confidence: float


@dataclass
class Detection:
    reference: str
    colour: str
    pose: Pose
    confidence: float
    encoder_at_capture: int

    def to_dict(self):
        return {
            "reference": self.reference,
            "colour": self.colour,
            "x_mm": self.pose.x,
            "y_mm": self.pose.y,
            "theta_deg": self.pose.theta,
            "confidence": self.confidence,
            "encoder_at_capture": self.encoder_at_capture,
        }
