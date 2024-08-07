// Auto-generated. Do not edit!

// (in-package path_tracking_pid.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class PidDebug {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.control_error = null;
      this.tracking_error = null;
      this.proportional = null;
      this.integral = null;
      this.derivative = null;
      this.feedforward = null;
      this.steering_angle = null;
      this.steering_yaw_vel = null;
      this.steering_x_vel = null;
    }
    else {
      if (initObj.hasOwnProperty('control_error')) {
        this.control_error = initObj.control_error
      }
      else {
        this.control_error = new geometry_msgs.msg.Twist();
      }
      if (initObj.hasOwnProperty('tracking_error')) {
        this.tracking_error = initObj.tracking_error
      }
      else {
        this.tracking_error = new geometry_msgs.msg.Twist();
      }
      if (initObj.hasOwnProperty('proportional')) {
        this.proportional = initObj.proportional
      }
      else {
        this.proportional = new geometry_msgs.msg.Twist();
      }
      if (initObj.hasOwnProperty('integral')) {
        this.integral = initObj.integral
      }
      else {
        this.integral = new geometry_msgs.msg.Twist();
      }
      if (initObj.hasOwnProperty('derivative')) {
        this.derivative = initObj.derivative
      }
      else {
        this.derivative = new geometry_msgs.msg.Twist();
      }
      if (initObj.hasOwnProperty('feedforward')) {
        this.feedforward = initObj.feedforward
      }
      else {
        this.feedforward = new geometry_msgs.msg.Twist();
      }
      if (initObj.hasOwnProperty('steering_angle')) {
        this.steering_angle = initObj.steering_angle
      }
      else {
        this.steering_angle = 0.0;
      }
      if (initObj.hasOwnProperty('steering_yaw_vel')) {
        this.steering_yaw_vel = initObj.steering_yaw_vel
      }
      else {
        this.steering_yaw_vel = 0.0;
      }
      if (initObj.hasOwnProperty('steering_x_vel')) {
        this.steering_x_vel = initObj.steering_x_vel
      }
      else {
        this.steering_x_vel = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type PidDebug
    // Serialize message field [control_error]
    bufferOffset = geometry_msgs.msg.Twist.serialize(obj.control_error, buffer, bufferOffset);
    // Serialize message field [tracking_error]
    bufferOffset = geometry_msgs.msg.Twist.serialize(obj.tracking_error, buffer, bufferOffset);
    // Serialize message field [proportional]
    bufferOffset = geometry_msgs.msg.Twist.serialize(obj.proportional, buffer, bufferOffset);
    // Serialize message field [integral]
    bufferOffset = geometry_msgs.msg.Twist.serialize(obj.integral, buffer, bufferOffset);
    // Serialize message field [derivative]
    bufferOffset = geometry_msgs.msg.Twist.serialize(obj.derivative, buffer, bufferOffset);
    // Serialize message field [feedforward]
    bufferOffset = geometry_msgs.msg.Twist.serialize(obj.feedforward, buffer, bufferOffset);
    // Serialize message field [steering_angle]
    bufferOffset = _serializer.float32(obj.steering_angle, buffer, bufferOffset);
    // Serialize message field [steering_yaw_vel]
    bufferOffset = _serializer.float32(obj.steering_yaw_vel, buffer, bufferOffset);
    // Serialize message field [steering_x_vel]
    bufferOffset = _serializer.float32(obj.steering_x_vel, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type PidDebug
    let len;
    let data = new PidDebug(null);
    // Deserialize message field [control_error]
    data.control_error = geometry_msgs.msg.Twist.deserialize(buffer, bufferOffset);
    // Deserialize message field [tracking_error]
    data.tracking_error = geometry_msgs.msg.Twist.deserialize(buffer, bufferOffset);
    // Deserialize message field [proportional]
    data.proportional = geometry_msgs.msg.Twist.deserialize(buffer, bufferOffset);
    // Deserialize message field [integral]
    data.integral = geometry_msgs.msg.Twist.deserialize(buffer, bufferOffset);
    // Deserialize message field [derivative]
    data.derivative = geometry_msgs.msg.Twist.deserialize(buffer, bufferOffset);
    // Deserialize message field [feedforward]
    data.feedforward = geometry_msgs.msg.Twist.deserialize(buffer, bufferOffset);
    // Deserialize message field [steering_angle]
    data.steering_angle = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [steering_yaw_vel]
    data.steering_yaw_vel = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [steering_x_vel]
    data.steering_x_vel = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 300;
  }

  static datatype() {
    // Returns string type for a message object
    return 'path_tracking_pid/PidDebug';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '4e3a85077871d90d16f8de7c7a3cf074';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # Error topic containing the 'control' error on which the PID acts
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
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new PidDebug(null);
    if (msg.control_error !== undefined) {
      resolved.control_error = geometry_msgs.msg.Twist.Resolve(msg.control_error)
    }
    else {
      resolved.control_error = new geometry_msgs.msg.Twist()
    }

    if (msg.tracking_error !== undefined) {
      resolved.tracking_error = geometry_msgs.msg.Twist.Resolve(msg.tracking_error)
    }
    else {
      resolved.tracking_error = new geometry_msgs.msg.Twist()
    }

    if (msg.proportional !== undefined) {
      resolved.proportional = geometry_msgs.msg.Twist.Resolve(msg.proportional)
    }
    else {
      resolved.proportional = new geometry_msgs.msg.Twist()
    }

    if (msg.integral !== undefined) {
      resolved.integral = geometry_msgs.msg.Twist.Resolve(msg.integral)
    }
    else {
      resolved.integral = new geometry_msgs.msg.Twist()
    }

    if (msg.derivative !== undefined) {
      resolved.derivative = geometry_msgs.msg.Twist.Resolve(msg.derivative)
    }
    else {
      resolved.derivative = new geometry_msgs.msg.Twist()
    }

    if (msg.feedforward !== undefined) {
      resolved.feedforward = geometry_msgs.msg.Twist.Resolve(msg.feedforward)
    }
    else {
      resolved.feedforward = new geometry_msgs.msg.Twist()
    }

    if (msg.steering_angle !== undefined) {
      resolved.steering_angle = msg.steering_angle;
    }
    else {
      resolved.steering_angle = 0.0
    }

    if (msg.steering_yaw_vel !== undefined) {
      resolved.steering_yaw_vel = msg.steering_yaw_vel;
    }
    else {
      resolved.steering_yaw_vel = 0.0
    }

    if (msg.steering_x_vel !== undefined) {
      resolved.steering_x_vel = msg.steering_x_vel;
    }
    else {
      resolved.steering_x_vel = 0.0
    }

    return resolved;
    }
};

module.exports = PidDebug;
