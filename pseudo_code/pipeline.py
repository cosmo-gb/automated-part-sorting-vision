image = acquire()

image = undistort(image)

mask = segment_colour(image)

objects = extract_objects(mask)

for obj in objects:

    pose = estimate_pose(obj)

    pose_robot = transform(pose)

    pose_robot = compensate_conveyor(pose_robot)

    send_to_robot(pose_robot)
