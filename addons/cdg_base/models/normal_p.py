# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import *
import logging

# 一般人基本檔 團員 會員 收費員 顧問
_logger = logging.getLogger(__name__)

class NormalP(models.Model):
    # 捐款人
    _name = 'normal.p'
    _order = 'sequence'
    _description = u'捐款者基本資料管理'

    new_coding = fields.Char(string='捐款者編號')
    # old_coding = fields.Char(string='舊捐款者編號')
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

    come_date = fields.Date(string='到職日期')
    lev_date = fields.Date(string='離職日期')
    ps = fields.Text(string='備註')
    habbit_donate = fields.Selection(selection=[(01, '造橋'), (02, '補路'), (03, '施棺'), (04, '伙食費'), (05, '貧困扶助'),(06, '一般捐款'), (99, '其他工程')],
                                     string='喜好捐款')
    cashier_name = fields.Many2one(comodel_name='cashier.base', string='收費員姓名', ondelete='cascade')
    temp_cashier_name = fields.Char(string='收費員姓名_temp')
    donate_cycle = fields.Selection(selection=[('03', '季繳'), ('06', '半年繳'), ('12', '年繳')], string='捐助週期')
    rec_type = fields.Selection(selection=[(1, '正常'), (2, '年收據')], string='收據狀態')
    rec_send = fields.Boolean(string='收據寄送', default=True)

    self = fields.Char(string='自訂排序')
    report_send = fields.Boolean(string='報表寄送', default=True)
    thanks_send = fields.Boolean(string='感謝狀寄送')
    prints = fields.Boolean(string='是否列印')
    prints_id = fields.Char(string='核印批號')
    prints_date = fields.Char(string='核印日期')
    bank_id = fields.Char(string='扣款銀行代碼')
    bank = fields.Char(string='扣款銀行')
    bank_id2 = fields.Char(string='扣款分行代碼')
    bank2 = fields.Char(string='扣款分行')
    account = fields.Char(string='銀行帳號')
    bank_check = fields.Boolean(string='銀行核印')
    ps2 = fields.Text(string='備註')

    comp_id = fields.Char(string='電腦編號')
    member_list = fields.Char(string='會員名冊編號')
    year = fields.Char(string='繳費年度')
    should_pay = fields.Integer(string='應繳金額')
    cashier = fields.Many2one(comodel_name='cashier.base', string='收費員')
    temp_cashier = fields.Char(string='收費員_temp')
    pay_date = fields.Date(string='收費日期')
    booklist = fields.Boolean(string='名冊列印', default=True)
    member_type = fields.Selection(selection=[(1, '基本會員'), (2, '贊助會員')], string='會員種類')
    hire_date = fields.Date(string='雇用日期')
    merge_report = fields.Boolean(string='年收據寄送', help='將捐款者的收據整合進該住址') # help 可以在開發者模式下的欄位看到內容
    #團員檔及團員眷屬檔設定戶長之功能
    parent = fields.Many2one(comodel_name='normal.p', string='戶長', ondelete='cascade')
    donate_family1 = fields.One2many(comodel_name='normal.p', inverse_name='parent', string='團員眷屬')
    # 來判斷你是不是老大
    member_data_ids = fields.Many2one(comodel_name='member.data', string='關聯的顧問會員檔')
    donate_history_ids = fields.One2many(comodel_name='donate.order', inverse_name='donate_member')
    donate_single_history_ids = fields.One2many(comodel_name='donate.single', inverse_name='donate_member')
    #會員收費檔及顧問檔收費檔關聯
    member_pay_history = fields.One2many(comodel_name='associatemember.fee', inverse_name='normal_p_id')
    consultant_pay_history = fields.One2many(comodel_name='consultant.fee', inverse_name='normal_p_id')
    member_id = fields.Char(string='會員編號')
    consultant_id = fields.Char(string='顧問編號')

    sequence = fields.Integer(string='排序',default=1)

    is_donate = fields.Boolean(string='是否捐助', default=True)
    is_merge = fields.Boolean(string='是否合併收據', default=True)

    donate_family_list = fields.Char(string='眷屬列表', compute='compute_faamily_list' )
    active = fields.Boolean(default=True)
    is_same_addr = fields.Boolean(string='報表地址同收據地址')
    auto_num = fields.Char('自動地區編號')
    check_donate_order = fields.Boolean(string='捐款紀錄查詢', default = False)
    is_delete = fields.Boolean(string='未有捐款紀錄', default = False)

    last_donate_date = fields.Date('上次捐款日期')
    last_donate_type = fields.Selection(selection=[(01, '造橋'), (02, '補路'), (03, '施棺'), (05, '貧困扶助'),(06, '一般捐款')],string='捐款種類')
    last_donate_money = fields.Integer('上次捐款金額')
    donate_batch_setting = fields.Boolean(string='確認捐款', default = False)
    postal_code_id = fields.Many2one(comodel_name='postal.code', string='郵遞區號關聯')
    print_all_donor_list = fields.Boolean(string='列印願意捐助的眷屬')
    head_of_household = fields.Integer('我是戶長')

    # 設定上一筆捐款 如果捐款種類有選擇 金額帶入100
    @api.onchange('last_donate_type')
    def set_default_last_donate_money(self):
        if self.last_donate_type != False and self.last_donate_money == 0:
            self.last_donate_money = 100


    @api.onchange('check_donate_order')
    def check_unlink(self):
        if self.check_donate_order:
            for line in self.donate_family1:
                if (len(line.donate_history_ids) != 0 or len(line.donate_single_history_ids) != 0 ) is True:
                    line.is_delete = False
                elif (len(line.donate_history_ids) == 0 and len(line.donate_single_history_ids) == 0) is True:
                    line.is_delete = True

    # 合併捐款者功能
    def action_chang_donater_wizard(self):
        wizard_data = self.env['chang.donater'].create({
            'from_target': self.id
        })
        action = self.env.ref('cdg_base.chang_donater_action').read()[0]
        action['res_id'] = wizard_data.id
        return action


    def start_donate(self):
        action = self.env.ref('cdg_base.start_donate_action').read()[0]
        user = self.env['res.users'].search([('login', '=', self.env.user.login)])
        action['context'] = {'default_donate_member':self.id, 'default_payment_method':user.payment_method}
        return action


    def historypersonal(self):
        action = self.env.ref('cdg_base.donate_single_view_action').read()[0]
        action['context'] ={} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        action['domain'] = ['&',('donate_member.new_coding', '=', self.new_coding),('state','!=',3)]  # set new domain condition to search data
        return action

    def cashier_block(self, ids):
        res = []
        for line in ids:
            res.append([4,line])
            wizard_data = self.env['cashier.block'].create({'from_target': res})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cashier.block',
            'name': '收費員捐款者名冊-新',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

    def cashier_member(self, ids):
        res = []
        for line in ids:
            res.append([4,line])
            wizard_data = self.env['cashier.member'].create({'from_target': res})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cashier.member',
            'name': '收費員會員名冊-新',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

    def cashier_consultant(self, ids):
        res = []
        for line in ids:
            res.append([4,line])
            wizard_data = self.env['cashier.consultant'].create({'from_target': res})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cashier.consultant',
            'name': '收費員顧問名冊-新',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

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



    def check_batch_donate(self):
        if self.donate_batch_setting == True:
            self.donate_batch_setting = False
        elif self.donate_batch_setting == False:
            self.donate_batch_setting = True
        return True


    @api.depends('donate_family1.is_donate','donate_family1.is_merge')
    def compute_faamily_list(self):
        for line in self:
            sb = ''
            str = ''
            donate_type = ''
            for row in line.donate_family1:
                if row.last_donate_type == 1:
                    donate_type =  u'造橋'
                if row.last_donate_type == 2:
                    donate_type = u'補路'
                if row.last_donate_type == 3:
                    donate_type = u'施棺'
                if row.last_donate_type == 4:
                    donate_type = u'伙食費'
                if row.last_donate_type == 5:
                    donate_type = u'貧困扶助'
                if row.last_donate_type == 6:
                    donate_type = u'一般捐款'
                if row.last_donate_type == 99:
                    donate_type = u'其他工程'
                if row.last_donate_type == False:
                    donate_type = ''

                if row.is_donate is False:
                    str += u'(X %s %s %s),' % (row.name , donate_type , row.last_donate_money )
                elif row.is_merge is False:
                    sb += u'(★ %s %s %s),' % (row.name , donate_type , row.last_donate_money )
                else:
                    sb += u'(%s %s %s),' % (row.name , donate_type , row.last_donate_money )
            line.donate_family_list = sb+str

    def toggle_donate(self):
        self.is_donate = not self.is_donate

    def toggle_merge(self):
        self.is_merge = not self.is_merge

    def all_addr_chnage(self):
        for line in self.donate_family1:
            if line:
                line.rec_addr  =  self.rec_addr
            else:
                break

    def combine_addr(self):
        for line in self.donate_family1:
            if line:
                if line.is_merge is True:
                  line.rec_addr =  self.rec_addr
            else:
                break

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if u'\u4e00' <= name <=u'\u9fff':
            domain = [('name', operator, name)]
        else:
            domain = ['|', ('w_id', operator, name), ('new_coding', operator, name)]

        banks = self.search(domain + args, limit=limit)
        return banks.name_get()

    @api.multi
    def my_self(self):
        return [('parent', '=', self.id)]


    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "{%s} %s {%s}" % (record.new_coding, record.name,record.w_id)
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

    @api.onchange('parent')
    def set_rec_zip(self):
        if self.parent:
            self.zip = self.parent.zip
            self.rec_addr = self.parent.rec_addr
            self.cashier_name = self.parent.cashier_name

    @api.onchange('zip','zip_code')
    def set_postal_code_id(self):
        flag = True
        if self.zip:
            for ch in self.zip:
                if not u'\u0030' <= ch <=u'\u0039':
                    raise ValidationError(u'收據郵遞區號輸入格式錯誤，請重新輸入')
                if int(self.zip[0]) == 0:
                    raise ValidationError(u'收據郵遞區號輸入格式錯誤，請重新輸入')

            if len(self.zip) < 3:
                raise ValidationError(u'收據郵遞區號為三碼，請重新輸入')
            else:
                for line in self.postal_code_id:
                    if self.zip == line.zip:
                        self.postal_code_id = line.id

        if self.zip_code:
            for ch in self.zip_code:
                if not u'\u0030' <= ch <= u'\u0039':
                    raise ValidationError(u'收據郵遞區號輸入格式錯誤，請重新輸入')
                if int(self.zip_code[0]) == 0:
                    raise ValidationError(u'收據郵遞區號輸入格式錯誤，請重新輸入')

            if len(self.zip_code) < 3:
                raise ValidationError(u'報表郵遞區號為三碼，請重新輸入')
            else:
                for line in self.postal_code_id:
                    if self.zip_code == line.zip:
                        self.postal_code_id = line.id




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

    # @api.onchange('zip', 'type')
    # def rec_addr_change(self):
    #     if self.name:
    #         self.old_coding = self.new_coding # 將原本的捐款者編號, 放入歷史紀錄之中
    #
    #         if self.zip is False: #使用者如果沒有填收據寄送地址郵遞區號, 則編碼前3碼為 '999'
    #             compute_code = self.env['auto.donateid'].search([('zip','=','999')])
    #             self.new_coding = '999' + str(compute_code.area_number + 1).zfill(5) # 取出當前 zip = '999' 的累積人數+1
    #             compute_code.write({
    #                 'area_number': compute_code.area_number + 1 #  寫入 zip = 'OOO' 目前的累積人數
    #             })
    #         elif self.zip and len(self.zip) < 3: # 使用者有輸入收據寄送地址的郵遞區號但不足3碼
    #             raise ValidationError(u'收據寄送地址的郵遞區號填寫錯誤，請至少填3碼的郵遞區號!')
    #         elif self.zip and len(self.zip) >= 3: # 使用者可以填3+2郵遞區號, 但是少要填3碼的郵遞區號
    #             compute_code = self.env['auto.donateid'].search([('zip', '=', self.zip[0:3])]) # 搜尋計數器裡符合使用者填入郵遞區號的資料
    #             if compute_code.zip: # 在計數器裡有找到該郵遞區號
    #                 self.new_coding = self.zip[0:3] + str(compute_code.area_number + 1).zfill(5)
    #                 compute_code.write({
    #                     'area_number': compute_code.area_number + 1 #  寫入 zip 目前的累積人數
    #                 })
    #             elif compute_code.zip is False: # 在計數器裡沒有找到該郵遞區號
    #                 self.new_coding = self.zip[0:3] + str('1').zfill(5) # 代表此捐款者為該郵遞區號捐款的第1人
    #                 self.env['auto.donateid'].create({
    #                     'zip': self.zip[0:3], # 在計數器裡創建該郵遞區號的資料
    #                     'area_number': 1 # 將累積人數設定為1
    #                 })

    @api.model
    def create(self, vals):
        res_id = super(NormalP, self).create(vals)
        if res_id.name is False:
            raise ValidationError(u'請輸入姓名')

        if res_id.zip is False: #使用者如果沒有填收據寄送地址郵遞區號, 則編碼前3碼為 '999'
            raise ValidationError(u'收據郵遞區號不能為空白')
        elif res_id.zip == True or res_id.zip_code == True:

            for ch in res_id.zip:
                if not u'\u0030' <= ch <= u'\u0039':
                    raise ValidationError(u'收據郵遞區號輸入格式錯誤，請重新輸入')
                if int(res_id.zip[0]) == 0:
                    raise ValidationError(u'收據郵遞區號輸入格式錯誤，請重新輸入')

            for ch in res_id.zip_code:
                if not u'\u0030' <= ch <= u'\u0039':
                    raise ValidationError(u'報表郵遞區號輸入格式錯誤，請重新輸入')
                if int(res_id.zip_code[0]) == 0:
                    raise ValidationError(u'報表郵遞區號輸入格式錯誤，請重新輸入')

        elif (res_id.zip and len(res_id.zip) < 3) or (res_id.zip_code and len(res_id.zip_code) < 3): # 使用者有輸入收據寄送地址的郵遞區號但不足3碼
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
