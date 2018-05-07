# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging
import math

# 一般人基本檔 團員 會員 收費員 顧問
_logger = logging.getLogger(__name__)

# 存储1901-2099年每年每月的天数，第1位到第13位存储每月（包括闰月共13月）的天数，为1表示该月为30天，
# 为0表示该月为29天。第12－15位表示该年闰月的月份，如果为0x0F表示该年没有闰月。
g_lunar_month_days = [
    0xF0EA4, 0xF1D4A, 0x52C94, 0xF0C96, 0xF1536, 0x42AAC, 0xF0AD4, 0xF16B2, 0x22EA4, 0xF0EA4,  # 1901-1910
    0x6364A, 0xF164A, 0xF1496, 0x52956, 0xF055A, 0xF0AD6, 0x216D2, 0xF1B52, 0x73B24, 0xF1D24,  # 1911-1920
    0xF1A4A, 0x5349A, 0xF14AC, 0xF056C, 0x42B6A, 0xF0DA8, 0xF1D52, 0x23D24, 0xF1D24, 0x61A4C,  # 1921-1930
    0xF0A56, 0xF14AE, 0x5256C, 0xF16B4, 0xF0DA8, 0x31D92, 0xF0E92, 0x72D26, 0xF1526, 0xF0A56,  # 1931-1940
    0x614B6, 0xF155A, 0xF0AD4, 0x436AA, 0xF1748, 0xF1692, 0x23526, 0xF152A, 0x72A5A, 0xF0A6C,  # 1941-1950
    0xF155A, 0x52B54, 0xF0B64, 0xF1B4A, 0x33A94, 0xF1A94, 0x8152A, 0xF152E, 0xF0AAC, 0x6156A,  # 1951-1960
    0xF15AA, 0xF0DA4, 0x41D4A, 0xF1D4A, 0xF0C94, 0x3192E, 0xF1536, 0x72AB4, 0xF0AD4, 0xF16D2,  # 1961-1970
    0x52EA4, 0xF16A4, 0xF164A, 0x42C96, 0xF1496, 0x82956, 0xF055A, 0xF0ADA, 0x616D2, 0xF1B52,  # 1971-1980
    0xF1B24, 0x43A4A, 0xF1A4A, 0xA349A, 0xF14AC, 0xF056C, 0x60B6A, 0xF0DAA, 0xF1D92, 0x53D24,  # 1981-1990
    0xF1D24, 0xF1A4C, 0x314AC, 0xF14AE, 0x829AC, 0xF06B4, 0xF0DAA, 0x52D92, 0xF0E92, 0xF0D26,  # 1991-2000
    0x42A56, 0xF0A56, 0xF14B6, 0x22AB4, 0xF0AD4, 0x736AA, 0xF1748, 0xF1692, 0x53526, 0xF152A,  # 2001-2010
    0xF0A5A, 0x4155A, 0xF156A, 0x92B54, 0xF0BA4, 0xF1B4A, 0x63A94, 0xF1A94, 0xF192A, 0x42A5C,  # 2011-2020
    0xF0AAC, 0xF156A, 0x22B64, 0xF0DA4, 0x61D52, 0xF0E4A, 0xF0C96, 0x5192E, 0xF1956, 0xF0AB4,  # 2021-2030
    0x315AC, 0xF16D2, 0xB2EA4, 0xF16A4, 0xF164A, 0x63496, 0xF1496, 0xF0956, 0x50AB6, 0xF0B5A,  # 2031-2040
    0xF16D4, 0x236A4, 0xF1B24, 0x73A4A, 0xF1A4A, 0xF14AA, 0x5295A, 0xF096C, 0xF0B6A, 0x31B54,  # 2041-2050
    0xF1D92, 0x83D24, 0xF1D24, 0xF1A4C, 0x614AC, 0xF14AE, 0xF09AC, 0x40DAA, 0xF0EAA, 0xF0E92,  # 2051-2060
    0x31D26, 0xF0D26, 0x72A56, 0xF0A56, 0xF14B6, 0x52AB4, 0xF0AD4, 0xF16CA, 0x42E94, 0xF1694,  # 2061-2070
    0x8352A, 0xF152A, 0xF0A5A, 0x6155A, 0xF156A, 0xF0B54, 0x4174A, 0xF1B4A, 0xF1A94, 0x3392A,  # 2071-2080
    0xF192C, 0x7329C, 0xF0AAC, 0xF156A, 0x52B64, 0xF0DA4, 0xF1D4A, 0x41C94, 0xF0C96, 0x8192E,  # 2081-2090
    0xF0956, 0xF0AB6, 0x615AC, 0xF16D4, 0xF0EA4, 0x42E4A, 0xF164A, 0xF1516, 0x22936,           # 2090-2099
]
#-天干名称
cTianGan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
#-地支名称
cDiZhi = ["子","丑","寅","卯","辰","巳","午", "未","申","酉","戌","亥"]

wNongliData = [2635,333387,1701,1748,267701,694,2391,133423,1175,396438
    ,3402,3749,331177,1453,694,201326,2350,465197,3221,3402
    ,400202,2901,1386,267611,605,2349,137515,2709,464533,1738
    ,2901,330421,1242,2651,199255,1323,529706,3733,1706,398762
    ,2741,1206,267438,2647,1318,204070,3477,461653,1386,2413
    ,330077,1197,2637,268877,3365,531109,2900,2922,398042,2395
    ,1179,267415,2635,661067,1701,1748,398772,2742,2391,330031
    ,1175,1611,200010,3749,527717,1452,2742,332397,2350,3222
    ,268949,3402,3493,133973,1386,464219,605,2349,334123,2709
    ,2890,267946,2773,592565,1210,2651,395863,1323,2707,265877]

wMonthAdd = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
# - 农历数据

START_YEAR, END_YEAR = 1901, 1900 + len(g_lunar_month_days)
LUNAR_START_DATE, SOLAR_START_DATE = (1901, 1, 1), datetime(1901, 2, 19)  # 1901年正月初一的公历日期为1901/2/19
LUNAR_END_DATE, SOLAR_END_DATE = (2099, 12, 30), datetime(2100, 2, 18)  # 2099年12月30的公历日期是2100/2/8


class BridgeData(models.Model):
    _name = 'bridge.data'
    _order = 'bridge_code desc'

    bridge_code = fields.Char('橋樑編號')
    name = fields.Char('橋樑名稱')
    length = fields.Float('長度')
    width = fields.Float('寬度')
    height = fields.Float('高度')
    bridge_addr = fields.Char('橋樑地址')
    donate_date_start = fields.Date('募捐起日')
    donate_date_end = fields.Date('募捐迄日')
    build_date = fields.Date('國曆動土日期')
    completed_date = fields.Date('國曆謝土日期')
    china_build_date = fields.Char('農曆動土日期')
    china_completed_date = fields.Char('農曆謝土日期')
    db_change_date = fields.Date('異動日期')

    numbers = fields.Integer('數字')
    position_x = fields.Float('座標X', digits=(2,6))
    position_y = fields.Float('座標Y', digits=(2,6))

    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', ondelete='cascade')
    temp_key_in_user = fields.Char('輸入人員')

    def GetDayOf(self,st):
        wCurYear = st["year"]
        wCurMonth = st["mon"]
        wCurDay = st["day"]
        nTheDate = (wCurYear - 1921) * 365 + (wCurYear - 1921) / 4 + wCurDay + wMonthAdd[wCurMonth - 1] - 38
        if (((wCurYear % 4) == 0) and (wCurMonth > 2)):
            nTheDate = nTheDate + 1
        nIsEnd = 0
        m = 0
        while nIsEnd != 1:
            # if wNongliData[m+1] < 4095:
            if wNongliData[m] < 4095:
                k = 11
            else:
                k = 12
            n = k
            while n >= 0:
                nBit = wNongliData[m]
                for i in range(n):
                    nBit = math.floor(nBit / 2);
                nBit = nBit % 2
                if nTheDate <= (29 + nBit):
                    nIsEnd = 1
                    break
                nTheDate = nTheDate - 29 - nBit
                n = n - 1
            if nIsEnd != 0:
                break
            m = m + 1
        wCurYear = 1921 + m
        wCurMonth = k - n + 1
        wCurDay = int(math.floor(nTheDate))
        if k == 12:
            if wCurMonth == wNongliData[m] / 65536 + 1:
                wCurMonth = 1 - wCurMonth
            elif wCurMonth > wNongliData[m] / 65536 + 1:
                wCurMonth = wCurMonth - 1

        return cTianGan[(((wCurYear - 4) % 60) % 10)] + cDiZhi[(((wCurYear - 4) % 60) % 12)]

    @api.onchange('build_date')
    def build_date_change(self):
        if self.build_date:
            year = int(datetime.strptime(self.build_date, '%Y-%m-%d').year)
            month = int(datetime.strptime(self.build_date, '%Y-%m-%d').month)
            day = int(datetime.strptime(self.build_date, '%Y-%m-%d').day)
            self.china_build_date = self.get_lunar_date(datetime(year, month, day))

    @api.onchange('completed_date')
    def completed_date_change(self):
        if self.completed_date:
            year = int(datetime.strptime(self.completed_date, '%Y-%m-%d').year)
            month = int(datetime.strptime(self.completed_date, '%Y-%m-%d').month)
            day = int(datetime.strptime(self.completed_date, '%Y-%m-%d').day)
            self.china_completed_date = self.get_lunar_date(datetime(year, month, day))

    def date_diff(self,tm):
        return (tm - SOLAR_START_DATE).days

    def get_leap_month(self,lunar_year):
        return (g_lunar_month_days[lunar_year - START_YEAR] >> 16) & 0x0F

    def lunar_month_days(self,lunar_year, lunar_month):
        return 29 + ((g_lunar_month_days[lunar_year - START_YEAR] >> lunar_month) & 0x01)

    def lunar_year_days(self,year):
        days = 0
        months_day = g_lunar_month_days[year - START_YEAR]
        for i in range(1, 13 if self.get_leap_month(year) == 0x0F else 14):
            day = 29 + ((months_day >> i) & 0x01)
            days += day
        return days

    # 根据公历计算农历日期，返回(year,month,day,isLeap)
    def get_lunar_date(self,tm):
        if (tm < SOLAR_START_DATE or tm > SOLAR_END_DATE):
            raise Exception('out of range')

        span_days = self.date_diff(tm)

        year, month, day = START_YEAR, 1, 1
        tmp = self.lunar_year_days(year)
        while span_days >= tmp:
            span_days -= tmp
            year += 1
            tmp = self.lunar_year_days(year)

        leap = False
        tmp = self.lunar_month_days(year, month)
        while span_days >= tmp:
            span_days -= tmp
            month += 1
            tmp = self.lunar_month_days(year, month)
        leap_month = self.get_leap_month(year)
        if month > leap_month:
            month -= 1
            if month == leap_month:
                leap = True

        day += span_days
        st = {"year": year, "mon": month, "day": day}
        self.GetDayOf(st)
        return "民國%s年%s月%s日 (農曆 %s年%s月%s日)" % (year-1911, month, day,self.GetDayOf(st), month, day)

    # 根据农历计算公历日期，返回一个数组[datetime1, datetime2]，如果为闰月，则可能包含两个日期，否则只有一个
    def get_solar_date(self,year, month, day):
        if not (START_YEAR <= year <= END_YEAR and 1 <= month <= 12 and 1 <= day <= 30):
            raise Exception('out of range')
        span_days = 0;
        for y in range(START_YEAR, year):
            span_days += self.lunar_year_days(y)
        leap_month = self.get_leap_month(year)
        for m in range(1, month + (month > leap_month)):
            span_days += self.lunar_month_days(year, m)
        span_days += day - 1

        if leap_month == month:
            return [SOLAR_START_DATE + timedelta(span_days),
                    SOLAR_START_DATE + timedelta(span_days + self.lunar_month_days(year, leap_month))]
        else:
            return [SOLAR_START_DATE + timedelta(span_days)]

    @api.model
    def create(self, vals):
        res_id = super(BridgeData, self).create(vals)

        if res_id.name is False:
            raise ValidationError(u'橋樑名稱不得為空')

        # res_id.bridge_code = self.env['ir.sequence'].next_by_code('bridge.data')
        res_id.key_in_user = self.env.uid
        return res_id

    @api.onchange('bridge_code')
    def bridge_code_is_repeart(self):
        data = self.env['bridge.data'].search([('bridge_code','=',self.bridge_code)])

        for line in data:
            if line.bridge_code == self.bridge_code:
                raise ValidationError(u'橋樑編號不得重複')

