from .menu import get_main_menu_kb


def get_client_kb():
    return get_main_menu_kb("client")


__all__ = ["get_main_menu_kb", "get_client_kb"]