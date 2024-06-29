from module.base.base import ModuleBase


class GGData(ModuleBase):
    def __init__(self, config):
        self.config = config
        self.ggdata = {
            'name': self.config.config_name,
            'gg_restart': self.config.cross_get('GGManager.GGManager.RestartEverytime', default=True),
            'gg_on': False
        }
        try:
            if self.get_data('name') != self.config.config_name:
                raise ValueError
        except(ValueError, KeyError):
            self.config.cross_set('GGManager.Storage.Storage', self.ggdata)

    def get_data(self, target=None):
        return self.config.cross_get(f'GGManager.Storage.Storage.{target}', default=None)

    def set_data(self, target=None, value=None):
        self.config.cross_set(f'GGManager.Storage.Storage.{target}', value)
