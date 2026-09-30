# Class label emitted by the detector, for example "person".
string class_name

# Detector confidence in the inclusive range [0, 1].
float32 confidence

# True only when a valid 3D position has been estimated from depth.
bool has_position

# Position in the coordinate frame and timestamp on the containing array header.
geometry_msgs/Point position

# Optional tracker identifier. Empty when tracking is unavailable.
string track_id

# Detection rectangle in source-image pixel coordinates.
float32 bbox_center_x
float32 bbox_center_y
float32 bbox_width
float32 bbox_height
