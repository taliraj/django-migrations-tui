import pytest
from textual.widgets import Button

from django_migrations_tui.tui.app import Format, MigrationsApp
from django_migrations_tui.tui.confirmation import ConfirmationScreen


@pytest.fixture
def app():
    return MigrationsApp(format=Format.LIST)


@pytest.mark.django_db
async def test_toggle_view_action(app):
    async with app.run_test() as pilot:
        widgets = pilot.app.children[0].children[0].children
        tree = widgets[1]

        assert tree.format == Format.LIST
        await pilot.press("v")
        assert tree.format == Format.PLAN


@pytest.mark.django_db
async def test_toggle_logs_action(app):
    async with app.run_test() as pilot:
        widgets = pilot.app.children[0].children[0].children
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
        assert isinstance(
            pilot.app.children[0], ConfirmationScreen
        ), "Confirmation screen should be displayed"
        assert pilot.app.children[0].command == "[bold cyan]python manage.py migrate"

        migrate_button = pilot.app.children[0].children[0].children[1]
        assert isinstance(migrate_button, Button)
        assert migrate_button.label.__str__() == "Migrate"

        await pilot.click("#yes")  # "Click on the Migrate button"
        assert not isinstance(
            pilot.app.children[0], ConfirmationScreen
        ), "Confirmation screen should be dismissed"

        widgets = pilot.app.children[0].children[0].children
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
        assert isinstance(
            pilot.app.children[0], ConfirmationScreen
        ), "Confirmation screen should be displayed"
        assert (
            pilot.app.children[0].command == "[bold cyan]python manage.py migrate admin"
        ), "Command should conatin the app name"

        await pilot.click("#yes")  # "Click on the Migrate button"
        widgets = pilot.app.children[0].children[0].children
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

        assert isinstance(
            pilot.app.children[0], ConfirmationScreen
        ), "Confirmation screen should be displayed"
        assert (
            pilot.app.children[0].command
            == "[bold cyan]python manage.py migrate admin 0001_initial"
        ), "Command should contain the migration name"

        await pilot.click("#yes")  # "Click on the Migrate button"
        widgets = pilot.app.children[0].children[0].children
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

        assert isinstance(
            pilot.app.children[0], ConfirmationScreen
        ), "Confirmation screen should be displayed"
        assert (
            pilot.app.children[0].command
            == "[bold cyan]python manage.py migrate --fake"
        ), "Command should contain the migration name"


@pytest.mark.django_db
async def test_revert_migration_action(app):
    async with app.run_test() as pilot:
        await pilot.press("r")

        widgets = pilot.app.children[0].children[0].children
        log_widget = widgets[2]
        assert log_widget.display is True, "Logs should be visible"

        logs = [line.text.__str__() for line in log_widget.lines]
        assert logs == ["Select an app to revert."], "Revert should work only on apps"

        await pilot.press("down")
        await pilot.press("r")
        assert isinstance(
            pilot.app.children[0], ConfirmationScreen
        ), "Confirmation screen should be displayed"
        assert (
            pilot.app.children[0].command
            == "[bold cyan]python manage.py migrate admin zero"
        ), "Command should contain the app name followed by zero"
