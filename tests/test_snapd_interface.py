from unittest import mock, TestCase

from snap_http import SnapdResponse
from snap_http.http import SnapdHttpException

from ros_snapd.snapd_interface import RosSnapdNode
from ros_snapd_interfaces.srv import (
    SnapdList,
    SnapdListResponse,
    SnapdRestartRequest,
    SnapdRestartResponse,
    SnapdStartRequest,
    SnapdStartResponse,
    SnapdStopRequest,
    SnapdStopResponse,
)


class TestSnapdInterface(TestCase):

    @classmethod
    def setUpClass(self):
        self.node = RosSnapdNode()

    @mock.patch("snap_http.get_apps")
    def test_handle_list_empty(self, mocked_get_apps):
        mocked_get_apps.return_value = SnapdResponse(
            type="", status_code="", status="", result=[]
        )

        results = self.node._handle_list(SnapdList())

        assert results == SnapdListResponse(
            success=True, message="", services=[]
        )

    @mock.patch("snap_http.get_apps")
    def test_handle_list(self, mocked_get_apps):
        mocked_get_apps.return_value = SnapdResponse(
            type="", status_code="", status="", result=[
                {"snap": "foo", "name": "srv"},
                {"snap": "bar", "name": "srv"},
            ]
        )

        results = self.node._handle_list(SnapdList())

        assert results == SnapdListResponse(
            success=True, message="", services=["foo.srv", "bar.srv"]
        )

    @mock.patch("ros_snapd.snapd_interface._EXCLUSION_LIST", ["bar.srv"])
    @mock.patch("snap_http.get_apps")
    def test_list_exclusion_list(self, mocked_get_apps):
        mocked_get_apps.return_value = SnapdResponse(
            type="", status_code="", status="", result=[
                {"snap": "foo", "name": "srv"},
                {"snap": "bar", "name": "srv"},
            ]
        )

        results = self.node._handle_list(SnapdList())

        assert "bar.srv" not in results.services

    @mock.patch("snap_http.get_apps")
    def test_handle_list_raise(self, mocked_get_apps):
        mocked_get_apps.side_effect = SnapdHttpException()

        results = self.node._handle_list(SnapdList())

        assert results == SnapdListResponse(
            success=False,
            message="Something went wrong while querying for services",
            services=[]
        )

    @mock.patch("snap_http.start")
    def test_handle_start_raise(self, mocked_start):
        error_message = "nop"
        service_name = "foo"
        mocked_start.side_effect = SnapdHttpException(error_message)

        results = self.node._handle_start(SnapdStartRequest(service=service_name))

        assert results == SnapdStartResponse(
            success=False,
            message=f"Something went wrong while starting '{service_name}': {error_message}",
        )

        results = self.node._handle_start(SnapdStartRequest())

        assert results == SnapdStartResponse(
            success=False,
            message=f"Something went wrong while starting '': {error_message}",
        )

    @mock.patch("snap_http.check_change")
    @mock.patch("snap_http.start")
    def test_handle_start(self, mocked_start, mocked_check_change):
        mocked_start.return_value = SnapdResponse(
            type="", status_code="", status="", result=[]
        )

        mocked_check_change.return_value = SnapdResponse(
            type="", status_code="", status="", result={"status": "ok"}
        )

        results = self.node._handle_start(SnapdStartRequest(service="foo"))

        assert results == SnapdStartResponse(
            success=True, message="Service 'foo' started"
        )

    @mock.patch("ros_snapd.snapd_interface._EXCLUSION_LIST", ["foo.srv"])
    @mock.patch("snap_http.start")
    def test_start_callback_exclusion(self, mocked_start):
        service_name = "foo.srv"
        results = self.node._handle_start(SnapdStartRequest(service="foo.srv"))

        assert results == SnapdStartResponse(
            success=False, message=f"Cannot start '{service_name}'"
        )

    @mock.patch("snap_http.stop")
    def test_handle_stop_raise(self, mocked_stop):
        error_message = "nop"
        service_name = "foo"
        mocked_stop.side_effect = SnapdHttpException(error_message)

        results = self.node._handle_stop(SnapdStopRequest(service=service_name))

        assert results == SnapdStopResponse(
            success=False,
            message=f"Something went wrong while stopping '{service_name}': {error_message}",
        )

        results = self.node._handle_stop(SnapdStopRequest())

        assert results == SnapdStopResponse(
            success=False,
            message=f"Something went wrong while stopping '': {error_message}",
        )

    @mock.patch("snap_http.check_change")
    @mock.patch("snap_http.stop")
    def test_handle_stop(self, mocked_stop, mocked_check_change):
        mocked_stop.return_value = SnapdResponse(
            type="", status_code="", status="", result=[]
        )

        mocked_check_change.return_value = SnapdResponse(
            type="", status_code="", status="", result={"status": "ok"}
        )

        results = self.node._handle_stop(SnapdStopRequest(service="foo"))

        assert isinstance(results, SnapdStopResponse)

        assert results == SnapdStopResponse(
            success=True, message="Service 'foo' stopped"
        )

    @mock.patch("ros_snapd.snapd_interface._EXCLUSION_LIST", ["foo.srv"])
    @mock.patch("snap_http.stop")
    def test_stop_callback_exclusion(self, mocked_stop):
        service_name = "foo.srv"
        results = self.node._handle_stop(SnapdStopRequest(service="foo.srv"))

        assert results == SnapdStopResponse(
            success=False, message=f"Cannot stop '{service_name}'"
        )

    @mock.patch("snap_http.restart")
    def test_handle_restart_raise(self, mocked_restart):
        error_message = "nop"
        service_name = "foo"
        mocked_restart.side_effect = SnapdHttpException(error_message)

        results = self.node._handle_restart(SnapdRestartRequest(service=service_name))

        assert results == SnapdRestartResponse(
            success=False,
            message=f"Something went wrong while restarting '{service_name}': {error_message}",
        )

        results = self.node._handle_restart(SnapdRestartRequest())

        assert results == SnapdRestartResponse(
            success=False,
            message=f"Something went wrong while restarting '': {error_message}",
        )

    @mock.patch("snap_http.check_change")
    @mock.patch("snap_http.restart")
    def test_handle_restart(self, mocked_restart, mocked_check_change):
        mocked_restart.return_value = SnapdResponse(
            type="", status_code="", status="", result=[]
        )

        mocked_check_change.return_value = SnapdResponse(
            type="", status_code="", status="", result={"status": "ok"}
        )

        results = self.node._handle_restart(SnapdRestartRequest(service="foo"))

        assert isinstance(results, SnapdRestartResponse)

        assert results == SnapdRestartResponse(
            success=True, message="Service 'foo' restarted"
        )

    @mock.patch("ros_snapd.snapd_interface._EXCLUSION_LIST", ["foo.srv"])
    @mock.patch("snap_http.restart")
    def test_restart_callback_exclusion(self, mocked_restart):
        service_name = "foo.srv"
        results = self.node._handle_restart(SnapdRestartRequest(service="foo.srv"))

        assert results == SnapdRestartResponse(
            success=False, message=f"Cannot restart '{service_name}'"
        )
