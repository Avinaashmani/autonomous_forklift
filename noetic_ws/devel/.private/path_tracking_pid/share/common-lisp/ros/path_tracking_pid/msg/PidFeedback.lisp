; Auto-generated. Do not edit!


(cl:in-package path_tracking_pid-msg)


;//! \htmlinclude PidFeedback.msg.html

(cl:defclass <PidFeedback> (roslisp-msg-protocol:ros-message)
  ((eda
    :reader eda
    :initarg :eda
    :type cl:real
    :initform 0)
   (progress
    :reader progress
    :initarg :progress
    :type cl:float
    :initform 0.0))
)

(cl:defclass PidFeedback (<PidFeedback>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PidFeedback>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PidFeedback)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name path_tracking_pid-msg:<PidFeedback> is deprecated: use path_tracking_pid-msg:PidFeedback instead.")))

(cl:ensure-generic-function 'eda-val :lambda-list '(m))
(cl:defmethod eda-val ((m <PidFeedback>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader path_tracking_pid-msg:eda-val is deprecated.  Use path_tracking_pid-msg:eda instead.")
  (eda m))

(cl:ensure-generic-function 'progress-val :lambda-list '(m))
(cl:defmethod progress-val ((m <PidFeedback>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader path_tracking_pid-msg:progress-val is deprecated.  Use path_tracking_pid-msg:progress instead.")
  (progress m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PidFeedback>) ostream)
  "Serializes a message object of type '<PidFeedback>"
  (cl:let ((__sec (cl:floor (cl:slot-value msg 'eda)))
        (__nsec (cl:round (cl:* 1e9 (cl:- (cl:slot-value msg 'eda) (cl:floor (cl:slot-value msg 'eda)))))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 0) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __nsec) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'progress))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PidFeedback>) istream)
  "Deserializes a message object of type '<PidFeedback>"
    (cl:let ((__sec 0) (__nsec 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 0) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __nsec) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'eda) (cl:+ (cl:coerce __sec 'cl:double-float) (cl:/ __nsec 1e9))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'progress) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PidFeedback>)))
  "Returns string type for a message object of type '<PidFeedback>"
  "path_tracking_pid/PidFeedback")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PidFeedback)))
  "Returns string type for a message object of type 'PidFeedback"
  "path_tracking_pid/PidFeedback")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PidFeedback>)))
  "Returns md5sum for a message object of type '<PidFeedback>"
  "23bc81d441ea26241a36fb6127b9e7e4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PidFeedback)))
  "Returns md5sum for a message object of type 'PidFeedback"
  "23bc81d441ea26241a36fb6127b9e7e4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PidFeedback>)))
  "Returns full string definition for message of type '<PidFeedback>"
  (cl:format cl:nil "duration eda       # Estimated (optimistic) duration remaining~%float32  progress  # Progress in distance of the path traveled~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PidFeedback)))
  "Returns full string definition for message of type 'PidFeedback"
  (cl:format cl:nil "duration eda       # Estimated (optimistic) duration remaining~%float32  progress  # Progress in distance of the path traveled~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PidFeedback>))
  (cl:+ 0
     8
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PidFeedback>))
  "Converts a ROS message object to a list"
  (cl:list 'PidFeedback
    (cl:cons ':eda (eda msg))
    (cl:cons ':progress (progress msg))
))
