;; Auto-generated. Do not edit!


(when (boundp 'path_tracking_pid::PidDebug)
  (if (not (find-package "PATH_TRACKING_PID"))
    (make-package "PATH_TRACKING_PID"))
  (shadow 'PidDebug (find-package "PATH_TRACKING_PID")))
(unless (find-package "PATH_TRACKING_PID::PIDDEBUG")
  (make-package "PATH_TRACKING_PID::PIDDEBUG"))

(in-package "ROS")
;;//! \htmlinclude PidDebug.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass path_tracking_pid::PidDebug
  :super ros::object
  :slots (_control_error _tracking_error _proportional _integral _derivative _feedforward _steering_angle _steering_yaw_vel _steering_x_vel ))

(defmethod path_tracking_pid::PidDebug
  (:init
   (&key
    ((:control_error __control_error) (instance geometry_msgs::Twist :init))
    ((:tracking_error __tracking_error) (instance geometry_msgs::Twist :init))
    ((:proportional __proportional) (instance geometry_msgs::Twist :init))
    ((:integral __integral) (instance geometry_msgs::Twist :init))
    ((:derivative __derivative) (instance geometry_msgs::Twist :init))
    ((:feedforward __feedforward) (instance geometry_msgs::Twist :init))
    ((:steering_angle __steering_angle) 0.0)
    ((:steering_yaw_vel __steering_yaw_vel) 0.0)
    ((:steering_x_vel __steering_x_vel) 0.0)
    )
   (send-super :init)
   (setq _control_error __control_error)
   (setq _tracking_error __tracking_error)
   (setq _proportional __proportional)
   (setq _integral __integral)
   (setq _derivative __derivative)
   (setq _feedforward __feedforward)
   (setq _steering_angle (float __steering_angle))
   (setq _steering_yaw_vel (float __steering_yaw_vel))
   (setq _steering_x_vel (float __steering_x_vel))
   self)
  (:control_error
   (&rest __control_error)
   (if (keywordp (car __control_error))
       (send* _control_error __control_error)
     (progn
       (if __control_error (setq _control_error (car __control_error)))
       _control_error)))
  (:tracking_error
   (&rest __tracking_error)
   (if (keywordp (car __tracking_error))
       (send* _tracking_error __tracking_error)
     (progn
       (if __tracking_error (setq _tracking_error (car __tracking_error)))
       _tracking_error)))
  (:proportional
   (&rest __proportional)
   (if (keywordp (car __proportional))
       (send* _proportional __proportional)
     (progn
       (if __proportional (setq _proportional (car __proportional)))
       _proportional)))
  (:integral
   (&rest __integral)
   (if (keywordp (car __integral))
       (send* _integral __integral)
     (progn
       (if __integral (setq _integral (car __integral)))
       _integral)))
  (:derivative
   (&rest __derivative)
   (if (keywordp (car __derivative))
       (send* _derivative __derivative)
     (progn
       (if __derivative (setq _derivative (car __derivative)))
       _derivative)))
  (:feedforward
   (&rest __feedforward)
   (if (keywordp (car __feedforward))
       (send* _feedforward __feedforward)
     (progn
       (if __feedforward (setq _feedforward (car __feedforward)))
       _feedforward)))
  (:steering_angle
   (&optional __steering_angle)
   (if __steering_angle (setq _steering_angle __steering_angle)) _steering_angle)
  (:steering_yaw_vel
   (&optional __steering_yaw_vel)
   (if __steering_yaw_vel (setq _steering_yaw_vel __steering_yaw_vel)) _steering_yaw_vel)
  (:steering_x_vel
   (&optional __steering_x_vel)
   (if __steering_x_vel (setq _steering_x_vel __steering_x_vel)) _steering_x_vel)
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Twist _control_error
    (send _control_error :serialization-length)
    ;; geometry_msgs/Twist _tracking_error
    (send _tracking_error :serialization-length)
    ;; geometry_msgs/Twist _proportional
    (send _proportional :serialization-length)
    ;; geometry_msgs/Twist _integral
    (send _integral :serialization-length)
    ;; geometry_msgs/Twist _derivative
    (send _derivative :serialization-length)
    ;; geometry_msgs/Twist _feedforward
    (send _feedforward :serialization-length)
    ;; float32 _steering_angle
    4
    ;; float32 _steering_yaw_vel
    4
    ;; float32 _steering_x_vel
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Twist _control_error
       (send _control_error :serialize s)
     ;; geometry_msgs/Twist _tracking_error
       (send _tracking_error :serialize s)
     ;; geometry_msgs/Twist _proportional
       (send _proportional :serialize s)
     ;; geometry_msgs/Twist _integral
       (send _integral :serialize s)
     ;; geometry_msgs/Twist _derivative
       (send _derivative :serialize s)
     ;; geometry_msgs/Twist _feedforward
       (send _feedforward :serialize s)
     ;; float32 _steering_angle
       (sys::poke _steering_angle (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _steering_yaw_vel
       (sys::poke _steering_yaw_vel (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _steering_x_vel
       (sys::poke _steering_x_vel (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Twist _control_error
     (send _control_error :deserialize buf ptr-) (incf ptr- (send _control_error :serialization-length))
   ;; geometry_msgs/Twist _tracking_error
     (send _tracking_error :deserialize buf ptr-) (incf ptr- (send _tracking_error :serialization-length))
   ;; geometry_msgs/Twist _proportional
     (send _proportional :deserialize buf ptr-) (incf ptr- (send _proportional :serialization-length))
   ;; geometry_msgs/Twist _integral
     (send _integral :deserialize buf ptr-) (incf ptr- (send _integral :serialization-length))
   ;; geometry_msgs/Twist _derivative
     (send _derivative :deserialize buf ptr-) (incf ptr- (send _derivative :serialization-length))
   ;; geometry_msgs/Twist _feedforward
     (send _feedforward :deserialize buf ptr-) (incf ptr- (send _feedforward :serialization-length))
   ;; float32 _steering_angle
     (setq _steering_angle (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _steering_yaw_vel
     (setq _steering_yaw_vel (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _steering_x_vel
     (setq _steering_x_vel (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get path_tracking_pid::PidDebug :md5sum-) "4e3a85077871d90d16f8de7c7a3cf074")
(setf (get path_tracking_pid::PidDebug :datatype-) "path_tracking_pid/PidDebug")
(setf (get path_tracking_pid::PidDebug :definition-)
      "# Error topic containing the 'control' error on which the PID acts
geometry_msgs/Twist control_error
# Error topic containing the 'tracking' error, i.e. the real error between path and tracked link
geometry_msgs/Twist tracking_error
# Control values
geometry_msgs/Twist proportional
geometry_msgs/Twist integral
geometry_msgs/Twist derivative
geometry_msgs/Twist feedforward
float32 steering_angle
float32 steering_yaw_vel
float32 steering_x_vel

================================================================================
MSG: geometry_msgs/Twist
# This expresses velocity in free space broken into its linear and angular parts.
Vector3  linear
Vector3  angular

================================================================================
MSG: geometry_msgs/Vector3
# This represents a vector in free space. 
# It is only meant to represent a direction. Therefore, it does not
# make sense to apply a translation to it (e.g., when applying a 
# generic rigid transformation to a Vector3, tf2 will only apply the
# rotation). If you want your data to be translatable too, use the
# geometry_msgs/Point message instead.

float64 x
float64 y
float64 z
")



(provide :path_tracking_pid/PidDebug "4e3a85077871d90d16f8de7c7a3cf074")


