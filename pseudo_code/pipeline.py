image = acquire()

image = undistort(image)

# segmentation from background

image_lab = convert_to_lab(image)

# consider a comparison with empty conveyor
mask = threshold_difference_from_background(image_lab)

mask = morphological_opening(mask)
mask = morphological_closing(mask)

objects = connected_components(mask)

mask = segment_colour(image)

objects = extract_objects(mask)

for obj in objects:

    pose = estimate_pose(obj)

    pose_robot = transform(pose)

    pose_robot = compensate_conveyor(pose_robot)

    send_to_robot(pose_robot)
