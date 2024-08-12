#include <pluginlib/class_list_macros.h>
#include <nav_core/base_global_planner.h>
#include <nav_msgs/Path.h>
#include <ros/ros.h>

namespace custom_global_planner {

class StraightLineGlobalPlanner : public nav_core::BaseGlobalPlanner {
public:
    StraightLineGlobalPlanner() : initialized_(false) {}

    StraightLineGlobalPlanner(std::string name, costmap_2d::Costmap2DROS* costmap_ros) : initialized_(false) {
        initialize(name, costmap_ros);
    }

    void initialize(std::string name, costmap_2d::Costmap2DROS* costmap_ros) override {
        if (!initialized_) {
            ros::NodeHandle private_nh("~/" + name);
            path_sub_ = private_nh.subscribe("/path", 1, &StraightLineGlobalPlanner::pathCallback, this);
            initialized_ = true;
        }
    }

    bool makePlan(const geometry_msgs::PoseStamped& start,
                  const geometry_msgs::PoseStamped& goal,
                  std::vector<geometry_msgs::PoseStamped>& plan) override {
        if (!initialized_) {
            ROS_ERROR("The planner has not been initialized, please call initialize() first");
            return false;
        }

        if (path_.poses.empty()) {
            ROS_WARN("Received empty path");
            return false;
        }

        plan = path_.poses;
        return true;
    }

private:
    void pathCallback(const nav_msgs::Path::ConstPtr& path_msg) {
        path_ = *path_msg;
        ROS_INFO("Received path with %lu poses", path_.poses.size());
    }

    bool initialized_;
    ros::Subscriber path_sub_;
    nav_msgs::Path path_;
};

}  // namespace custom_global_planner

PLUGINLIB_EXPORT_CLASS(custom_global_planner::StraightLineGlobalPlanner, nav_core::BaseGlobalPlanner)
