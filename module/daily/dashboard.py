from module.logger import logger
from module.daily.dashboard_status import DashboardStatus

class DashboardUpdate(DashboardStatus):
    def dashboard_run(self):
        self.ui_goto_main()
        self.get_cube()
        self.ui_goto_main()
        self.ui_goto_shop()
        self.get_oilcoingem()
        if self.config.DashboardUpdate_Update:
            self.goto_shop()
        self.ui_goto_main()
        logger.info('Update Dashboard Data Finished')

    def goto_shop(self):
        self.ui_goto_shop()
        self.shop_tab.set(main=self, left=2)
        self.shop_nav.set(main=self, upper=2)
        logger.hr('Get Merit')
        self.get_merit()

        self.shop_tab.set(main=self, left=2)
        self.shop_nav.set(main=self, upper=3)
        logger.hr('Get GuildCoin')
        self.get_guild_coins()

        self.shop_tab.set(main=self, left=1)
        self.shop_nav.set(main=self, upper=2)
        logger.hr('Get Core')
        self.get_core()

        self.shop_tab.set(main=self, left=1)
        self.shop_nav.set(main=self, upper=3)
        logger.hr('Get Medal')
        self.get_medal()
        self.ui_goto_main()

    def run(self):
        self.dashboard_run()
        self.config.task_delay(server_update=True)
