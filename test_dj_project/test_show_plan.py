import pytest


@pytest.mark.django_db
def test_migration_plan(migrations_plan):
    assert migrations_plan == [
        "[X]  contenttypes.0001_initial",
        "[X]  auth.0001_initial",
        "[X]  admin.0001_initial",
        "[X]  admin.0002_logentry_remove_auto_add",
        "[X]  admin.0003_logentry_add_action_flag_choices",
        "[X]  contenttypes.0002_remove_content_type_name",
        "[X]  auth.0002_alter_permission_name_max_length",
        "[X]  auth.0003_alter_user_email_max_length",
        "[X]  auth.0004_alter_user_username_opts",
        "[X]  auth.0005_alter_user_last_login_null",
        "[X]  auth.0006_require_contenttypes_0002",
        "[X]  auth.0007_alter_validators_add_error_messages",
        "[X]  auth.0008_alter_user_username_max_length",
        "[X]  auth.0009_alter_user_last_name_max_length",
        "[X]  auth.0010_alter_group_name_max_length",
        "[X]  auth.0011_update_proxy_permissions",
        "[X]  auth.0012_alter_user_first_name_max_length",
        "[X]  sessions.0001_initial",
    ]


@pytest.mark.django_db
def test_migrations_plan_with_verbosity_2(migrations_plan_verbosity_2):
    assert migrations_plan_verbosity_2 == [
        "[X]  contenttypes.0001_initial",
        "[X]  auth.0001_initial ... (contenttypes.0001_initial)",
        "[X]  admin.0001_initial ... (auth.0001_initial, contenttypes.0001_initial)",
        "[X]  admin.0002_logentry_remove_auto_add ... (admin.0001_initial)",
        "[X]  admin.0003_logentry_add_action_flag_choices ... (admin.0002_logentry_remove_auto_add)",
        "[X]  contenttypes.0002_remove_content_type_name ... (contenttypes.0001_initial)",
        "[X]  auth.0002_alter_permission_name_max_length ... (auth.0001_initial)",
        "[X]  auth.0003_alter_user_email_max_length ... (auth.0002_alter_permission_name_max_length)",
        "[X]  auth.0004_alter_user_username_opts ... (auth.0003_alter_user_email_max_length)",
        "[X]  auth.0005_alter_user_last_login_null ... (auth.0004_alter_user_username_opts)",
        "[X]  auth.0006_require_contenttypes_0002 ... (auth.0005_alter_user_last_login_null, contenttypes.0002_remove_content_type_name)",
        "[X]  auth.0007_alter_validators_add_error_messages ... (auth.0006_require_contenttypes_0002)",
        "[X]  auth.0008_alter_user_username_max_length ... (auth.0007_alter_validators_add_error_messages)",
        "[X]  auth.0009_alter_user_last_name_max_length ... (auth.0008_alter_user_username_max_length)",
        "[X]  auth.0010_alter_group_name_max_length ... (auth.0009_alter_user_last_name_max_length)",
        "[X]  auth.0011_update_proxy_permissions ... (auth.0010_alter_group_name_max_length, contenttypes.0002_remove_content_type_name)",
        "[X]  auth.0012_alter_user_first_name_max_length ... (auth.0011_update_proxy_permissions)",
        "[X]  sessions.0001_initial",
    ]
