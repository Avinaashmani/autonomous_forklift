# CMake generated Testfile for 
# Source directory: /home/avinaash/autonomous_forklift/noetic_ws/src/path_tracking_pid
# Build directory: /home/avinaash/autonomous_forklift/noetic_ws/build/path_tracking_pid
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_path_tracking_pid_roslint_package "/home/avinaash/autonomous_forklift/noetic_ws/build/path_tracking_pid/catkin_generated/env_cached.sh" "/usr/bin/python3" "/opt/ros/noetic/share/catkin/cmake/test/run_tests.py" "/home/avinaash/autonomous_forklift/noetic_ws/build/path_tracking_pid/test_results/path_tracking_pid/roslint-path_tracking_pid.xml" "--working-dir" "/home/avinaash/autonomous_forklift/noetic_ws/build/path_tracking_pid" "--return-code" "/opt/ros/noetic/share/roslint/cmake/../../../lib/roslint/test_wrapper /home/avinaash/autonomous_forklift/noetic_ws/build/path_tracking_pid/test_results/path_tracking_pid/roslint-path_tracking_pid.xml make roslint_path_tracking_pid")
set_tests_properties(_ctest_path_tracking_pid_roslint_package PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/noetic/share/catkin/cmake/test/tests.cmake;160;add_test;/opt/ros/noetic/share/roslint/cmake/roslint-extras.cmake;67;catkin_run_tests_target;/home/avinaash/autonomous_forklift/noetic_ws/src/path_tracking_pid/CMakeLists.txt;83;roslint_add_test;/home/avinaash/autonomous_forklift/noetic_ws/src/path_tracking_pid/CMakeLists.txt;0;")
add_test(_ctest_path_tracking_pid_rostest_test_path_tracking_pid__rviz_false__reconfigure_false.test "/home/avinaash/autonomous_forklift/noetic_ws/build/path_tracking_pid/catkin_generated/env_cached.sh" "/usr/bin/python3" "/opt/ros/noetic/share/catkin/cmake/test/run_tests.py" "/home/avinaash/autonomous_forklift/noetic_ws/build/path_tracking_pid/test_results/path_tracking_pid/rostest-test_path_tracking_pid__rviz_false__reconfigure_false.xml" "--return-code" "/usr/bin/python3 /opt/ros/noetic/share/rostest/cmake/../../../bin/rostest --pkgdir=/home/avinaash/autonomous_forklift/noetic_ws/src/path_tracking_pid --package=path_tracking_pid --results-filename test_path_tracking_pid__rviz_false__reconfigure_false.xml --results-base-dir \"/home/avinaash/autonomous_forklift/noetic_ws/build/path_tracking_pid/test_results\" /home/avinaash/autonomous_forklift/noetic_ws/src/path_tracking_pid/test/test_path_tracking_pid.test rviz:=false reconfigure:=false")
set_tests_properties(_ctest_path_tracking_pid_rostest_test_path_tracking_pid__rviz_false__reconfigure_false.test PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/noetic/share/catkin/cmake/test/tests.cmake;160;add_test;/opt/ros/noetic/share/rostest/cmake/rostest-extras.cmake;52;catkin_run_tests_target;/home/avinaash/autonomous_forklift/noetic_ws/src/path_tracking_pid/CMakeLists.txt;111;add_rostest;/home/avinaash/autonomous_forklift/noetic_ws/src/path_tracking_pid/CMakeLists.txt;0;")
add_test(_ctest_path_tracking_pid_gtest_unittests "/home/avinaash/autonomous_forklift/noetic_ws/build/path_tracking_pid/catkin_generated/env_cached.sh" "/usr/bin/python3" "/opt/ros/noetic/share/catkin/cmake/test/run_tests.py" "/home/avinaash/autonomous_forklift/noetic_ws/build/path_tracking_pid/test_results/path_tracking_pid/gtest-unittests.xml" "--return-code" "/home/avinaash/autonomous_forklift/noetic_ws/devel/.private/path_tracking_pid/lib/path_tracking_pid/unittests --gtest_output=xml:/home/avinaash/autonomous_forklift/noetic_ws/build/path_tracking_pid/test_results/path_tracking_pid/gtest-unittests.xml")
set_tests_properties(_ctest_path_tracking_pid_gtest_unittests PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/noetic/share/catkin/cmake/test/tests.cmake;160;add_test;/opt/ros/noetic/share/catkin/cmake/test/gtest.cmake;98;catkin_run_tests_target;/opt/ros/noetic/share/catkin/cmake/test/gtest.cmake;37;_catkin_add_google_test;/home/avinaash/autonomous_forklift/noetic_ws/src/path_tracking_pid/CMakeLists.txt;112;catkin_add_gtest;/home/avinaash/autonomous_forklift/noetic_ws/src/path_tracking_pid/CMakeLists.txt;0;")
subdirs("gtest")