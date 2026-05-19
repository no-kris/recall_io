from app.config import config


def test_config_password_masking():
    """
    Ensure database password is not readbale in string representation.
    """
    config_repr = repr(config)
    assert "DB_PASSWORD" not in config_repr
    assert config.DB_PASSWORD not in config_repr
