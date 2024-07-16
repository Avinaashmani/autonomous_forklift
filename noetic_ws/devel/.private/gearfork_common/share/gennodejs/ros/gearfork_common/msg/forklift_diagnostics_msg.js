// Auto-generated. Do not edit!

// (in-package gearfork_common.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class forklift_diagnostics_msg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.angular_vel = null;
      this.linear_vel = null;
      this.kp_dist = null;
      this.kd_dist = null;
      this.kp_angle = null;
      this.kd_angle = null;
      this.y_offset = null;
      this.fork_angle = null;
      this.dist_2_pallet = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('angular_vel')) {
        this.angular_vel = initObj.angular_vel
      }
      else {
        this.angular_vel = 0.0;
      }
      if (initObj.hasOwnProperty('linear_vel')) {
        this.linear_vel = initObj.linear_vel
      }
      else {
        this.linear_vel = 0.0;
      }
      if (initObj.hasOwnProperty('kp_dist')) {
        this.kp_dist = initObj.kp_dist
      }
      else {
        this.kp_dist = 0.0;
      }
      if (initObj.hasOwnProperty('kd_dist')) {
        this.kd_dist = initObj.kd_dist
      }
      else {
        this.kd_dist = 0.0;
      }
      if (initObj.hasOwnProperty('kp_angle')) {
        this.kp_angle = initObj.kp_angle
      }
      else {
        this.kp_angle = 0.0;
      }
      if (initObj.hasOwnProperty('kd_angle')) {
        this.kd_angle = initObj.kd_angle
      }
      else {
        this.kd_angle = 0.0;
      }
      if (initObj.hasOwnProperty('y_offset')) {
        this.y_offset = initObj.y_offset
      }
      else {
        this.y_offset = 0.0;
      }
      if (initObj.hasOwnProperty('fork_angle')) {
        this.fork_angle = initObj.fork_angle
      }
      else {
        this.fork_angle = 0.0;
      }
      if (initObj.hasOwnProperty('dist_2_pallet')) {
        this.dist_2_pallet = initObj.dist_2_pallet
      }
      else {
        this.dist_2_pallet = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type forklift_diagnostics_msg
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [angular_vel]
    bufferOffset = _serializer.float64(obj.angular_vel, buffer, bufferOffset);
    // Serialize message field [linear_vel]
    bufferOffset = _serializer.float64(obj.linear_vel, buffer, bufferOffset);
    // Serialize message field [kp_dist]
    bufferOffset = _serializer.float64(obj.kp_dist, buffer, bufferOffset);
    // Serialize message field [kd_dist]
    bufferOffset = _serializer.float64(obj.kd_dist, buffer, bufferOffset);
    // Serialize message field [kp_angle]
    bufferOffset = _serializer.float64(obj.kp_angle, buffer, bufferOffset);
    // Serialize message field [kd_angle]
    bufferOffset = _serializer.float64(obj.kd_angle, buffer, bufferOffset);
    // Serialize message field [y_offset]
    bufferOffset = _serializer.float64(obj.y_offset, buffer, bufferOffset);
    // Serialize message field [fork_angle]
    bufferOffset = _serializer.float64(obj.fork_angle, buffer, bufferOffset);
    // Serialize message field [dist_2_pallet]
    bufferOffset = _serializer.float64(obj.dist_2_pallet, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type forklift_diagnostics_msg
    let len;
    let data = new forklift_diagnostics_msg(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [angular_vel]
    data.angular_vel = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [linear_vel]
    data.linear_vel = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [kp_dist]
    data.kp_dist = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [kd_dist]
    data.kd_dist = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [kp_angle]
    data.kp_angle = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [kd_angle]
    data.kd_angle = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [y_offset]
    data.y_offset = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [fork_angle]
    data.fork_angle = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [dist_2_pallet]
    data.dist_2_pallet = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 72;
  }

  static datatype() {
    // Returns string type for a message object
    return 'gearfork_common/forklift_diagnostics_msg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '65a0dd5e5edc9836b73daeb41d8cfa46';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new forklift_diagnostics_msg(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.angular_vel !== undefined) {
      resolved.angular_vel = msg.angular_vel;
    }
    else {
      resolved.angular_vel = 0.0
    }

    if (msg.linear_vel !== undefined) {
      resolved.linear_vel = msg.linear_vel;
    }
    else {
      resolved.linear_vel = 0.0
    }

    if (msg.kp_dist !== undefined) {
      resolved.kp_dist = msg.kp_dist;
    }
    else {
      resolved.kp_dist = 0.0
    }

    if (msg.kd_dist !== undefined) {
      resolved.kd_dist = msg.kd_dist;
    }
    else {
      resolved.kd_dist = 0.0
    }

    if (msg.kp_angle !== undefined) {
      resolved.kp_angle = msg.kp_angle;
    }
    else {
      resolved.kp_angle = 0.0
    }

    if (msg.kd_angle !== undefined) {
      resolved.kd_angle = msg.kd_angle;
    }
    else {
      resolved.kd_angle = 0.0
    }

    if (msg.y_offset !== undefined) {
      resolved.y_offset = msg.y_offset;
    }
    else {
      resolved.y_offset = 0.0
    }

    if (msg.fork_angle !== undefined) {
      resolved.fork_angle = msg.fork_angle;
    }
    else {
      resolved.fork_angle = 0.0
    }

    if (msg.dist_2_pallet !== undefined) {
      resolved.dist_2_pallet = msg.dist_2_pallet;
    }
    else {
      resolved.dist_2_pallet = 0.0
    }

    return resolved;
    }
};

module.exports = forklift_diagnostics_msg;
