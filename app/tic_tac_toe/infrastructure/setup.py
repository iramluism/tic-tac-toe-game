import inject
from tic_tac_toe.infrastructure.dependencies import DEPENDENCIES


def setup_dependencies(binder):
    for interface, implementation in DEPENDENCIES.items():
        binder.bind(interface, implementation)


def setup_app():
    inject.configure(setup_dependencies)
