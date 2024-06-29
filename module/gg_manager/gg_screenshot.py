import uiautomator2 as u2
from module.ocr.ocr import Digit
from module.logger import logger
from module.base.base import ModuleBase
from module.handler.login import LoginHandler
from module.exception import GameStuckError, GameTooManyClickError
from module.gg_manager.gg_data import GGData
from module.handler.assets import *
from module.gg_manager.assets import *
from module.ui.assets import *
from module.ui_white.assets import *
from module.meowfficer.assets import *
from module.os_ash.assets import ASH_QUIT
from module.raid.assets import RPG_HOME
from module.combat.assets import GET_ITEMS_1

OCR_GG_FOLD = Digit(OCR_GG_FOLD, name='OCR_GG_FOLD', letter=(222, 228, 227), threshold=255)
OCR_GG_FOLD_CHECK = Digit(OCR_GG_FOLD_CHECK, name= 'OCR_GG_FOLD_CHECK', letter=(222, 228, 227), threshold=255)

class GGScreenshot(ModuleBase):
    count = 0
    method = [REWARD_GOTO_MAIN, GOTO_MAIN, MAIN_GOTO_BUILD,
              MAIN_GOTO_BUILD_WHITE, DORM_CHECK, MEOWFFICER_FORT_ENTER,
              ASH_QUIT, GET_ITEMS_1, RPG_HOME]

    def __init__(self, config, device):
        super().__init__(config, device)
        self.config = config
        self.device = device
        self.u2 = u2.connect_usb(self.device.serial)
        self.gg_package_name = self.config.cross_get('GGManager.GGManager.GGPackageName')
        self.gg_action = self.config.cross_get('GGManager.GGManager.GGAction')
        self.path = self.config.cross_get('GGManager.GGManager.GGLuapath')
        self.path_record = self.config.cross_get('GGManager.GGManager.GGLuapathRecord')
        self.luapath = "/sdcard/Alarms/Multiplier.lua"

    def _enter_gg(self):
        """
        Page:
            in: any
            out: any GG
        """
        skip_first_screenshot = True
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.sleep(0.5)
                self.device.screenshot()
            if self.appear(self.method[int(self.count)], offset=(20, 20)) and \
                  self.method[int(self.count)].match_appear_on(self.device.image):
                self.device.click(GG_ENTER_POS)
                continue
            if self.appear(GG_CONFIRM, offset=(20, 20)):
                logger.hr('Enter GG')
                logger.info('Entered GG')
                return True

    def enter_gg(self):
        self._enter_gg()
        logger.hr('Enter APP State')
        skip_first_screenshot = True
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.sleep(0.5)
                self.device.screenshot()
            if self.appear(GG_APP_CHOOSE1, offset=(20, 20)):
                if self.appear_then_click(GG_APP_CHOOSE0, offset=(20, 20), interval=1):
                    pass
                else:
                    self.device.click(GG_APP_CHOOSE1)
                logger.info('APP Choose')
                continue
            if self.appear(GG_APP_ENTER, offset=(20, 20)) and \
                GG_APP_ENTER.match_appear_on(self.device.image):
                logger.info('APP Enter')
                return True
            if not self.appear(GG_APP_ENTER, offset=(20, 20)) and \
                self.appear(GG_SEARCH_MODE_CONFIRM, offset=(10, 10)) and \
                    GG_SEARCH_MODE_CONFIRM.match_appear_on(self.device.image):
                logger.info('Select APP')
                self.device.click(GG_APP_RECHOOSE)
                continue
            if self.appear(GG_NOTRUN, offset=(20, 20)):
                self.gg_restart()
                self.device.sleep(0.5)
                self.device.screenshot()
                self.gg_open()
                self._enter_gg()
                continue

    def _gg_enter_script(self):
        """
        Page:
            in: any GG
            out: GG ready to start script
        """
        logger.hr('Select Script')
        skip_first_screenshot = True
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.sleep(0.5)
                self.device.screenshot()
            if self.appear(GG_SEARCH_MODE_CONFIRM, offset=(10, 10)) and \
                GG_SEARCH_MODE_CONFIRM.match_appear_on(self.device.image):
                self.device.click(GG_SCRIPT_ENTER_POS)
                logger.info('Enter script choose')
                continue
            if self.appear(GG_SCRIPT_ENTER_CONFIRM, offset=(20, 20)):
                self.gg_lua()
                logger.hr('Lua execute')
                return True

    def gg_enter_script(self):
        self._gg_enter_script()
        skip_first_screenshot = True
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.sleep(0.5)
                self.device.screenshot()
            if self.appear_then_click(GG_SCRIPT_START, offset=(10, 10), interval=1):
                continue
            if self.appear_then_click(GG_SCRIPT_MENU_A, offset=(20, 20), interval=1):
                continue
            if self.appear(GG_SCRIPT_START_PROCESS, offset=(20, 20)):
                return True
            if self.appear_then_click(GG_STOP, offset=(20, 20), interval=1):
                self.gg_restart()
                self.gg_open()
                self.enter_gg()
                continue

    def gg_handle_factor(self):
        """
        Page:
            in: GG input panel
            out:factor set(Not ensured yet)
        """
        number = [
            GG_SCRIPT_PANEL_NUM0,
            GG_SCRIPT_PANEL_NUM1,
            GG_SCRIPT_PANEL_NUM2,
            GG_SCRIPT_PANEL_NUM3,
            GG_SCRIPT_PANEL_NUM4,
            GG_SCRIPT_PANEL_NUM5,
            GG_SCRIPT_PANEL_NUM6,
            GG_SCRIPT_PANEL_NUM7,
            GG_SCRIPT_PANEL_NUM8,
            GG_SCRIPT_PANEL_NUM9,
        ]
        self.wait_until_appear(GG_SCRIPT_START_PROCESS, skip_first_screenshot=True)
        logger.hr('Factor Input')
        if (isinstance(self.factor, int) == True or isinstance(self.factor, float) == True) and (1 <= self.factor <= 1000):
            logger.attr('Factor', self.factor)
            while 1:
                self.device.sleep(0.5)
                self.device.screenshot()
                FOLD = OCR_GG_FOLD.ocr(self.device.image)
                if FOLD != None:
                    break
            if self.factor == int(FOLD):
                logger.info('Skip factor input')
                return True
            logger.hr('Re: Input')
            logger.info('Factor Reinput')
            for i in str(self.factor):
                self.appear_then_click(number[int(i)], interval=1)
            logger.info('Input success')
            logger.hr('Factor Check')
            count=0
            while 1:
                self.device.sleep(0.5)
                self.device.screenshot()
                FOLD_CHECK = OCR_GG_FOLD_CHECK.ocr(self.device.image)
                if self.factor == FOLD_CHECK:
                    logger.info('Check success')
                    break
                else:
                    count += 1
                    logger.warning('Check error')  
                    logger.info('Factor delete')
                    self.device.long_click(GG_SCRIPT_PANEL_DEL, duration=(1, 1.1))
                    if count >= 3:
                        logger.error('Check more failed,Try default factor will be run')
                        for i in str(200):
                            self.appear_then_click(number[int(i)], interval=1)
                        break
                    logger.info('Input again')
                    for i in str(self.factor):
                        self.appear_then_click(number[int(i)], interval=1)
        else:
            for _ in range(3):
                logger.error('Factor illegal')
            logger.warning('Try default factor will be run')
            from module.notify import handle_notify
            handle_notify(self.config.Error_OnePushConfig,
                          title=f"Alas <{self.config.config_name}> 输入的倍率不合法",
                          content=f"<{self.config.config_name}> 需要手动介入，输入的倍率不合法，将尝试默认倍率运行")
            logger.hr('Try again')
            for i in str(200):
                self.appear_then_click(number[int(i)], interval=1)

    def gg_script_run(self):
        """
        Page:
            in: GG factor set
            out: GG Menu
        """
        logger.hr('Execute')
        skip_first_screenshot = True
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.sleep(0.5)
                self.device.screenshot()
            if self.appear_then_click(GG_SCRIPT_START_PROCESS, offset=(20, 20), interval=1):
                continue
            if self.appear(GG_SCRIPT_START_CHECK, offset=(20, 20)):
                break
        logger.info('Waiting for end')
        self.wait_until_appear_then_click(GG_SCRIPT_END, offset=(20, 20))

    def gg_lua(self):
        if self.path != '' and self.gg_action == 'manual' and self.gg_package_name != 'com.':
            self.luapath = self.path
        if self.path_record:
            logger.hr('Skip lua path set')
            return True
        else:
            logger.hr('Lua path set')
            self.u2.send_keys(f'{self.luapath}')
            logger.info('Lua path set success')
            self.config.cross_set('GGManager.GGManager.GGLuapathRecord', value=True)

    def gg_push(self):
        if self.path_record:
            logger.hr('Skip push lua file')
        else:
            logger.hr('Push lua file')
            self.device.adb_push('bin/lua/Multiplier.lua', f'{self.luapath}')
            logger.info('Push success')

    def gg_open(self):
        skip_first_screenshot = True
        count = 0
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.sleep(0.5)
                self.device.screenshot()
            if count > 2:
                for i in range(len(self.method)):
                    if self.appear(self.method[int(i)], offset=(20, 20)) and \
                        self.method[int(i)].match_appear_on(self.device.image):
                        self.count = i
                        return True
            if self.appear_then_click(GG_SKIP0, offset=(20, 20), interval=1):
                count += 1
                continue
            if self.appear_then_click(GG_SKIP1, offset=(20, 20), interval=1):
                count += 1
                continue
            if self.appear(GG_START, offset=(20, 20)) and GG_START.match_appear_on(self.device.image):
                self.device.click(GG_START)
                count += 3
                continue
            if self.get_interval_timer(IDLE, interval=3).reached():
                if IDLE.match_luma(self.device.image, offset=(5, 5)):
                    logger.info(f'UI additional: {IDLE} -> {REWARD_GOTO_MAIN}')
                    self.device.click(REWARD_GOTO_MAIN)
                    self.get_interval_timer(IDLE).reset()
                    continue
            if self.appear(GG_NOTRUN, offset=(20, 20)):
                self.gg_restart()
                continue
            if (count > 2 and self.appear(LOGIN_CHECK, offset=(30, 30)) and LOGIN_CHECK.match_appear_on(self.device.image)) \
                or self.appear(LOGIN_GAME_UPDATE, offset=(30, 30)):
                self.handle_app_login()
                continue
            if self.appear_then_click(LOGIN_ANNOUNCE, offset=(30, 30), interval=5):
                continue

    def gg_start(self):
        logger.info(f'GG start: {self.gg_package_name}')
        self.u2.app_start(f'{self.gg_package_name}')

    def gg_stop(self):
        logger.info(f'GG stop: {self.gg_package_name}')
        self.u2.app_stop(f'{self.gg_package_name}')

    def gg_restart(self):
        logger.hr('GG Restart')
        self.device.app_start()
        self.gg_stop()
        self.device.sleep((1, 2))
        self.gg_start()

    def handle_app_login(self):
        for _ in range(3):
            self.device.stuck_record_clear()
            self.device.click_record_clear()
            try:
                LoginHandler(self.config, self.device)._handle_app_login()
                return True
            except (GameTooManyClickError, GameStuckError) as e:
                logger.warning(e)
                self.device.app_stop()
                self.device.app_start()
                continue
        logger.critical('Login failed more than 3')
        logger.critical('Azur Lane server may be under maintenance, or you may lost network connection')
        raise GameStuckError

    def run(self, factor):
        self.factor = factor
        if self.gg_package_name == 'com.':
            logger.critical('GG package name is None, please check your config')
            exit(1)
        self.gg_push()
        self.gg_stop()
        self.gg_start()
        self.gg_open()
        self.enter_gg()
        self.gg_enter_script()
        self.gg_handle_factor()
        self.gg_script_run()
        GGData(self.config).set_data(target='gg_on', value=True)
        logger.attr('GG', 'Enabled')
        self.gg_stop()
