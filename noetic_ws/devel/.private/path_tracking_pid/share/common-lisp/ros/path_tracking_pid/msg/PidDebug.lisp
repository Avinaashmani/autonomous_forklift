; Auto-generated. Do not edit!


(cl:in-package path_tracking_pid-msg)


;//! \htmlinclude PidDebug.msg.html

(cl:defclass <PidDebug> (roslisp-msg-protocol:ros-message)
  ((control_error
    :reader control_error
    :initarg :control_error
    :type geometry_msgs-msg:Twist
    :initform (cl:make-instance 'geometry_msgs-msg:Twist))
   (tracking_error
    :reader tracking_error
    :initarg :tracking_error
    :type geometry_msgs-msg:Twist
    :initform (cl:make-instance 'geometry_msgs-msg:Twist))
   (proportional
    :reader proportional
    :initarg :proportional
    :type geometry_msgs-msg:Twist
    :initform (cl:make-instance 'geometry_msgs-msg:Twist))
   (integral
    :reader integral
    :initarg :integral
    :type geometry_msgs-msg:Twist
    :initform (cl:make-instance 'geometry_msgs-msg:Twist))
   (derivative
    :reader derivative
    :initarg :derivative
    :type geometry_msgs-msg:Twist
    :initform (cl:make-instance 'geometry_msgs-msg:Twist))
   (feedforward
    :reader feedforward
    :initarg :feedforward
    :type geometry_msgs-msg:Twist
    :initform (cl:make-instance 'geometry_msgs-msg:Twist))
   (steering_angle
    :reader steering_angle
    :initarg :steering_angle
    :type cl:float
    :initform 0.0)
   (steering_yaw_vel
    :reader steering_yaw_vel
    :initarg :steering_yaw_vel
    :type cl:float
    :initform 0.0)
   (steering_x_vel
    :reader steering_x_vel
    :initarg :steering_x_vel
    :type cl:float
    :initform 0.0))
)

(cl:defclass PidDebug (<PidDebug>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PidDebug>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PidDebug)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name path_tracking_pid-msg:<PidDebug> is deprecated: use path_tracking_pid-msg:PidDebug instead.")))

(cl:ensure-generic-function 'control_error-val :lambda-list '(m))
(cl:defmethod control_error-val ((m <PidDebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader path_tracking_pid-msg:control_error-val is deprecated.  Use path_tracking_pid-msg:control_error instead.")
  (control_error m))

(cl:ensure-generic-function 'tracking_error-val :lambda-list '(m))
(cl:defmethod tracking_error-val ((m <PidDebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader path_tracking_pid-msg:tracking_error-val is deprecated.  Use path_tracking_pid-msg:tracking_error instead.")
  (tracking_error m))

(cl:ensure-generic-function 'proportional-val :lambda-list '(m))
(cl:defmethod proportional-val ((m <PidDebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader path_tracking_pid-msg:proportional-val is deprecated.  Use path_tracking_pid-msg:proportional instead.")
  (proportional m))

(cl:ensure-generic-function 'integral-val :lambda-list '(m))
(cl:defmethod integral-val ((m <PidDebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader path_tracking_pid-msg:integral-val is deprecated.  Use path_tracking_pid-msg:integral instead.")
  (integral m))

(cl:ensure-generic-function 'derivative-val :lambda-list '(m))
(cl:defmethod derivative-val ((m <PidDebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader path_tracking_pid-msg:derivative-val is deprecated.  Use path_tracking_pid-msg:derivative instead.")
  (derivative m))

(cl:ensure-generic-function 'feedforward-val :lambda-list '(m))
(cl:defmethod feedforward-val ((m <PidDebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader path_tracking_pid-msg:feedforward-val is deprecated.  Use path_tracking_pid-msg:feedforward instead.")
  (feedforward m))

(cl:ensure-generic-function 'steering_angle-val :lambda-list '(m))
(cl:defmethod steering_angle-val ((m <PidDebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader path_tracking_pid-msg:steering_angle-val is deprecated.  Use path_tracking_pid-msg:steering_angle instead.")
  (steering_angle m))

(cl:ensure-generic-function 'steering_yaw_vel-val :lambda-list '(m))
(cl:defmethod steering_yaw_vel-val ((m <PidDebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader path_tracking_pid-msg:steering_yaw_vel-val is deprecated.  Use path_tracking_pid-msg:steering_yaw_vel instead.")
  (steering_yaw_vel m))

(cl:ensure-generic-function 'steering_x_vel-val :lambda-list '(m))
(cl:defmethod steering_x_vel-val ((m <PidDebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader path_tracking_pid-msg:steering_x_vel-val is deprecated.  Use path_tracking_pid-msg:steering_x_vel instead.")
  (steering_x_vel m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PidDebug>) ostream)
  "Serializes a message object of type '<PidDebug>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'control_error) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'tracking_error) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'proportional) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'integral) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'derivative) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'feedforward) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'steering_angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'steering_yaw_vel))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'steering_x_vel))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PidDebug>) istream)
  "Deserializes a message object of type '<PidDebug>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'control_error) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'tracking_error) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'proportional) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'integral) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'derivative) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'feedforward) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'steering_angle) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'steering_yaw_vel) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'steering_x_vel) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PidDebug>)))
  "Returns string type for a message object of type '<PidDebug>"
  "path_tracking_pid/PidDebug")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PidDebug)))
  "Returns string type for a message object of type 'PidDebug"
  "path_tracking_pid/PidDebug")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PidDebug>)))
  "Returns md5sum for a message object of type '<PidDebug>"
  "4e3a85077871d90d16f8de7c7a3cf074")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PidDebug)))
  "Returns md5sum for a message object of type 'PidDebug"
  "4e3a85077871d90d16f8de7c7a3cf074")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PidDebug>)))
  "Returns full string definition for message of type '<PidDebug>"
  (cl:format cl:nil "# Error topic containing the 'control' error on which the PID acts~%geometry_msgs/Twist control_error~%# Error topic containing the 'tracking' error, i.e. the real error between path and tracked link~%geometry_msgs/Twist tracking_error~%# Control values~%geometry_msgs/Twist proportional~%geometry_msgs/Twist integral~%geometry_msgs/Twist derivative~%geometry_msgs/Twist feedforward~%float32 steering_angle~%float32 steering_yaw_vel~%float32 steering_x_vel~%~%================================================================================~%MSG: geometry_msgs/Twist~%# This expresses velocity in free space broken into its linear and angular parts.~%Vector3  linear~%Vector3  angular~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PidDebug)))
  "Returns full string definition for message of type 'PidDebug"
  (cl:format cl:nil "# Error topic containing the 'control' error on which the PID acts~%geometry_msgs/Twist control_error~%# Error topic containing the 'tracking' error, i.e. the real error between path and tracked link~%geometry_msgs/Twist tracking_error~%# Control values~%geometry_msgs/Twist proportional~%geometry_msgs/Twist integral~%geometry_msgs/Twist derivative~%geometry_msgs/Twist feedforward~%float32 steering_angle~%float32 steering_yaw_vel~%float32 steering_x_vel~%~%================================================================================~%MSG: geometry_msgs/Twist~%# This expresses velocity in free space broken into its linear and angular parts.~%Vector3  linear~%Vector3  angular~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PidDebug>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'control_error))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'tracking_error))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'proportional))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'integral))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'derivative))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'feedforward))
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PidDebug>))
  "Converts a ROS message object to a list"
  (cl:list 'PidDebug
    (cl:cons ':control_error (control_error msg))
    (cl:cons ':tracking_error (tracking_error msg))
    (cl:cons ':proportional (proportional msg))
    (cl:cons ':integral (integral msg))
    (cl:cons ':derivative (derivative msg))
    (cl:cons ':feedforward (feedforward msg))
    (cl:cons ':steering_angle (steering_angle msg))
    (cl:cons ':steering_yaw_vel (steering_yaw_vel msg))
    (cl:cons ':steering_x_vel (steering_x_vel msg))
))
