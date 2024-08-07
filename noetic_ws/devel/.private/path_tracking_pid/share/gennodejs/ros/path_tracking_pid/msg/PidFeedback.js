// Auto-generated. Do not edit!

// (in-package path_tracking_pid.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class PidFeedback {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.eda = null;
      this.progress = null;
    }
    else {
      if (initObj.hasOwnProperty('eda')) {
        this.eda = initObj.eda
      }
      else {
        this.eda = {secs: 0, nsecs: 0};
      }
      if (initObj.hasOwnProperty('progress')) {
        this.progress = initObj.progress
      }
      else {
        this.progress = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type PidFeedback
    // Serialize message field [eda]
    bufferOffset = _serializer.duration(obj.eda, buffer, bufferOffset);
    // Serialize message field [progress]
    bufferOffset = _serializer.float32(obj.progress, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type PidFeedback
    let len;
    let data = new PidFeedback(null);
    // Deserialize message field [eda]
    data.eda = _deserializer.duration(buffer, bufferOffset);
    // Deserialize message field [progress]
    data.progress = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'path_tracking_pid/PidFeedback';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '23bc81d441ea26241a36fb6127b9e7e4';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    duration eda       # Estimated (optimistic) duration remaining
    float32  progress  # Progress in distance of the path traveled
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new PidFeedback(null);
    if (msg.eda !== undefined) {
      resolved.eda = msg.eda;
    }
    else {
      resolved.eda = {secs: 0, nsecs: 0}
    }

    if (msg.progress !== undefined) {
      resolved.progress = msg.progress;
    }
    else {
      resolved.progress = 0.0
    }

    return resolved;
    }
};

module.exports = PidFeedback;
