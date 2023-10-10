import pytest
from django.apps import apps


@pytest.mark.django_db
def test_apps_list(migrations_list):
    models = apps.get_models()
    apps_with_models = set(model._meta.app_label for model in models)
    apps_with_migrations = set(migration.app_name for migration in migrations_list)
    assert (
        apps_with_models
        == apps_with_migrations
        == {"sessions", "auth", "admin", "contenttypes"}
    )


@pytest.mark.django_db
def test_admin_migrations_list(migrations_list, recorded_migrations):
    admin_migrations_list = next(
        migration for migration in migrations_list if migration.app_name == "admin"
    )
    admin_applied_migrations = [
        migration for migration in recorded_migrations if migration[0] == "admin"
    ]
    assert admin_migrations_list.applied_count == len(admin_applied_migrations) == 3
    admin_migrations = [migration for migration in admin_migrations_list.migrations]
    assert admin_migrations == [
        " [X] 0001_initial",
        " [X] 0002_logentry_remove_auto_add",
        " [X] 0003_logentry_add_action_flag_choices",
    ]


@pytest.mark.django_db
def test_auth_migrations_list(migrations_list, recorded_migrations):
    auth_migrations_list = next(
        migration for migration in migrations_list if migration.app_name == "auth"
    )
    auth_applied_migrations = [
        migration for migration in recorded_migrations if migration[0] == "auth"
    ]
    assert auth_migrations_list.applied_count == len(auth_applied_migrations) == 12
    auth_migrations = [migration for migration in auth_migrations_list.migrations]
    assert auth_migrations == [
        " [X] 0001_initial",
        " [X] 0002_alter_permission_name_max_length",
        " [X] 0003_alter_user_email_max_length",
        " [X] 0004_alter_user_username_opts",
        " [X] 0005_alter_user_last_login_null",
        " [X] 0006_require_contenttypes_0002",
        " [X] 0007_alter_validators_add_error_messages",
        " [X] 0008_alter_user_username_max_length",
        " [X] 0009_alter_user_last_name_max_length",
        " [X] 0010_alter_group_name_max_length",
        " [X] 0011_update_proxy_permissions",
        " [X] 0012_alter_user_first_name_max_length",
    ]


@pytest.mark.django_db
def test_contenttypes_migrations_list(migrations_list, recorded_migrations):
    contenttypes_migrations_list = next(
        migration
        for migration in migrations_list
        if migration.app_name == "contenttypes"
    )
    contenttypes_applied_migrations = [
        migration for migration in recorded_migrations if migration[0] == "contenttypes"
    ]
    assert (
        contenttypes_migrations_list.applied_count
        == len(contenttypes_applied_migrations)
        == 2
    )
    contenttypes_migrations = [
        migration for migration in contenttypes_migrations_list.migrations
    ]
    assert contenttypes_migrations == [
        " [X] 0001_initial",
        " [X] 0002_remove_content_type_name",
    ]


@pytest.mark.django_db
def test_sessions_migrations_list(migrations_list, recorded_migrations):
    sessions_migrations_list = next(
        migration for migration in migrations_list if migration.app_name == "sessions"
    )
    sessions_applied_migrations = [
        migration for migration in recorded_migrations if migration[0] == "sessions"
    ]
    assert (
        sessions_migrations_list.applied_count == len(sessions_applied_migrations) == 1
    )
    sessions_migrations = [
        migration for migration in sessions_migrations_list.migrations
    ]
    assert sessions_migrations == [" [X] 0001_initial"]
