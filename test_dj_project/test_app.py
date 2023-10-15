import pytest
from textual.widgets import Footer, Header

from django_migrations_tui.tui.app import Format, MigrationsApp
from django_migrations_tui.tui.logs import Log
from django_migrations_tui.tui.tree import Tree


@pytest.mark.django_db
async def test_list_format():
    app = MigrationsApp(format=Format.LIST)
    async with app.run_test() as pilot:
        widgets = pilot.app.children[0].children[0].children
        assert len(widgets) == 4

        assert isinstance(widgets[0], Header)
        assert isinstance(widgets[1], Tree)
        assert isinstance(widgets[2], Log)
        assert isinstance(widgets[3], Footer)

        header = widgets[0]
        assert header.screen_title == "Django Migrations TUI"

        tree = widgets[1]
        assert str(tree.root.label) == "migrations (18/18)"
        assert len(tree.root.children) == 4
        assert tree.root.children[0].label.__str__() == "admin (3/3)"
        assert tree.root.children[1].label.__str__() == "auth (12/12)"
        assert tree.root.children[2].label.__str__() == "contenttypes (2/2)"
        assert tree.root.children[3].label.__str__() == "sessions (1/1)"

        admin_migrations = tree.root.children[0]
        assert len(admin_migrations.children) == 3
        assert admin_migrations.children[0].label.__str__() == " [X] 0001_initial"
        assert (
            admin_migrations.children[1].label.__str__()
            == " [X] 0002_logentry_remove_auto_add"
        )
        assert (
            admin_migrations.children[2].label.__str__()
            == " [X] 0003_logentry_add_action_flag_choices"
        )

        auth_migrations = tree.root.children[1]
        assert len(auth_migrations.children) == 12
        assert auth_migrations.children[0].label.__str__() == " [X] 0001_initial"
        assert (
            auth_migrations.children[1].label.__str__()
            == " [X] 0002_alter_permission_name_max_length"
        )
        assert (
            auth_migrations.children[2].label.__str__()
            == " [X] 0003_alter_user_email_max_length"
        )
        assert (
            auth_migrations.children[3].label.__str__()
            == " [X] 0004_alter_user_username_opts"
        )
        assert (
            auth_migrations.children[4].label.__str__()
            == " [X] 0005_alter_user_last_login_null"
        )
        assert (
            auth_migrations.children[5].label.__str__()
            == " [X] 0006_require_contenttypes_0002"
        )
        assert (
            auth_migrations.children[6].label.__str__()
            == " [X] 0007_alter_validators_add_error_messages"
        )
        assert (
            auth_migrations.children[7].label.__str__()
            == " [X] 0008_alter_user_username_max_length"
        )
        assert (
            auth_migrations.children[8].label.__str__()
            == " [X] 0009_alter_user_last_name_max_length"
        )
        assert (
            auth_migrations.children[9].label.__str__()
            == " [X] 0010_alter_group_name_max_length"
        )
        assert (
            auth_migrations.children[10].label.__str__()
            == " [X] 0011_update_proxy_permissions"
        )
        assert (
            auth_migrations.children[11].label.__str__()
            == " [X] 0012_alter_user_first_name_max_length"
        )

        contenttypes_migrations = tree.root.children[2]
        assert len(contenttypes_migrations.children) == 2
        assert (
            contenttypes_migrations.children[0].label.__str__() == " [X] 0001_initial"
        )
        assert (
            contenttypes_migrations.children[1].label.__str__()
            == " [X] 0002_remove_content_type_name"
        )

        sessions_migrations = tree.root.children[3]
        assert len(sessions_migrations.children) == 1
        assert sessions_migrations.children[0].label.__str__() == " [X] 0001_initial"


@pytest.mark.django_db
async def test_plan_format():
    app = MigrationsApp(format=Format.PLAN)
    async with app.run_test() as pilot:
        widgets = pilot.app.children[0].children[0].children
        tree = widgets[1]

        assert str(tree.root.label) == "plan (18/18)"
        assert len(tree.root.children) == 18
