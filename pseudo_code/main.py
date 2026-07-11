"""Main loop for the conveyor vision pipeline."""

from models import Detection
from vision_steps import (
    acquire_frame,
    segment_objects,
    analyse_object,
    compensate_conveyor_motion,
)


def process_frame(camera, encoder, calibration, config, robot):
    # Capture the image and encoder position together.
    image, encoder_at_capture = acquire_frame(camera, encoder)

    # Detect individual parts on the conveyor.
    object_masks = segment_objects(image, calibration, config)
    detections = []

    for object_mask in object_masks:
        result = analyse_object(
            image=image,
            object_mask=object_mask,
            calibration=calibration,
            config=config,
        )

        if result is None:
            continue

        # Update the grasp position using conveyor displacement.
        grasp_pose = compensate_conveyor_motion(
            pose=result.pose,
            encoder_at_capture=encoder_at_capture,
            encoder_now=encoder.read(),
            mm_per_count=config.encoder_mm_per_count,
        )

        detections.append(Detection(
            reference=result.reference,
            colour=result.colour,
            pose=grasp_pose,
            confidence=result.confidence,
            encoder_at_capture=encoder_at_capture,
        ))

    # Send only validated detections to the robot.
    robot.send({"detections": [d.to_dict() for d in detections]})


def run(camera, encoder, calibration, config, robot):
    while system_is_running():
        process_frame(camera, encoder, calibration, config, robot)
