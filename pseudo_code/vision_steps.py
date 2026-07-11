"""High-level pseudo-code for image processing steps."""

from models import AnalysisResult


def acquire_frame(camera, encoder):
    encoder_position = encoder.read()
    image = camera.capture()
    return image, encoder_position


def segment_objects(image, calibration, config):
    # Correct lens distortion before any measurement.
    image = undistort(image, calibration.camera)

    # Separate parts from the conveyor background.
    mask = threshold_parts(
        image,
        background=config.empty_conveyor_image,
        thresholds=config.segmentation,
    )

    # Remove noise and return one mask per visible part.
    mask = clean_binary_mask(mask)
    return find_connected_objects(mask)


def analyse_object(image, object_mask, calibration, config):
    if not valid_size(object_mask, config.min_area, config.max_area):
        return None

    colour = estimate_colour(image, object_mask)
    contour = extract_contour(object_mask)

    reference, class_score = classify_part(
        colour,
        contour,
        config.product_models,
    )

    if reference is None or class_score < config.min_class_score:
        return None

    pose_px, pose_score = estimate_pose(
        contour,
        config.product_models[reference],
    )

    if pose_score < config.min_pose_score:
        return None

    # Convert image coordinates to robot coordinates.
    pose_robot = transform_pose(
        pose_px,
        calibration.image_to_conveyor,
        calibration.conveyor_to_robot,
    )

    # Apply the reference-specific grasp point.
    grasp_pose = apply_grasp_offset(
        pose_robot,
        config.product_models[reference].grasp_offset,
    )

    return AnalysisResult(
        reference=reference,
        colour=colour,
        pose=grasp_pose,
        confidence=min(class_score, pose_score),
    )


def compensate_conveyor_motion(
    pose,
    encoder_at_capture,
    encoder_now,
    mm_per_count,
):
    travelled_mm = (encoder_now - encoder_at_capture) * mm_per_count
    pose.y += travelled_mm
    return pose
