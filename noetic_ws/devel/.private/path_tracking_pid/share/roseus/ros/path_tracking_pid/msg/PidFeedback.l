;; Auto-generated. Do not edit!


(when (boundp 'path_tracking_pid::PidFeedback)
  (if (not (find-package "PATH_TRACKING_PID"))
    (make-package "PATH_TRACKING_PID"))
  (shadow 'PidFeedback (find-package "PATH_TRACKING_PID")))
(unless (find-package "PATH_TRACKING_PID::PIDFEEDBACK")
  (make-package "PATH_TRACKING_PID::PIDFEEDBACK"))

(in-package "ROS")
;;//! \htmlinclude PidFeedback.msg.html


(defclass path_tracking_pid::PidFeedback
  :super ros::object
  :slots (_eda _progress ))

(defmethod path_tracking_pid::PidFeedback
  (:init
   (&key
    ((:eda __eda) (instance ros::time :init))
    ((:progress __progress) 0.0)
    )
   (send-super :init)
   (setq _eda __eda)
   (setq _progress (float __progress))
   self)
  (:eda
   (&optional __eda)
   (if __eda (setq _eda __eda)) _eda)
  (:progress
   (&optional __progress)
   (if __progress (setq _progress __progress)) _progress)
  (:serialization-length
   ()
   (+
    ;; duration _eda
    8
    ;; float32 _progress
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; duration _eda
       (write-long (send _eda :sec) s) (write-long (send _eda :nsec) s)
     ;; float32 _progress
       (sys::poke _progress (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; duration _eda
     (send _eda :sec (sys::peek buf ptr- :integer)) (incf ptr- 4)  (send _eda :nsec (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float32 _progress
     (setq _progress (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get path_tracking_pid::PidFeedback :md5sum-) "23bc81d441ea26241a36fb6127b9e7e4")
(setf (get path_tracking_pid::PidFeedback :datatype-) "path_tracking_pid/PidFeedback")
(setf (get path_tracking_pid::PidFeedback :definition-)
      "duration eda       # Estimated (optimistic) duration remaining
float32  progress  # Progress in distance of the path traveled

")



(provide :path_tracking_pid/PidFeedback "23bc81d441ea26241a36fb6127b9e7e4")


