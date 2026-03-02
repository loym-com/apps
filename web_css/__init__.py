from . import models


def uninstall_hook(env):
    env["res.config.settings"].reset_scss()
