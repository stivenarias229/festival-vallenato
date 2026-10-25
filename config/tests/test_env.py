from config.settings import env_str


def test_env_str_quita_comillas_y_espacios(monkeypatch):
    monkeypatch.setenv("EMAIL_HOST_USER", "  '6d1456f80a369c'  ")
    assert env_str("EMAIL_HOST_USER") == "6d1456f80a369c"
