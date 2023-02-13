from unittest.mock import Mock

from proton.vpn.app.gtk.widgets.main.main_widget import MainWidget

from proton.vpn.app.gtk.widgets.main.notification_bar import NotificationBar
from proton.vpn.app.gtk.widgets.main.notifications import Notifications


def test_main_widget_initially_shows_login_widget_if_the_user_did_not_log_in_yet():
    controller_mock = Mock()
    controller_mock.user_logged_in = False
    main_window_mock = Mock()

    main_widget = MainWidget(
        controller=controller_mock,
        main_window=main_window_mock
    )
    main_widget.initialize_visible_widget()

    assert main_widget.active_widget is main_widget.login_widget
    assert main_window_mock.header_bar.menu.logout_enabled is False


def test_main_widget_initially_shows_vpn_widget_if_the_user_had_already_logged_in():
    controller_mock = Mock()
    controller_mock.user_logged_in = True
    main_window_mock = Mock()

    main_widget = MainWidget(
        controller=controller_mock,
        main_window=main_window_mock
    )
    main_widget.initialize_visible_widget()

    assert main_widget.active_widget is main_widget.vpn_widget
    assert main_window_mock.header_bar.menu.logout_enabled is True


def test_main_widget_switches_from_login_to_vpn_widget_after_login():
    main_window_mock = Mock()
    main_widget = MainWidget(
        controller=Mock(),
        main_window=main_window_mock
    )
    main_widget.active_widget = main_widget.login_widget

    main_widget.login_widget.emit("user-logged-in")

    assert main_widget.active_widget is main_widget.vpn_widget
    assert main_window_mock.header_bar.menu.logout_enabled is True


def test_main_widget_switches_from_vpn_to_login_widget_after_logout():
    main_window_mock = Mock()
    main_widget = MainWidget(
        controller=Mock(),
        main_window=main_window_mock
    )
    main_widget.active_widget = main_widget.vpn_widget

    logout_callback = main_window_mock.header_bar.menu.connect.call_args.args[1]
    logout_callback()

    assert main_widget.active_widget is main_widget.login_widget
    assert main_window_mock.header_bar.menu.logout_enabled is False


def test_main_widget_switches_to_login_widget_when_session_expired():
    main_window_mock = Mock()
    notifications_mock = Mock()
    notifications_mock.notification_bar = NotificationBar()
    main_widget = MainWidget(
        controller=Mock(),
        main_window=main_window_mock,
        notifications=notifications_mock
    )
    main_widget.active_widget = main_widget.vpn_widget
    main_widget.session_expired()

    assert main_widget.active_widget is main_widget.login_widget
    notifications_mock.show_error_dialog.assert_called_once_with(
        title=MainWidget.SESSION_EXPIRED_ERROR_TITLE,
        message=MainWidget.SESSION_EXPIRED_ERROR_MESSAGE
    )
    assert main_window_mock.header_bar.menu.logout_enabled is False


def test_hide_loading_widget_after_vpn_widget_is_ready():
    """The main widget should hide the loading widget whenever the vpn
    widget is ready."""
