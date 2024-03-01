import pytest
from textual.command import CommandPalette
from textual.widgets import Button

from django_migrations_tui.tui.app import Format, MigrationsApp
from django_migrations_tui.tui.confirmation import ConfirmationScreen


@pytest.fixture
def app(event_loop):
    return MigrationsApp(format=Format.LIST)


def confiration_screen_is_open(app):
    return isinstance(app.children[0], ConfirmationScreen)


def command_is(app, command):
    return app.children[0].command == command


def get_widgets(app):
    return app.children[0].children[0].children


@pytest.mark.django_db
async def test_toggle_view_action(app):
    async with app.run_test() as pilot:
        widgets = get_widgets(pilot.app)
        tree = widgets[1]

        assert tree.format == Format.LIST
        await pilot.press("v")
        assert tree.format == Format.PLAN


@pytest.mark.django_db
async def test_toggle_logs_action(app):
    async with app.run_test() as pilot:
        widgets = get_widgets(pilot.app)
        log_widget = widgets[2]

        assert log_widget.display is False, "Logs should be hidden by default"
        await pilot.press("l")
        assert log_widget.display is True, "Logs should be visible"
        await pilot.press("l")
        assert log_widget.display is False, "Logs should be hidden"


@pytest.mark.django_db
async def test_migrate_action(app):
    async with app.run_test() as pilot:
        await pilot.press("m")
        assert confiration_screen_is_open(pilot.app), "Confirmation screen should open"
        assert command_is(
            pilot.app, "[bold cyan]python manage.py migrate"
        ), "Command should be the migrate command"

        migrate_button = get_widgets(pilot.app)[1]
        assert isinstance(migrate_button, Button)
        assert migrate_button.label.__str__() == "Migrate"

        await pilot.click("#yes")  # "Click on the Migrate button"
        assert not confiration_screen_is_open(
            pilot.app
        ), "Confirmation screen should be dismissed"

        widgets = get_widgets(pilot.app)
        log_widget = widgets[2]
        assert log_widget.display is True, "Logs should be visible"
        logs = [line.text.__str__() for line in log_widget.lines]
        assert (
            "Running python manage.py migrate" in logs
        ), "Logs should contain the command"


@pytest.mark.django_db
async def test_migrate_app_action(app):
    async with app.run_test() as pilot:
        await pilot.press("down")
        await pilot.press("m")
        assert confiration_screen_is_open(pilot.app), "Confirmation screen should open"
        assert command_is(
            pilot.app, "[bold cyan]python manage.py migrate admin"
        ), "Command should contain the app name"

        await pilot.click("#yes")  # "Click on the Migrate button"
        widgets = get_widgets(pilot.app)
        log_widget = widgets[2]
        assert log_widget.display is True, "Logs should be visible"

        logs = [line.text.__str__() for line in log_widget.lines]
        assert (
            "Running python manage.py migrate admin" in logs
        ), "Logs should contain the command"


@pytest.mark.django_db
async def test_migrate_migration_action(app):
    async with app.run_test() as pilot:
        await pilot.press("down")
        await pilot.press("enter")
        await pilot.press("down")
        await pilot.press("m")

        assert confiration_screen_is_open(pilot.app), "Confirmation screen should open"
        assert command_is(
            pilot.app, "[bold cyan]python manage.py migrate admin 0001_initial"
        ), "Command should contain the migration name"

        await pilot.click("#yes")  # "Click on the Migrate button"
        widgets = get_widgets(pilot.app)
        log_widget = widgets[2]
        assert log_widget.display is True, "Logs should be visible"

        logs = [line.text.__str__() for line in log_widget.lines]
        assert (
            "Running python manage.py migrate admin 0001_initial" in logs
        ), "Logs should contain the command"


@pytest.mark.django_db
async def test_fake_migrate_action(app):
    async with app.run_test() as pilot:
        await pilot.press("f")

        assert confiration_screen_is_open(pilot.app), "Confirmation screen should open"
        assert command_is(
            pilot.app, "[bold cyan]python manage.py migrate --fake"
        ), "Command should be the fake migrate command"


@pytest.mark.django_db
async def test_revert_migration_action(app):
    async with app.run_test() as pilot:
        await pilot.press("r")

        widgets = get_widgets(pilot.app)
        log_widget = widgets[2]
        assert log_widget.display is True, "Logs should be visible"

        logs = [line.text.__str__() for line in log_widget.lines]
        assert logs == ["Select an app to revert."], "Revert should work only on apps"

        await pilot.press("down")
        await pilot.press("r")
        assert confiration_screen_is_open(pilot.app), "Confirmation screen should open"
        assert command_is(
            pilot.app, "[bold cyan]python manage.py migrate admin zero"
        ), "Command should contain the app name followed by zero"


@pytest.mark.django_db
async def test_vim_keybindings(app):
    async with app.run_test() as pilot:
        widgets = get_widgets(pilot.app)
        tree = widgets[1]

        assert tree.cursor_node.label.__str__() == "migrations (18/18)"
        await pilot.press("j")
        assert (
            tree.cursor_node.label.__str__() == "admin (3/3)"
        ), "Selction should go down"
        await pilot.press("k")
        assert (
            tree.cursor_node.label.__str__() == "migrations (18/18)"
        ), "Selection should go up"

        await pilot.press("G")
        assert (
            tree.cursor_node.label.__str__() == "sessions (1/1)"
        ), "Selection should go the last app"

        await pilot.press("ctrl+home")
        assert tree.cursor_node.label.__str__() == "migrations (18/18)"


@pytest.mark.django_db
async def test_search_select(app):
    async with app.run_test() as pilot:
        assert not CommandPalette.is_open(pilot.app), "Command palette should be open"
        await pilot.press("ctrl+backslash")
        assert CommandPalette.is_open(pilot.app), "Command palette should be open"
