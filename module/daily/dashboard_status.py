from module.log_res import LogRes
from module.logger import logger
from module.base.utils import *
from module.ocr.ocr import Digit
from module.gacha.ui import GachaUI
from module.shop.ui import ShopUI
from module.campaign.assets import OCR_COIN, OCR_OIL, OCR_COIN_LIMIT, OCR_OIL_LIMIT
from module.shop.assets import SHOP_GEMS, SHOP_MEDAL, SHOP_MERIT, SHOP_GUILD_COINS, SHOP_CORE
from module.gacha.assets import BUILD_CUBE_COUNT

OCR_OIL = Digit(OCR_OIL, name='OCR_OIL', letter=(247, 247, 247), threshold=128)
OCR_COIN = Digit(OCR_COIN, name='OCR_COIN', letter=(239, 239, 239), threshold=128)
OCR_OIL_LIMIT = Digit(OCR_OIL_LIMIT, name='OCR_OIL_LIMIT', letter=(235, 235, 235), threshold=128)
OCR_COIN_LIMIT = Digit(OCR_COIN_LIMIT, name='OCR_COIN_LIMIT', letter=(239, 239, 239), threshold=128)
OCR_SHOP_GEMS = Digit(SHOP_GEMS, letter=(255, 243, 82), name='OCR_SHOP_GEMS')
OCR_BUILD_CUBE_COUNT = Digit(BUILD_CUBE_COUNT, letter=(255, 247, 247), threshold=64)
OCR_SHOP_MEDAL = Digit(SHOP_MEDAL, letter=(239, 239, 239), name='OCR_SHOP_MEDAL')
OCR_SHOP_MERIT = Digit(SHOP_MERIT, letter=(239, 239, 239), name='OCR_SHOP_MERIT')
OCR_SHOP_GUILD_COINS = Digit(SHOP_GUILD_COINS, letter=(255, 255, 255), name='OCR_SHOP_GUILD_COINS')
OCR_SHOP_CORE = Digit(SHOP_CORE, letter=(239, 239, 239), name='OCR_SHOP_CORE')


class DashboardStatus(ShopUI, GachaUI):
    def get_oilcoingem(self, skip_first_screenshot=True):
        _oil = {}
        _coin = {}
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            
            logger.hr('Get Oil')
            _oil = {
                'Value': OCR_OIL.ocr(self.device.image),
                'Limit': OCR_OIL_LIMIT.ocr(self.device.image)
            }
            oil = _oil['Value']
            logger.hr('Get Coin')
            _coin = {
                'Value': OCR_COIN.ocr(self.device.image),
                'Limit': OCR_COIN_LIMIT.ocr(self.device.image)
            }
            coin = _coin['Value']
            logger.hr('Get Gem')
            gem = OCR_SHOP_GEMS.ocr(self.device.image)
            if _oil['Value'] > 0:
                break
        logger.info(f'[Oil]{oil} [Coin]{coin} [Gem]{gem}')
        LogRes(self.config).Oil = _oil
        LogRes(self.config).Coin = _coin
        LogRes(self.config).Gem = gem
        self.config.update()

    def get_cube(self, skip_first_screenshot=True):
        logger.hr('Get Cube')
        self.ui_goto_gacha()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            cube = OCR_BUILD_CUBE_COUNT.ocr(self.device.image)
            if cube > 0:
                break
        logger.attr('Cube',cube)
        LogRes(self.config).Cube = cube
        self.config.update()

    def get_merit(self, skip_first_screenshot=True):
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            merit = OCR_SHOP_MERIT.ocr(self.device.image)
            if merit > 0:
                break
        logger.attr('Merit',merit)
        LogRes(self.config).Merit = merit
        self.config.update()

    def get_core(self, skip_first_screenshot=True):
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            core = OCR_SHOP_CORE.ocr(self.device.image)
            if core > 0:
                break
        logger.attr('Core',core)
        LogRes(self.config).Core = core
        self.config.update()

    def get_guild_coins(self, skip_first_screenshot=True):
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            guildcoin = OCR_SHOP_GUILD_COINS.ocr(self.device.image)
            if guildcoin > 0:
                break
        logger.attr('GuildCoin',guildcoin)
        LogRes(self.config).GuildCoin = guildcoin
        self.config.update()
    
    def get_medal(self, skip_first_screenshot=True):
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            medal = OCR_SHOP_MEDAL.ocr(self.device.image)
            if medal > 0:
                break
        logger.attr('Medal',medal)
        LogRes(self.config).Medal = medal
        self.config.update()