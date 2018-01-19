# -*- coding: utf-8 -*-
import datetime
from odoo.exceptions import ValidationError

from datetime import datetime
from odoo import models, fields, api

# 一般人基本檔 團員 會員 收費員 顧問
import logging

_logger = logging.getLogger(__name__)


class NormalP(models.Model):
    # 捐款人
    _name = 'normal.p'
    _order = 'sequence,id'

    new_coding = fields.Char(string='捐款者編號')
    old_coding = fields.Char(string='舊捐款者編號')
    special_tag = fields.Boolean(string='眷屬檔沒有的團員')
    w_id = fields.Char(string='舊團員編號')
    number = fields.Char(string='序號')
    name = fields.Char(string='姓名')
    birth = fields.Date(string='生日')
    cellphone = fields.Char(string='手機')
    con_phone = fields.Char(string='連絡電話')
    con_phone2 = fields.Char(string='連絡電話(二)')
    zip = fields.Char(string='收據郵遞區號')
    rec_addr = fields.Char(string='收據寄送地址')
    zip_code = fields.Char(string='報表郵遞區號')
    con_addr = fields.Char(string='報表寄送地址')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', ondelete='cascade')
    temp_key_in_user = fields.Char(string='輸入人員_temp')
    db_chang_date = fields.Date(string='異動日期')
    build_date = fields.Date(string='建檔日期', default=datetime.today())

    email = fields.Char(string='Email')
    type = fields.Many2many(comodel_name='people.type', string='人員種類')
    self_iden = fields.Char(string='身分證字號')

#    send_addr = fields.Char(string='寄送地址')
#    address = fields.Char(string='通訊地址')
    sex = fields.Selection(selection=[(1, '男生'), (2, '女生')], string='性別')
    come_date = fields.Date(string='到職日期')
    lev_date = fields.Date(string='離職日期')
    ps = fields.Text(string='備註')
    habbit_donate = fields.Selection(selection=[(01, '造橋'), (02, '補路'), (03, '施棺'), (04, '伙食費'), (05, '貧困扶助'),(06, '不指定'), (99, '其他工程')],
                                     string='喜好捐款')
    cashier_name = fields.Many2one(comodel_name='cashier.base', string='收費員姓名', ondelete='cascade')
    temp_cashier_name = fields.Char(string='收費員姓名_temp')
    donate_cycle = fields.Selection(selection=[('03', '季繳'), ('06', '半年繳'), ('12', '年繳')], string='捐助週期')
    rec_type = fields.Selection(selection=[(1, '正常'), (2, '年收據')], string='收據狀態')
    rec_send = fields.Boolean(string='收據寄送')

    self = fields.Char(string='自訂排序')
    report_send = fields.Boolean(string='報表寄送')
    thanks_send = fields.Boolean(string='感謝狀寄送')
    prints = fields.Boolean(string='是否列印')
    prints_id = fields.Char(string='核印批號')
    prints_date = fields.Char(string='核印日期')
    bank_id = fields.Char(string='扣款銀行代碼')
    bank = fields.Char(string='扣款銀行')
    bank_id2 = fields.Char(string='扣款分行代碼')
    bank2 = fields.Char(string='扣款分行')
    account = fields.Char(string='扣款帳號')
    bank_check = fields.Boolean(string='銀行核印')
    ps2 = fields.Text(string='備註')

    comp_id = fields.Char(string='電腦編號')
    member_list = fields.Char(string='會員名冊編號')
    year = fields.Char(string='繳費年度')
    should_pay = fields.Integer(string='應繳金額')
    cashier = fields.Many2one(comodel_name='cashier.base', string='收費員')
    temp_cashier = fields.Char(string='收費員_temp')
    pay_date = fields.Date(string='收費日期')
    booklist = fields.Boolean(string='名冊列印')
    member_type = fields.Selection(selection=[(1, '基本會員'), (2, '贊助會員')], string='會員種類')
    hire_date = fields.Date(string='雇用日期')
    merge_report = fields.Boolean(string='年收據寄送', help='將捐款者的收據整合進該住址') # help 可以在開發者模式下的欄位看到內容
    #團員檔及團員眷屬檔設定戶長之功能
    parent = fields.Many2one(comodel_name='normal.p', string='戶長', ondelete='cascade',)
    donate_family1 = fields.One2many(comodel_name='normal.p', inverse_name='parent', string='團員眷屬',readonly='True')
    # 來判斷你是不是老大
    member_data_ids = fields.Many2one(comodel_name='member.data', string='關聯的顧問會員檔')
    donate_history_ids = fields.One2many(comodel_name='donate.order', inverse_name='donate_member')
    #會員收費檔及顧問檔收費檔關聯
    member_pay_history = fields.One2many(comodel_name='associatemember.fee', inverse_name='normal_p_id')
    consultant_pay_history = fields.One2many(comodel_name='consultant.fee', inverse_name='normal_p_id')
    member_id = fields.Char(string='會員編號')
    consultant_id = fields.Char(string='顧問編號')

    sequence = fields.Integer(string='排序')
    is_donate = fields.Boolean(string='是否捐助', default=True)
    is_merge = fields.Boolean(string='是否合併收據', default=True)

    donate_family_list = fields.Char(string='眷屬列表', compute='compute_faamily_list')
    active = fields.Boolean(default=True)
    is_same_addr = fields.Boolean(string='報表地址同收據地址')
    auto_num = fields.Char('自動地區編號')

    def action_chang_donater_wizard(self):

        wizard_data = self.env['chang.donater'].create({
            'from_target': self.id
        })

        action = self.env.ref('cdg_base.chang_donater_action').read()[0]
        action['res_id'] = wizard_data.id
        return action

    def historypersonal(self):
        action = self.env.ref('cdg_base.donate_single_view_action').read()[0]
        action['context'] ={} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        action['domain'] = ['&',('donate_member', '=', self.new_coding),('state','!=',3)] # set new domain condition to search data
        return action

    def donate_batch(self,ids):
        res = []
        for line in ids:
            res.append([4, line])
        wizard_data = self.env['wizard.batch'].create({
            'donate_line': res
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.batch',
            'name': '批次捐款項目',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

    @api.depends('donate_family1.is_donate','donate_family1.is_merge')
    def compute_faamily_list(self):
        for line in self:
            sb = ''
            str = ''
            for row in line.donate_family1:
                if row.is_donate is False:
                    str += u'(X)' + row.name + ','
                elif row.is_merge is False:
                    sb += u'(★)'+ row.name + ','
                else:
                    sb += row.name + ','
            line.donate_family_list = sb+str

    def toggle_donate(self):
        self.is_donate = not self.is_donate

    def toggle_merge(self):
        self.is_merge = not self.is_merge


    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), '|', ('w_id', operator, name), '|', ('new_coding', operator, name),
                      '|', ('self_iden',operator, name), ('con_addr', operator, name)]

        banks = self.search(domain + args, limit=limit)
        return banks.name_get()

    @api.multi
    def my_self(self):
        return [('parent', '=', self.id)]


    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "{%s} %s" % (record.new_coding, record.name)
            result.append((record.id, name))
        return result

    def input_member(self):
        max_id = 753395
        member_data = self.env['member.data'].search([])
        new_id = ""
        i = 1
        type_id = 0
        for line in member_data:
            _logger.error(' %s / %s', i, len(member_data))
            if line.conn_zip_code != "":
                new_id = line.conn_zip_code[:3] + str(max_id)
            else:
                new_id = '000' + str(max_id)

            self.create({
                'new_coding': new_id,
                'name': line.name,
                'self_iden': line.user_id,
                'birth': line.birthday,
                'cellphone': line.cellphone,
                'con_phone': line.phone1,
                'con_phone2': line.phone2,
                'zip_code': line.conn_zip_code,
                'con_addr': line.conn_address,
                'member_data_ids': line.id,
                'type': self.check_type(line)
            })
            i = i + 1
            max_id = max_id + 1

    def check_type(self, line):
        if line.member_type.id > 0:
            return [(4, line.member_type.id)]
        else:
            return None

    @api.onchange('cashier_name')
    def setcashier(self):
        self.cashier = self.cashier_name.name

    @api.onchange('is_same_addr')
    def rec_addr_same_con_addr(self):
        if self.is_same_addr is True:
            if not self.zip or not self.rec_addr:
                raise ValidationError(u'收據郵遞區號或收據寄送地址不能為空白')
            else:
                self.zip_code = self.zip
                self.con_addr = self.rec_addr

    def data_input_form_DB(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 團員眷屬檔')
        i = 1
        for line in lines:
            _logger.error(' %s / %s', i, len(lines))
            self.create({
                'w_id': line[u'團員編號'],
                'number': line[u'序號'],
                'name': line[u'姓名'],
                'cellphone': line[u'手機'],
                'con_addr': line[u'通訊地址'],
                'con_phone': line[u'電話一'],
                'con_phone2': line[u'電話二'],
                'zip_code': line[u'郵遞區號'],
                'type': 1,
                'habbit_donate': self.check_habbit(line[u'捐助種類編號']),
                'rec_send': self.checkbool(line[u'收據寄送']),
                'is_donate': self.checkbool(line[u'是否捐助']),
                'self': line[u'自訂排序'],
                'key_in_user': self.check_user(line[u'輸入人員']),
                'birth': self.check_db_date(line[u'建檔日期']),
                'db_chang_date': self.check(line[u'異動日期'])
            })
            i += 1

    def check_habbit(self, habbit):
        if habbit == u'01':
            return 01
        elif habbit == u'02':
            return 02
        elif habbit == u'03':
            return 03
        elif habbit == u'04':
            return 04
        elif habbit == u'05':
            return 05
        elif habbit == u'06':
            return 06
        elif habbit == u'99':
            return 99
        else:
            return None

    # 生日裡面有亂放東西，需要驗證是否真的是YYYY-MM-DD的格式
    def check_db_date(self, date):
        if date:
            try:
                time.strptime(date, "%Y-%m-%d")
                return date
            except:
                return None
        else:
            return None

    def check_user(self, row):
        check = self.env['c.worker'].search([('w_id', '=', row)])
        if check.id > 0:
            return check.id
        else:
            return False

    def set_parent(self):
        self.search([]).remove()


    # def set_parent(self):
    #     member = self.search([('w_id', '!=', None), ('number', '=', '1')])
    #     conn = psycopg2.connect("dbname=old_cdg user=odoo password=odoo")
    #     cur = conn.cursor()
    #     i = 1
    #     for line in member:
    #         # try:
    #         sql = "UPDATE normal_p SET parent = '{}' WHERE w_id = '{}' AND number != '1'".format(str(line.id),
    #                                                                                              str(line.w_id))
    #         _logger.error('it is run to %s line', i)
    #         cur.execute(sql)
    #         # except Exception:
    #         #     _logger.error('it is run to %s line', i)
    #         #     pass
    #         i += 1
    #     conn.commit()
    #     cur.close()
    #     conn.close()

    def data_input_from_database(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 團員檔')
        i = 1
        for line in lines:
            _logger.error(' %s / %s', i, len(lines))
            exist = False
            member = self.search([('w_id', '=', line[u'團員編號']), ('number', '=', '1'), ('name', '=', line[u'姓名'])])
            if member.id > 0:
                exist = True
            if exist is False and member.special_tag is not True:
                id_create = self.create({
                    'special_tag': True,
                    'w_id': line[u'團員編號'],
                    'number': u'0',
                    'name': line[u'姓名'],
                    'birth': self.check(line[u'出生日期']),
                    'cellphone': line[u'手機'],
                    'zip_code':line[u'郵遞區號'],
                    'con_addr': line[u'通訊地址'],
                    'con_phone': line[u'電話一'],
                    'con_phone2': line[u'電話二'],
                    'donate_cycle': line[u'捐助週期'],
                    'ps2': line[u'備註'],
                    'rec_send': self.checkbool(line[u'收據寄送']),
                    'bank_id': line[u'扣款銀行代碼'],
                    'bank_id2': line[u'扣款分行代碼'],
                    'thanks_send': self.checkbool(line[u'感謝狀寄送']),
                    'report_send': self.checkbool(line[u'報表寄送']),
                    'bank_check': self.checkbool(line[u'銀行核印']),
                    'cashier': line[u'收費員編號'],
                    'build_date': self.check_db_date(line[u'建檔日期']),
                    'db_chang_date': self.check(line[u'異動日期']),
                    'key_in_user': self.check_user(line[u'輸入人員']),
                })

            i += 1

    def check(self, date_check):
        if date_check:
            return date_check
        else:
            return None

    def checkbool(self, bool):
        if bool == 'Y':
            return True
        elif bool == 'N':
            return False



    def start_member_batch(self):
        basic_setting = self.env['ir.config_parameter'].search([])
        Annual_membership_fee=0
        for line in basic_setting:
            if line.key == 'Annual_membership_fee':
                Annual_membership_fee = int(line.value)
        if len(self.year) == 4:
            self.year=str(int(self.year)-1911)

        sql = "SELECT DISTINCT on (member_id) * FROM normal_p WHERE member_id <>'' and con_addr<>'' "
        self._cr.execute(sql)
        dict = self._cr.dictfetchall()
        for i in range(len(dict)):
            self.env['associatemember.fee'].create({
                'year': self.year,
                'fee_payable': Annual_membership_fee,
                'normal_p_id': dict[i]['id']
            })
        return True

    def start_consultant_batch(self):
        basic_setting = self.env['ir.config_parameter'].search([])
        Annual_consultants_fee = 0
        for line in basic_setting:
            if line.key == 'Annual_consultants_fee':
                Annual_consultants_fee = int(line.value)
        if len(self.year) == 4:
            self.year = str(int(self.year) - 1911)

        sql = "SELECT DISTINCT on (consultant_id) * FROM normal_p WHERE consultant_id <>'' and con_addr<>'' "
        self._cr.execute(sql)
        dict = self._cr.dictfetchall()
        for i in range(len(dict)):
            self.env['consultant.fee'].create({
                'year':self.year,
                'fee_payable':Annual_consultants_fee,
                'normal_p_id': dict[i]['id']
            })
        return True

    @api.onchange('zip', 'type')
    def rec_addr_change(self):
        if self.name:
            self.old_coding = self.new_coding # 將原本的捐款者編號, 放入歷史紀錄之中

            if self.zip is False: #使用者如果沒有填收據寄送地址郵遞區號, 則編碼前3碼為 'OOO'
                compute_code = self.env['auto.donateid'].search([('zip','=','OOO')])
                self.new_coding = 'OOO' + str(compute_code.area_number + 1).zfill(5) # 取出當前 zip = 'OOO' 的累積人數+1
                compute_code.write({
                    'area_number': compute_code.area_number + 1 #  寫入 zip = 'OOO' 目前的累積人數
                })
            elif self.zip and len(self.zip) < 3: # 使用者有輸入收據寄送地址的郵遞區號但不足3碼
                raise ValidationError(u'收據寄送地址的郵遞區號填寫錯誤，請至少填3碼的郵遞區號!')
            elif self.zip and len(self.zip) >= 3: # 使用者可以填3+2郵遞區號, 但是少要填3碼的郵遞區號
                compute_code = self.env['auto.donateid'].search([('zip', '=', self.zip[0:3])]) # 搜尋計數器裡符合使用者填入郵遞區號的資料
                if compute_code.zip: # 在計數器裡有找到該郵遞區號
                    self.new_coding = self.zip[0:3] + str(compute_code.area_number + 1).zfill(5)
                    compute_code.write({
                        'area_number': compute_code.area_number + 1 #  寫入 zip 目前的累積人數
                    })
                elif compute_code.zip is False: # 在計數器裡沒有找到該郵遞區號
                    self.new_coding = self.zip[0:3] + str('1').zfill(5) # 代表此捐款者為該郵遞區號捐款的第1人
                    self.env['auto.donateid'].create({
                        'zip': self.zip[0:3], # 在計數器裡創建該郵遞區號的資料
                        'area_number': 1 # 將累積人數設定為1
                    })

            if 2 in self.type.ids:  # 判斷該筆捐款者資料是否為基本會員
                if 4 in self.type.ids:  # 判斷是否具有顧問身分
                    self.new_coding = 'AC' + self.new_coding  # 代表該捐款者是基本會員以及具有顧問身分
                else:
                    self.new_coding = 'A' + self.new_coding  # 代表該捐款者是基本會員
            elif 3 in self.type.ids:  # 判斷該筆捐款者資料是否為贊助會員
                if 4 in self.type.ids:
                    self.new_coding = 'BC' + self.new_coding  # 代表該捐款者是贊助會員以及具有顧問身分
                else:
                    self.new_coding = 'B' + self.new_coding  # 代表該捐款者是贊助會員
            elif not (2 in self.type.ids) and not (3 in self.type.ids) and 4 in self.type.ids :
                self.new_coding = 'C' + self.new_coding  # 不具有任何會員身分但具有顧問身分
            else:
                self.new_coding = self.new_coding  # 什麼都沒有的一般捐款者

    @api.model
    def create(self, vals):
        res_id = super(NormalP, self).create(vals)
        if res_id.name is False:
            raise ValidationError(u'請輸入姓名')

        if res_id.zip is False: #使用者如果沒有填收據寄送地址郵遞區號, 則編碼前3碼為 'OOO'
            compute_code = self.env['auto.donateid'].search([('zip','=','OOO')])
            res_id.new_coding = 'OOO' + str(compute_code.area_number + 1).zfill(5) # 取出當前 zip = 'OOO' 的累積人數+1
            compute_code.write({
                'area_number': compute_code.area_number + 1 #  寫入 zip = 'OOO' 目前的累積人數
            })
        elif res_id.zip and len(res_id.zip) < 3: # 使用者有輸入收據寄送地址的郵遞區號但不足3碼
            raise ValidationError(u'收據寄送地址的郵遞區號填寫錯誤，請至少填3碼的郵遞區號!')
        elif res_id.zip and len(res_id.zip) >= 3: # 使用者可以填3+2郵遞區號, 但是少要填3碼的郵遞區號
            compute_code = self.env['auto.donateid'].search([('zip', '=', res_id.zip[0:3])]) # 搜尋計數器裡符合使用者填入郵遞區號的資料
            if compute_code.zip: # 在計數器裡有找到該郵遞區號
                res_id.new_coding = res_id.zip[0:3] + str(compute_code.area_number + 1).zfill(5)
                compute_code.write({
                    'area_number': compute_code.area_number + 1 #  寫入 zip 目前的累積人數
                })
            elif compute_code.zip is False: # 在計數器裡沒有找到該郵遞區號
                res_id.new_coding = res_id.zip[0:3] + str('1').zfill(5) # 代表此捐款者為該郵遞區號捐款的第1人
                self.env['auto.donateid'].create({
                    'zip': res_id.zip[0:3], # 在計數器裡創建該郵遞區號的資料
                    'area_number': 1 # 將累積人數設定為1
                })

        if 2 in res_id.type.ids:  # 判斷該筆捐款者資料是否為基本會員
            if 4 in res_id.type.ids:  # 判斷是否具有顧問身分
                res_id.new_coding = 'AC' + res_id.new_coding  # 代表該捐款者是基本會員以及具有顧問身分
            else:
                res_id.new_coding = 'A' + res_id.new_coding  # 代表該捐款者是基本會員
        elif 3 in res_id.type.ids:  # 判斷該筆捐款者資料是否為贊助會員
            if 4 in res_id.type.ids:
                res_id.new_coding = 'BC' + res_id.new_coding  # 代表該捐款者是贊助會員以及具有顧問身分
            else:
                res_id.new_coding = 'B' + res_id.new_coding  # 代表該捐款者是贊助會員
        elif not (2 in res_id.type.ids) and not (3 in res_id.type.ids) and 4 in res_id.type.ids :
            res_id.new_coding = 'C' + res_id.new_coding  # 不具有任何會員身分但具有顧問身分
        else:
            res_id.new_coding = res_id.new_coding  # 什麼都沒有的一般捐款者

        if res_id.parent.id is False: # 如果新建的捐款者資料沒有選定戶長是誰, 那麼就由系統自動將該使用者設為戶長
            res_id.write({
                'parent': res_id.id,
                'new_coding': res_id.new_coding # 給予捐款者編號
            })
        elif res_id.parent.id: # 如果有選定戶長
            old_member_code = self.env['normal.p'].search([('id','=',res_id.parent.id)]) # 搜尋該戶長的資料
            if old_member_code.w_id: # 如果該戶長有w_id, 則將捐款者的w_id 設為與戶長相同的w_id
                res_id.write({
                    'w_id': old_member_code.w_id
                })
        return res_id

# class DonateFamily(models.Model):
#     _name = 'donate.family'
#
#     name = fields.Char(string='眷屬姓名')
#     birth = fields.Date(string='生日')
#     cellphone = fields.Char(string='手機')
#     con_phone = fields.Char(string='聯絡電話(一)')
#     con_phone2 = fields.Char(string='聯絡電話(二)')
#     rec_address = fields.Char(string='收據地址')
#     habbit_donate = fields.Selection(selection=[(1,'造橋'),(2,'補路'),(3,'施棺'),(4,'伙食費'),(5,'窮困扶助'),(6,'其他工程')],string='喜好捐款種類')
#     self = fields.Char(string='自訂排序')
#     rec_send = fields.Selection(selection=[(1,'單獨'),(2,'合併')],string='收據寄送')
#     now_donate = fields.Boolean(string='目前是否捐助' ,default= True)
