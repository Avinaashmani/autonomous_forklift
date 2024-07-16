
(cl:in-package :asdf)

(defsystem "gearfork_common-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "forklift_diagnostics_msg" :depends-on ("_package_forklift_diagnostics_msg"))
    (:file "_package_forklift_diagnostics_msg" :depends-on ("_package"))
  ))