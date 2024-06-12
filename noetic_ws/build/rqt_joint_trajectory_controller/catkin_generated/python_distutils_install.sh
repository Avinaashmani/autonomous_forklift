#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/avinaash/autonomous_forklift/noetic_ws/src/ros_controllers/rqt_joint_trajectory_controller"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/avinaash/autonomous_forklift/noetic_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/avinaash/autonomous_forklift/noetic_ws/install/lib/python3/dist-packages:/home/avinaash/autonomous_forklift/noetic_ws/build/rqt_joint_trajectory_controller/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/avinaash/autonomous_forklift/noetic_ws/build/rqt_joint_trajectory_controller" \
    "/usr/bin/python3" \
    "/home/avinaash/autonomous_forklift/noetic_ws/src/ros_controllers/rqt_joint_trajectory_controller/setup.py" \
    egg_info --egg-base /home/avinaash/autonomous_forklift/noetic_ws/build/rqt_joint_trajectory_controller \
    build --build-base "/home/avinaash/autonomous_forklift/noetic_ws/build/rqt_joint_trajectory_controller" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/avinaash/autonomous_forklift/noetic_ws/install" --install-scripts="/home/avinaash/autonomous_forklift/noetic_ws/install/bin"
