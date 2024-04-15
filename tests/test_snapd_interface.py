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

from unittest import mock, TestCase

from snap_http import SnapdResponse
from snap_http.http import SnapdHttpException

import rclpy

from scripts.ros2_snapd import Ros2SnapdNode
from ros2_snapd.srv import SnapdList, SnapdRestart, SnapdStart, SnapdStop


class TestSnapdInterface(TestCase):

    @classmethod
    def setUpClass(self):
        rclpy.init()

        foo = SnapdList.Request()

        assert(foo)

        self.node = Ros2SnapdNode()

    @mock.patch("snap_http.get_apps")
    def test_list_callback_empty(self, mocked_get_apps):
        mocked_get_apps.return_value = SnapdResponse(
            type="", status_code="", status="", result=[]
        )

        response = SnapdList.Response()
        response = self.node._list_callback(SnapdList.Request(), response)

        assert response == SnapdList.Response(
            success=True, message="", services=[]
        )

    @mock.patch("snap_http.get_apps")
    def test_list_callback(self, mocked_get_apps):
        mocked_get_apps.return_value = SnapdResponse(
            type="", status_code="", status="", result=[
                {"snap": "foo", "name": "srv"},
                {"snap": "bar", "name": "srv"},
            ]
        )

        response = SnapdList.Response()
        response = self.node._list_callback(SnapdList.Request(), response)

        assert response == SnapdList.Response(
            success=True, message="", services=["foo.srv", "bar.srv"]
        )

    @mock.patch("snap_http.get_apps")
    def test_list_callback_raise(self, mocked_get_apps):
        mocked_get_apps.side_effect = SnapdHttpException()

        response = SnapdList.Response()
        response = self.node._list_callback(SnapdList.Request(), response)

        assert response == SnapdList.Response(
            success=False,
            message="Something went wrong while querying for services",
            services=[]
        )

    @mock.patch("scripts.ros2_snapd._EXCLUSION_LIST", ["bar.srv"])
    @mock.patch("snap_http.get_apps")
    def test_list_exclusion_list(self, mocked_get_apps):
        mocked_get_apps.return_value = SnapdResponse(
            type="", status_code="", status="", result=[
                {"snap": "foo", "name": "srv"},
                {"snap": "bar", "name": "srv"},
            ]
        )

        response = SnapdList.Response()
        response = self.node._list_callback(SnapdList.Request(), response)

        assert "bar.srv" not in response.services

    @mock.patch("snap_http.start")
    def test_start_callback_raise(self, mocked_start):
        error_message = "nop"
        service_name = "foo"
        mocked_start.side_effect = SnapdHttpException(error_message)

        response = SnapdStart.Response()
        response = self.node._start_callback(
            SnapdStart.Request(service=service_name), response
        )

        assert response == SnapdStart.Response(
            success=False,
            message=f"Something went wrong while starting '{service_name}': {error_message}",
        )

        response = SnapdStart.Response()
        response = self.node._start_callback(SnapdStart.Request(), response)

        assert response == SnapdStart.Response(
            success=False,
            message=f"Something went wrong while starting '': {error_message}",
        )

    @mock.patch("scripts.ros2_snapd._EXCLUSION_LIST", ["foo.srv"])
    @mock.patch("snap_http.start")
    def test_start_callback_exclusion(self, mocked_start):
        service_name = "foo.srv"
        response = SnapdStart.Response()
        response = self.node._start_callback(
            SnapdStart.Request(service=service_name), response
        )

        assert response == SnapdStart.Response(
            success=False,
            message=f"Cannot start '{service_name}'",
        )

    @mock.patch("snap_http.check_change")
    @mock.patch("snap_http.start")
    def test_start_callback(self, mocked_start, mocked_check_change):
        mocked_start.return_value = SnapdResponse(
            type="", status_code="", status="", result=[]
        )

        mocked_check_change.return_value = SnapdResponse(
            type="", status_code="", status="", result={"status": "ok"}
        )

        response = SnapdStart.Response()
        response = self.node._start_callback(SnapdStart.Request(service="foo"), response)

        assert response == SnapdStart.Response(
            success=True, message="Service 'foo' started"
        )

    @mock.patch("snap_http.stop")
    def test_stop_callback_raise(self, mocked_stop):
        error_message = "nop"
        service_name = "foo"
        mocked_stop.side_effect = SnapdHttpException(error_message)

        response = SnapdStop.Response()
        response = self.node._stop_callback(
            SnapdStop.Request(service=service_name), response
        )

        assert response == SnapdStop.Response(
            success=False,
            message=f"Something went wrong while stopping '{service_name}': {error_message}",
        )

        response = self.node._stop_callback(SnapdStop.Request(), response)

        assert response == SnapdStop.Response(
            success=False,
            message=f"Something went wrong while stopping '': {error_message}",
        )

    @mock.patch("scripts.ros2_snapd._EXCLUSION_LIST", ["foo.srv"])
    @mock.patch("snap_http.stop")
    def test_stop_callback_exclusion(self, mocked_stop):
        service_name = "foo.srv"
        response = SnapdStop.Response()
        response = self.node._stop_callback(
            SnapdStop.Request(service=service_name), response
        )

        assert response == SnapdStop.Response(
            success=False,
            message=f"Cannot stop '{service_name}'",
        )

    @mock.patch("snap_http.check_change")
    @mock.patch("snap_http.stop")
    def test_stop_callback(self, mocked_stop, mocked_check_change):
        mocked_stop.return_value = SnapdResponse(
            type="", status_code="", status="", result=[]
        )

        mocked_check_change.return_value = SnapdResponse(
            type="", status_code="", status="", result={"status": "ok"}
        )

        response = SnapdStop.Response()
        response = self.node._stop_callback(SnapdStop.Request(service="foo"), response)

        assert type(response) == SnapdStop.Response

        assert response == SnapdStop.Response(
            success=True, message="Service 'foo' stopped"
        )

    @mock.patch("snap_http.restart")
    def test_restart_callback_raise(self, mocked_restart):
        error_message = "nop"
        service_name = "foo"
        mocked_restart.side_effect = SnapdHttpException(error_message)

        response = SnapdRestart.Response()
        response = self.node._restart_callback(
            SnapdRestart.Request(service=service_name), response
        )

        assert response == SnapdRestart.Response(
            success=False,
            message=f"Something went wrong while restarting '{service_name}': {error_message}",
        )

        response = self.node._restart_callback(SnapdRestart.Request(), response)

        assert response == SnapdRestart.Response(
            success=False,
            message=f"Something went wrong while restarting '': {error_message}",
        )

    @mock.patch("scripts.ros2_snapd._EXCLUSION_LIST", ["foo.srv"])
    @mock.patch("snap_http.restart")
    def test_restart_callback_exclusion(self, mocked_restart):
        service_name = "foo.srv"
        response = SnapdRestart.Response()
        response = self.node._restart_callback(
            SnapdRestart.Request(service=service_name), response
        )

        assert response == SnapdRestart.Response(
            success=False,
            message=f"Cannot restart '{service_name}'",
        )

    @mock.patch("snap_http.check_change")
    @mock.patch("snap_http.restart")
    def test_restart_callback(self, mocked_restart, mocked_check_change):
        mocked_restart.return_value = SnapdResponse(
            type="", status_code="", status="", result=[]
        )

        mocked_check_change.return_value = SnapdResponse(
            type="", status_code="", status="", result={"status": "ok"}
        )

        response = SnapdRestart.Response()
        response = self.node._restart_callback(
            SnapdRestart.Request(service="foo"), response
        )

        assert type(response) == SnapdRestart.Response

        assert response == SnapdRestart.Response(
            success=True, message="Service 'foo' restarted"
        )
