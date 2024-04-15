"""Module providing the ros_snapd ROS node."""

import rospy
import snap_http

from ros_snapd.srv import (
    SnapdList,
    SnapdListRequest,
    SnapdListResponse,
    SnapdRestart,
    SnapdRestartRequest,
    SnapdRestartResponse,
    SnapdStart,
    SnapdStartRequest,
    SnapdStartResponse,
    SnapdStop,
    SnapdStopRequest,
    SnapdStopResponse,
)

_EXCLUSION_LIST = [
    "lxd.activate",
    "lxd.daemon",
    "lxd.user-daemon",
    "ros-snapd.ros-snapd",
    "ros2-snapd.ros2-snapd",
]


class RosSnapdNode:
    """The ros_snapd Node."""

    def __init__(self) -> None:
        self.list_service = rospy.Service("~list", SnapdList, self._handle_list)
        self.start_service = rospy.Service("~start", SnapdStart, self._handle_start)
        self.start_service = rospy.Service(
            "~restart", SnapdRestart, self._handle_restart
        )
        self.stop_service = rospy.Service("~stop", SnapdStop, self._handle_stop)

    def _handle_list(self, req: SnapdListRequest) -> SnapdListResponse:
        rospy.logdebug("Listing services")

        try:
            list_response = snap_http.get_apps(services_only=True)
        except snap_http.http.SnapdHttpException as e:
            rospy.logerr(e)
            return SnapdListResponse(
                False, "Something went wrong while querying for services", []
            )

        rospy.logdebug(list_response)

        services = []
        for it in list_response.result:
            service_name = f"{it['snap']}.{it['name']}"
            if service_name not in _EXCLUSION_LIST:
                services.append(service_name)

        rospy.logdebug(services)

        return SnapdListResponse(True, "", services)

    def _handle_start(self, req: SnapdStartRequest) -> SnapdStartResponse:
        rospy.logdebug("Starting: %s", req.service)

        if req.service in _EXCLUSION_LIST:
            return SnapdStartResponse(False, f"Cannot start '{req.service}'")

        start_response = None
        try:
            start_response = snap_http.start(name=req.service)
        except snap_http.http.SnapdHttpException as e:
            rospy.logerr(e)
            return SnapdStartResponse(
                False, f"Something went wrong while starting '{req.service}': {e}"
            )

        rospy.logdebug(start_response)

        check_change_response = snap_http.check_change(start_response.change)

        rospy.logdebug(check_change_response)

        while check_change_response.result["status"] == "Doing":
            rospy.sleep(0.1)
            check_change_response = snap_http.check_change(start_response.change)
            rospy.logdebug(check_change_response)

        return SnapdStartResponse(True, f"Service '{req.service}' started")

    def _handle_restart(self, req: SnapdRestartRequest) -> SnapdRestartResponse:
        rospy.logdebug("Restarting: %s", req.service)

        if req.service in _EXCLUSION_LIST:
            return SnapdRestartResponse(False, f"Cannot restart '{req.service}'")

        restart_response = None
        try:
            restart_response = snap_http.restart(name=req.service)
        except snap_http.http.SnapdHttpException as e:
            rospy.logerr(e)
            return SnapdRestartResponse(
                False, f"Something went wrong while restarting '{req.service}': {e}"
            )

        rospy.logdebug(restart_response)

        check_change_response = snap_http.check_change(restart_response.change)

        rospy.logdebug(check_change_response)

        while check_change_response.result["status"] == "Doing":
            rospy.sleep(0.1)
            check_change_response = snap_http.check_change(restart_response.change)
            rospy.logdebug(check_change_response)

        return SnapdRestartResponse(True, f"Service '{req.service}' restarted")

    def _handle_stop(self, req: SnapdStopRequest) -> SnapdStopResponse:
        rospy.logdebug("Stopping: %s", req.service)

        if req.service in _EXCLUSION_LIST:
            return SnapdStopResponse(False, f"Cannot stop '{req.service}'")

        stop_response = None
        try:
            stop_response = snap_http.stop(name=req.service)
        except snap_http.http.SnapdHttpException as e:
            rospy.logerr(e)
            return SnapdStopResponse(
                False, f"Something went wrong while stoping '{req.service}': {e}"
            )

        rospy.logdebug(stop_response)

        check_change_response = snap_http.check_change(stop_response.change)

        rospy.logdebug(check_change_response)

        while check_change_response.result["status"] == "Doing":
            rospy.sleep(0.1)
            check_change_response = snap_http.check_change(stop_response.change)
            rospy.logdebug(check_change_response)

        return SnapdStopResponse(True, f"Service '{req.service}' stopped")
