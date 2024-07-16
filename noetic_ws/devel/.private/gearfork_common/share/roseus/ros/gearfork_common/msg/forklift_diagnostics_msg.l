;; Auto-generated. Do not edit!


(when (boundp 'gearfork_common::forklift_diagnostics_msg)
  (if (not (find-package "GEARFORK_COMMON"))
    (make-package "GEARFORK_COMMON"))
  (shadow 'forklift_diagnostics_msg (find-package "GEARFORK_COMMON")))
(unless (find-package "GEARFORK_COMMON::FORKLIFT_DIAGNOSTICS_MSG")
  (make-package "GEARFORK_COMMON::FORKLIFT_DIAGNOSTICS_MSG"))

(in-package "ROS")
;;//! \htmlinclude forklift_diagnostics_msg.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass gearfork_common::forklift_diagnostics_msg
  :super ros::object
  :slots (_header _angular_vel _linear_vel _kp_dist _kd_dist _kp_angle _kd_angle _y_offset _fork_angle _dist_2_pallet ))

(defmethod gearfork_common::forklift_diagnostics_msg
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:angular_vel __angular_vel) 0.0)
    ((:linear_vel __linear_vel) 0.0)
    ((:kp_dist __kp_dist) 0.0)
    ((:kd_dist __kd_dist) 0.0)
    ((:kp_angle __kp_angle) 0.0)
    ((:kd_angle __kd_angle) 0.0)
    ((:y_offset __y_offset) 0.0)
    ((:fork_angle __fork_angle) 0.0)
    ((:dist_2_pallet __dist_2_pallet) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _angular_vel (float __angular_vel))
   (setq _linear_vel (float __linear_vel))
   (setq _kp_dist (float __kp_dist))
   (setq _kd_dist (float __kd_dist))
   (setq _kp_angle (float __kp_angle))
   (setq _kd_angle (float __kd_angle))
   (setq _y_offset (float __y_offset))
   (setq _fork_angle (float __fork_angle))
   (setq _dist_2_pallet (float __dist_2_pallet))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:angular_vel
   (&optional __angular_vel)
   (if __angular_vel (setq _angular_vel __angular_vel)) _angular_vel)
  (:linear_vel
   (&optional __linear_vel)
   (if __linear_vel (setq _linear_vel __linear_vel)) _linear_vel)
  (:kp_dist
   (&optional __kp_dist)
   (if __kp_dist (setq _kp_dist __kp_dist)) _kp_dist)
  (:kd_dist
   (&optional __kd_dist)
   (if __kd_dist (setq _kd_dist __kd_dist)) _kd_dist)
  (:kp_angle
   (&optional __kp_angle)
   (if __kp_angle (setq _kp_angle __kp_angle)) _kp_angle)
  (:kd_angle
   (&optional __kd_angle)
   (if __kd_angle (setq _kd_angle __kd_angle)) _kd_angle)
  (:y_offset
   (&optional __y_offset)
   (if __y_offset (setq _y_offset __y_offset)) _y_offset)
  (:fork_angle
   (&optional __fork_angle)
   (if __fork_angle (setq _fork_angle __fork_angle)) _fork_angle)
  (:dist_2_pallet
   (&optional __dist_2_pallet)
   (if __dist_2_pallet (setq _dist_2_pallet __dist_2_pallet)) _dist_2_pallet)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; float64 _angular_vel
    8
    ;; float64 _linear_vel
    8
    ;; float64 _kp_dist
    8
    ;; float64 _kd_dist
    8
    ;; float64 _kp_angle
    8
    ;; float64 _kd_angle
    8
    ;; float64 _y_offset
    8
    ;; float64 _fork_angle
    8
    ;; float64 _dist_2_pallet
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; float64 _angular_vel
       (sys::poke _angular_vel (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _linear_vel
       (sys::poke _linear_vel (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _kp_dist
       (sys::poke _kp_dist (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _kd_dist
       (sys::poke _kd_dist (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _kp_angle
       (sys::poke _kp_angle (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _kd_angle
       (sys::poke _kd_angle (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y_offset
       (sys::poke _y_offset (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _fork_angle
       (sys::poke _fork_angle (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dist_2_pallet
       (sys::poke _dist_2_pallet (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; float64 _angular_vel
     (setq _angular_vel (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _linear_vel
     (setq _linear_vel (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _kp_dist
     (setq _kp_dist (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _kd_dist
     (setq _kd_dist (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _kp_angle
     (setq _kp_angle (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _kd_angle
     (setq _kd_angle (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y_offset
     (setq _y_offset (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _fork_angle
     (setq _fork_angle (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dist_2_pallet
     (setq _dist_2_pallet (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get gearfork_common::forklift_diagnostics_msg :md5sum-) "65a0dd5e5edc9836b73daeb41d8cfa46")
(setf (get gearfork_common::forklift_diagnostics_msg :datatype-) "gearfork_common/forklift_diagnostics_msg")
(setf (get gearfork_common::forklift_diagnostics_msg :definition-)
      "Header header
float64 angular_vel
float64 linear_vel
float64 kp_dist
float64 kd_dist
float64 kp_angle
float64 kd_angle
float64 y_offset
float64 fork_angle
float64 dist_2_pallet
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

")



(provide :gearfork_common/forklift_diagnostics_msg "65a0dd5e5edc9836b73daeb41d8cfa46")


