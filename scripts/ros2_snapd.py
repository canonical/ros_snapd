#!/usr/bin/env python3
#
# Copyright 2024 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import snap_http

from ros_snapd_interfaces.srv import SnapdList, SnapdRestart, SnapdStart, SnapdStop

import rclpy
from rclpy.node import Node

import time


# Necessary to use the snap socket for `ros-snapd-support` interface.
snap_http.http.SNAPD_SOCKET = "/run/snapd-snap.socket"


_EXCLUSION_LIST = [
    "lxd.activate",
    "lxd.daemon",
    "lxd.user-daemon",
    "ros-snapd.ros-snapd",
    "ros2-snapd.ros2-snapd",
]


class Ros2SnapdNode(Node):
    def __init__(self):
        super().__init__("ros2_snapd")
        self.srv = self.create_service(SnapdList, "~/list", self._list_callback)
        self.srv = self.create_service(
            SnapdRestart, "~/restart", self._restart_callback
        )
        self.srv = self.create_service(SnapdStart, "~/start", self._start_callback)
        self.srv = self.create_service(SnapdStop, "~/stop", self._stop_callback)

    def _list_callback(self, request, response):
        """Service 'list' callback."""
        self.get_logger().debug("Incoming request to list services")

        try:
            list_response = snap_http.get_apps(services_only=True)
        except snap_http.http.SnapdHttpException as e:
            self.get_logger().error(str(e))
            response.success = False
            response.message = "Something went wrong while querying for services"
            return response

        self.get_logger().debug(str(list_response))

        for it in list_response.result:
            service_name = f"{it['snap']}.{it['name']}"
            if service_name not in _EXCLUSION_LIST:
                response.services.append(service_name)

        self.get_logger().debug(f"Services: {response.services}")

        response.success = True

        return response

    def _restart_callback(self, request, response):
        """Service 'restart' callback."""
        self.get_logger().debug(
            f"Incoming request to restart service '{request.service}'"
        )

        if request.service in _EXCLUSION_LIST:
            response.success = False
            response.message = f"Cannot restart '{request.service}'"
            return response

        restart_response = None
        try:
            restart_response = snap_http.restart(name=request.service)
        except snap_http.http.SnapdHttpException as e:
            self.get_logger().error(str(e))
            response.success = False
            response.message = (
                f"Something went wrong while restarting '{request.service}': {e}"
            )
            return response

        self.get_logger().debug(str(restart_response))

        check_change_response = snap_http.check_change(restart_response.change)

        self.get_logger().debug(str(check_change_response))

        while check_change_response.result["status"] == "Doing":
            time.sleep(0.1)
            check_change_response = snap_http.check_change(restart_response.change)
            self.get_logger().debug(str(check_change_response))

        response.success = True
        response.message = f"Service '{request.service}' restarted"

        return response

    def _start_callback(self, request, response):
        """Service 'start' callback."""
        self.get_logger().debug(f"Incoming request to start service {request.service}")

        if request.service in _EXCLUSION_LIST:
            response.success = False
            response.message = f"Cannot start '{request.service}'"
            return response

        start_response = None
        try:
            start_response = snap_http.start(name=request.service)
        except snap_http.http.SnapdHttpException as e:
            self.get_logger().error(str(e))
            response.success = False
            response.message = (
                f"Something went wrong while starting '{request.service}': {e}"
            )
            return response

        self.get_logger().debug(str(start_response))

        check_change_response = snap_http.check_change(start_response.change)

        self.get_logger().debug(str(check_change_response))

        while check_change_response.result["status"] == "Doing":
            time.sleep(0.1)
            check_change_response = snap_http.check_change(start_response.change)
            self.get_logger().debug(str(check_change_response))

        response.success = True
        response.message = f"Service '{request.service}' started"

        return response

    def _stop_callback(self, request, response):
        """Service 'stop' callback."""
        self.get_logger().debug(f"Incoming request to stop service '{request.service}'")

        if request.service in _EXCLUSION_LIST:
            response.success = False
            response.message = f"Cannot stop '{request.service}'"
            return response

        stop_response = None
        try:
            stop_response = snap_http.stop(name=request.service)
        except snap_http.http.SnapdHttpException as e:
            self.get_logger().error(str(e))
            response.success = False
            response.message = (
                f"Something went wrong while stopping '{request.service}': {e}"
            )
            return response

        self.get_logger().debug(str(stop_response))

        check_change_response = snap_http.check_change(stop_response.change)

        self.get_logger().debug(str(check_change_response))

        while check_change_response.result["status"] == "Doing":
            time.sleep(0.1)
            check_change_response = snap_http.check_change(stop_response.change)
            self.get_logger().debug(str(check_change_response))

        response.success = True
        response.message = f"Service '{request.service}' stopped"

        return response


def main():
    rclpy.init()

    ros2_snapd_node = Ros2SnapdNode()

    rclpy.spin(ros2_snapd_node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
