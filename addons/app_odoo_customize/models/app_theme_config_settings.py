# -*- coding: utf-8 -*-

import logging, datetime
import math
# import zipcodetw
# import collections

from openerp import api, fields, models, _

_logger = logging.getLogger(__name__)


class AppThemeConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'app.theme.config.settings'

    _description = u"App Odoo Customize settings"
    app_system_name = fields.Char('System Name', help=u"Setup System Name,which replace Odoo")
    app_show_lang = fields.Boolean('Show Quick Language Switcher',
                                   help=u"When enable,User can quick switch language in user menu")
    app_show_debug = fields.Boolean('Show Quick Debug', help=u"When enable,everyone login can see the debug menu")
    app_show_documentation = fields.Boolean('Show Documentation', help=u"When enable,User can visit user manual")
    app_show_documentation_dev = fields.Boolean('Show Developer Documentation',
                                                help=u"When enable,User can visit development documentation")
    app_show_support = fields.Boolean('Show Support', help=u"When enable,User can vist your support site")
    app_show_account = fields.Boolean('Show My Account', help=u"When enable,User can login to your website")
    app_show_enterprise = fields.Boolean('Show Enterprise Tag', help=u"Uncheck to hide the Enterprise tag")
    app_show_share = fields.Boolean('Show Share Dashboard', help=u"Uncheck to hide the Odoo Share Dashboard")
    app_show_poweredby = fields.Boolean('Show Powered by Odoo', help=u"Uncheck to hide the Powered by text")

    app_documentation_url = fields.Char('Documentation Url')
    app_documentation_dev_url = fields.Char('Developer Documentation Url')
    app_support_url = fields.Char('Support Url')
    app_account_title = fields.Char('My Odoo.com Account Title')
    app_account_url = fields.Char('My Odoo.com Account Url')

    Basic_donations = fields.Char(string="基本捐助款")
    First_Annual_membership_fee = fields.Char(string="首年會員年費")
    Annual_membership_fee = fields.Char(string="會員年費")
    Annual_consultants_fee = fields.Char(string="顧問年費")
    coffin_amount = fields.Char(string="施棺滿足額")
    exception_coffin_amount = fields.Char(string="特案施棺滿足額")
    move_data_year = fields.Char(string="轉移資料年份")

    def save_setting(self):
        basic_setting = self.env['ir.config_parameter'].search([])
        for line in basic_setting:
            if line.key == 'coffin_amount':
                line.value = self.coffin_amount
            if line.key == 'Basic_donations':
                line.value = self.Basic_donations
            if line.key == 'Annual_membership_fee':
                line.value = self.Annual_membership_fee
            if line.key == 'Annual_consultants_fee':
                line.value = self.Annual_consultants_fee
            if line.key == 'exception_coffin_amount':
                line.value = self.exception_coffin_amount
            if line.key == 'First_Annual_membership_fee':
                line.value = self.First_Annual_membership_fee
        return True

    @api.model
    def get_default_all(self, fields):
        ir_config = self.env['ir.config_parameter']
        app_system_name = ir_config.get_param('app.window_title', default='odooApp')

        app_show_lang = True if ir_config.get_param('app_show_lang') == "True" else False
        app_show_debug = True if ir_config.get_param('app_show_debug') == "True" else False
        app_show_documentation = True if ir_config.get_param('app_show_documentation') == "True" else False
        app_show_documentation_dev = True if ir_config.get_param('app_show_documentation_dev') == "True" else False
        app_show_support = True if ir_config.get_param('app_show_support') == "True" else False
        app_show_account = True if ir_config.get_param('app_show_account') == "True" else False
        app_show_enterprise = True if ir_config.get_param('app_show_enterprise') == "True" else False
        app_show_share = True if ir_config.get_param('app_show_share') == "True" else False
        app_show_poweredby = True if ir_config.get_param('app_show_poweredby') == "True" else False

        app_documentation_url = ir_config.get_param('app_documentation_url',
                                                    default='http://www.sunpop.cn/documentation/user/10.0/en/index.html')
        app_documentation_dev_url = ir_config.get_param('app_documentation_dev_url',
                                                        default='http://www.sunpop.cn/documentation/10.0/index.html')
        app_support_url = ir_config.get_param('app_support_url', default='http://www.sunpop.cn/trial/')
        app_account_title = ir_config.get_param('app_account_title', default='My Online Account')
        app_account_url = ir_config.get_param('app_account_url', default='http://www.sunpop.cn/my-account/')

        Basic_donations = ir_config.get_param('Basic_donations', default='100')
        First_Annual_membership_fee = ir_config.get_param('First_Annual_membership_fee', default='1700')
        Annual_membership_fee = ir_config.get_param('Annual_membership_fee', default='1200')
        Annual_consultants_fee = ir_config.get_param('Annual_consultants_fee', default='10000')
        coffin_amount = ir_config.get_param('coffin_amount', default='30000')
        exception_coffin_amount = ir_config.get_param('exception_coffin_amount', default='60000')
        move_data_year = ir_config.get_param('move_data_year')

        return dict(
            app_system_name=app_system_name,
            app_show_lang=app_show_lang,
            app_show_debug=app_show_debug,
            app_show_documentation=app_show_documentation,
            app_show_documentation_dev=app_show_documentation_dev,
            app_show_support=app_show_support,
            app_show_account=app_show_account,
            app_show_enterprise=app_show_enterprise,
            app_show_share=app_show_share,
            app_show_poweredby=app_show_poweredby,
            app_documentation_url=app_documentation_url,
            app_documentation_dev_url=app_documentation_dev_url,
            app_support_url=app_support_url,
            app_account_title=app_account_title,
            app_account_url=app_account_url,
            Basic_donations=Basic_donations,
            First_Annual_membership_fee = First_Annual_membership_fee,
            Annual_membership_fee = Annual_membership_fee,
            Annual_consultants_fee= Annual_consultants_fee,
            coffin_amount = coffin_amount,
            exception_coffin_amount = exception_coffin_amount,
            move_data_year = move_data_year,
        )

    @api.multi
    def set_default_all(self):
        self.ensure_one()
        ir_config = self.env['ir.config_parameter']
        ir_config.set_param("app_system_name", self.app_system_name or "")
        ir_config.set_param("app_show_lang", self.app_show_lang or "False")
        ir_config.set_param("app_show_debug", self.app_show_debug or "False")
        ir_config.set_param("app_show_documentation", self.app_show_documentation or "False")
        ir_config.set_param("app_show_documentation_dev", self.app_show_documentation_dev or "False")
        ir_config.set_param("app_show_support", self.app_show_support or "False")
        ir_config.set_param("app_show_account", self.app_show_account or "False")
        ir_config.set_param("app_show_enterprise", self.app_show_enterprise or "False")
        ir_config.set_param("app_show_share", self.app_show_share or "False")
        ir_config.set_param("app_show_poweredby", self.app_show_poweredby or "False")

        ir_config.set_param("app_documentation_url",
                            self.app_documentation_url or "http://www.sunpop.cn/documentation/user/10.0/en/index.html")
        ir_config.set_param("app_documentation_dev_url",
                            self.app_documentation_dev_url or "http://www.sunpop.cn/documentation/10.0/index.html")
        ir_config.set_param("app_support_url", self.app_support_url or "http://www.sunpop.cn/trial/")
        ir_config.set_param("app_account_title", self.app_account_title or "My Online Account")
        ir_config.set_param("app_account_url", self.app_account_url or "http://www.sunpop.cn/my-account/")

        ir_config.set_param("Basic_donations",self.Basic_donations or '100')
        ir_config.set_param("First_Annual_membership_fee", self.First_Annual_membership_fee or '1700')
        ir_config.set_param("Annual_membership_fee",self.Annual_membership_fee or '1200')
        ir_config.set_param("Annual_consultants_fee",self.Annual_consultants_fee or '10000')
        ir_config.set_param("coffin_amount",self.coffin_amount or '30000')
        ir_config.set_param("exception_coffin_amount", self.exception_coffin_amount or '60000')
        ir_config.set_param("move_data_year", self.move_data_year)
        return True

    @api.multi
    def remove_sales(self):
        to_removes = [
            # 清除销售单据
            ['sale.order.line', ],
            ['sale.order', ],
        ]
        try:
            for line in to_removes :
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table_exist:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号
            seqs = self.env['ir.sequence'].search([('code', '=', 'sale.order')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where code ='sale.order';"
            self._cr.execute(sql)
        except Exception, e:
            raise Warning(e)
        return True

    def remove_product(self):
        to_removes = [
            # 清除产品数据
            ['product.product', ],
            ['product.template', ],
        ]
        try:
            for line in to_removes :
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table_exist:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号,针对自动产品编号
            seqs = self.env['ir.sequence'].search([('code', '=', 'product.product')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where code ='product.product';"
            self._cr.execute(sql)
        except Exception, e:
            raise Warning(e)
        return True

    def remove_product_attribute(self):
        to_removes = [
            # 清除产品属性
            ['product.attribute.value', ],
            ['product.attribute', ],
        ]
        try:
            for line in to_removes :
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table_exist:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception, e:
            raise Warning(e)
        return True

    @api.multi
    def remove_pos(self):
        to_removes = [
            # 清除POS单据
            ['pos.order.line', ],
            ['pos.order', ],
        ]
        try:
            for line in to_removes :
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table_exist:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号
            seqs = self.env['ir.sequence'].search([('code', '=', 'pos.order')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where code ='pos.order';"
            self._cr.execute(sql)
        except Exception, e:
            raise Warning(e)
        return True

    @api.multi
    def remove_purchase(self):
        to_removes = [
            # 清除采购单据
            ['purchase.order.line', ],
            ['purchase.order', ],
        ]
        try:
            for line in to_removes :
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table_exist:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号
            seqs = self.env['ir.sequence'].search([('code', '=', 'purchase.order')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where code ='purchase.order';"
            self._cr.execute(sql)
        except Exception, e:
            raise Warning(e)
        return True

    @api.multi
    def remove_mrp(self):
        to_removes = [
            # 清除生产单据
            ['mrp.workcenter.productivity', ],
            ['mrp.workorder', ],
            ['mrp.production.workcenter.line', ],
            ['mrp.production', ],
            ['mrp.production.product.line', ],
            ['mrp.unbuild', ],
        ]
        try:
            for line in to_removes :
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table_exist:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号
            seqs = self.env['ir.sequence'].search(['|', ('code', '=', 'mrp.production'), ('code', '=', 'mrp.unbuild')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where (code ='mrp.production' or code ='mrp.unbuild');"
            self._cr.execute(sql)
        except Exception, e:
            raise Warning(e)
        return True

    @api.multi
    def remove_mrp_bom(self):
        to_removes = [
            # 清除生产BOM
            ['mrp.bom.line', ],
            ['mrp.bom', ],
        ]
        try:
            for line in to_removes :
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table_exist:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception, e:
            raise Warning(e)
        return True

    @api.multi
    def remove_inventory(self):
        to_removes = [
            # 清除库存单据
            ['procurement.order', ],
            ['stock.quant', ],
            ['stock.quant.package', ],
            ['stock.quant.move.rel', ],
            ['stock.move', ],
            ['stock.pack.operation', ],
            ['stock.picking', ],
            ['stock.scrap', ],
            ['stock.inventory.line', ],
            ['stock.inventory', ],
            ['stock.production.lot', ],
            ['stock.fixed.putaway.strat', ],
        ]
        try:
            for line in to_removes :
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table_exist:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # 更新序号
            seqs = self.env['ir.sequence'].search([
                '|', ('code', '=', 'stock.lot.serial'),
                '|', ('code', '=', 'stock.lot.tracking'),
                '|', ('code', '=', 'stock.orderpoint'),
                '|', ('code', '=', 'stock.picking'),
                '|', ('code', '=', 'stock.quant.package'),
                '|', ('code', '=', 'stock.scrap'),
                '|', ('code', '=', 'stock.picking'),
                '|', ('prefix', '=', 'WH/IN/'),
                '|', ('prefix', '=', 'WH/INT/'),
                '|', ('prefix', '=', 'WH/OUT/'),
                '|', ('prefix', '=', 'WH/PACK/'),
                ('prefix', '=', 'WH/PICK/')
            ])

            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where (" \
                  "code ='stock.lot.serial' " \
                  "or code ='stock.lot.tracking' " \
                  "or code ='stock.orderpoint'" \
                  "or code ='stock.picking'" \
                  "or code ='stock.quant.package'" \
                  "or code ='stock.scrap'" \
                  "or code ='stock.picking'" \
                  "or prefix ='WH/IN/'" \
                  "or prefix ='WH/INT/'" \
                  "or prefix ='WH/OUT/'" \
                  "or prefix ='WH/PACK/'" \
                  "or prefix ='WH/PICK/'" \
                  ");"
            self._cr.execute(sql)
        except Exception, e:
            raise Warning(e)
        return True

    @api.multi
    def remove_account(self):
        to_removes = [
            # 清除财务会计单据
            ['account.voucher.line', ],
            ['account.voucher', ],
            ['account.bank.statement', ],
            ['account.bank.statement.line', ],
            ['account.payment', ],
            ['account.analytic.line', ],
            ['account.invoice.line', ],
            ['account.invoice', ],
            ['account.partial.reconcile', ],
            ['account.move.line', ],
            ['account.move', ],
        ]
        try:
            for line in to_removes :
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table_exist:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)

                    # 更新序号
                    seqs = self.env['ir.sequence'].search([
                        '|', ('code', '=', 'account.reconcile'),
                        '|', ('code', '=', 'account.payment.customer.invoice'),
                        '|', ('code', '=', 'account.payment.customer.refund'),
                        '|', ('code', '=', 'account.payment.supplier.invoice'),
                        '|', ('code', '=', 'account.payment.supplier.refund'),
                        ('code', '=', 'account.payment.transfer')
                    ])

                    for seq in seqs:
                        seq.write({
                            'number_next': 1,
                        })
                    sql = "update ir_sequence set number_next=1 where (" \
                          "code ='account.reconcile' " \
                          "or code ='account.payment.customer.invoice' " \
                          "or code ='account.payment.customer.refund' " \
                          "or code ='account.payment.supplier.invoice' " \
                          "or code ='account.payment.supplier.refund' " \
                          ");"
                    self._cr.execute(sql)
        except Exception, e:
            raise Warning(e)
        return True

    @api.multi
    def remove_message(self):
        to_removes = [
            # 清除消息数据
            ['mail.message', ],
        ]
        try:
            for line in to_removes :
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table_exist:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception, e:
            raise Warning(e)
        return True

    @api.multi
    def remove_workflow(self):
        to_removes = [
            # 清除工作流
            ['wkf.workitem', ],
            ['wkf.instance', ],
        ]
        try:
            for line in to_removes :
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table_exist:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)

        except Exception, e:
            raise Warning(e)
        return True


    def data_transfer(self): #轉團員檔及團員眷屬檔
        sql = "INSERT INTO normal_p(w_id, number, name, cellphone, con_phone, con_phone2, zip, rec_addr, habbit_donate, is_merge, is_donate, temp_key_in_user, db_chang_date) "\
              " SELECT 團員編號, 序號, 姓名, 手機, 電話一, 電話二, 郵遞區號, 通訊地址, cast(捐助種類編號 as Integer), case when 收據寄送='N' then TRUE else FALSE end as 收據寄送, case when 是否捐助='N' then FALSE else TRUE end as 是否捐助, 輸入人員, case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期 FROM 新團員眷屬檔 WHERE 團員編號 <>'' "
        self._cr.execute(sql) # 輸入769339筆資料, 花費14.961秒

        sql = " DELETE FROM 舊團員眷屬檔 WHERE 團員編號 IN (SELECT a.團員編號 FROM 舊團員眷屬檔 a INNER JOIN 新團員眷屬檔 b ON a.團員編號=b.團員編號 AND a.序號 = b.序號)"
        self._cr.execute(sql)  # 刪除舊團員眷屬檔與新新團員眷屬檔重複資料 共645386筆 花費約17.766秒

        sql = "INSERT INTO normal_p(w_id, number, name, cellphone, con_phone, con_phone2, zip, rec_addr, habbit_donate, is_merge, is_donate, temp_key_in_user, db_chang_date) "\
              " SELECT 團員編號, 序號, 姓名, 手機, 電話一, 電話二, 郵遞區號, 通訊地址, cast(捐助種類編號 as Integer), case when 收據寄送='N' then TRUE else FALSE end as 收據寄送, case when 是否捐助='N' then FALSE else TRUE end as 是否捐助, 輸入人員, case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期 FROM 舊團員眷屬檔 WHERE 團員編號 <>''"
        self._cr.execute(sql) # 轉入舊團員眷屬檔資料共11筆, 花費0.061秒

        sql = "SELECT a.* INTO 暫存新團員檔 FROM 新團員檔 a  LEFT JOIN 新團員眷屬檔 b ON a.團員編號 = b.團員編號 AND a.姓名=b.姓名  WHERE b.姓名 IS NULL"
        self._cr.execute(sql) # 找出沒有在新團員眷屬檔卻在新團員檔的資料, 此資料一定是戶長, 共7885筆 花費大約0.702秒

        sql = "UPDATE 暫存新團員檔 SET 戶長 = '1'"
        self._cr.execute(sql)  # 將這些資料的戶長欄位寫入 1 , 以利以後做戶長的判斷

        sql = "INSERT INTO normal_p(head_of_household, w_id, name, cellphone, con_phone, con_phone2, zip_code, con_addr, habbit_donate, rec_send, donate_cycle, rec_type, create_date,"\
              "ps, report_send, thanks_send, self, bank_check, prints_id, self_iden, bank_id, bank, bank_id2, bank2, account, prints_date, ps2, temp_key_in_user, db_chang_date)"\
              "SELECT CAST(戶長 AS INTEGER), 團員編號, 姓名, 手機, 電話一, 電話二, 郵遞區號, 通訊地址, cast(捐助種類編號 as Integer), case when 收據寄送='Y' then TRUE else FALSE end, CAST(捐助週期 AS INTEGER), case when 年收據='N' then 1 else 2 end, case when 建檔日期='' then NULL else cast(建檔日期 as date) end,"\
              "備註, case when 報表寄送='N' then FALSE else TRUE end,case when 感謝狀寄送='N' then FALSE else TRUE end, 自訂排序, case when 銀行核印='N' then FALSE else TRUE end,核印批號, 身份證號, 扣款銀行代碼, 扣款銀行, 扣款分行代碼, 扣款分行, 銀行帳號, 核印日期, 約定轉帳備註,"\
              "輸入人員, case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期 FROM 暫存新團員檔 WHERE 團員編號 <>''"
        self._cr.execute(sql) # 轉入找出沒有在新團員眷屬檔卻在新團員檔的資料, 共 7885 筆, 花費 0.118 秒

        sql = " DELETE FROM 新團員檔 WHERE 團員編號 IN (SELECT a.團員編號 FROM 暫存新團員檔 a INNER JOIN 新團員檔 b ON a.團員編號=b.團員編號 AND a.姓名=b.姓名)"
        self._cr.execute(sql)  # 刪除 7885 筆資料, 花費 0.590 秒

        sql = "DROP TABLE 暫存新團員檔"
        self._cr.execute(sql) # 刪除暫存表

        sql = "SELECT a.* INTO 暫存新團員檔 FROM 新團員檔 a "\
              " LEFT JOIN 新團員眷屬檔 b ON a.團員編號 = b.團員編號 AND b.序號='1' AND a.姓名=b.姓名 "\
              " WHERE b.姓名 IS NOT NULL"
        self._cr.execute(sql) # 找出新團員眷屬檔與新團員檔且序號為 1 的戶長, 共 234816 筆, 花費 1.116  秒

        sql = "UPDATE 暫存新團員檔 SET 戶長 = '1'"
        self._cr.execute(sql)  # 將這些資料的戶長欄位寫入 1 , 以利以後做戶長的判斷

        sql = "UPDATE normal_p "\
              " SET head_of_household = CAST(a.戶長 AS INTEGER), cellphone = a.手機, con_phone = a.電話一, con_phone2 = a.電話二, donate_cycle = cast(a.捐助週期 as Integer), zip_code = a.郵遞區號, con_addr = a.通訊地址, "\
              " merge_report = case when a.年收據='N' then FALSE else TRUE end, ps = a.備註, temp_cashier = a.收費員編號, rec_send = case when a.收據寄送='N' then FALSE else TRUE end, report_send = case when a.報表寄送='N' then FALSE else TRUE end, "\
              " thanks_send = case when a.感謝狀寄送='N' then FALSE else TRUE end, prints = case when a.銀行核印='N' then FALSE else TRUE end, prints_id = a.核印批號, self_iden = a.身份證號, bank_id = a.扣款銀行代碼, bank = a.扣款銀行, "\
              " bank_id2 = a.扣款分行代碼, bank2 = a.扣款分行, account = a.銀行帳號, prints_date = a.核印日期, "\
              " ps2 = a.約定轉帳備註, temp_key_in_user = a.輸入人員, db_chang_date = case when a.異動日期='' then NULL else cast(a.異動日期 as date) end "\
              " FROM 暫存新團員檔 a WHERE a.團員編號 = normal_p.w_id and a.姓名 = normal_p.name AND normal_p.number = '1'"
        self._cr.execute(sql) # 更新新團員眷屬檔與新團員檔且序號為 1 的戶長資料, 共 234816 筆 , 花費  9.097  秒

        sql = " DELETE FROM 新團員檔 WHERE 團員編號 IN (SELECT a.團員編號 FROM 暫存新團員檔 a INNER JOIN 新團員檔 b ON a.團員編號=b.團員編號 AND a.姓名=b.姓名)"
        self._cr.execute(sql)  # 刪除 234816 筆資料, 花費 4.315 秒

        sql = "DROP TABLE 暫存新團員檔"
        self._cr.execute(sql)  # 刪除暫存表

        sql = "UPDATE 新團員檔 SET 戶長 = '1'"
        self._cr.execute(sql)  # 將這些資料的戶長欄位寫入 1 , 共 12464 筆, 花費 0.047 秒

        sql = "SELECT normal_p.w_id, normal_p.name, MAX(normal_p.id) INTO 暫存新團員檔 FROM normal_p, 新團員檔 a WHERE a.團員編號 = normal_p.w_id and a.姓名 = normal_p.name GROUP BY normal_p.w_id, normal_p.name"
        self._cr.execute(sql) # 篩選 normal_p 重複資料, 共 12464 筆 , 花費 0.531 秒

        sql = "UPDATE normal_p "\
              " SET head_of_household = CAST(a.戶長 AS INTEGER), cellphone = a.手機, con_phone = a.電話一, con_phone2 = a.電話二, donate_cycle = cast(a.捐助週期 as Integer), zip_code = a.郵遞區號, con_addr = a.通訊地址,"\
              " merge_report = case when a.年收據='N' then FALSE else TRUE end, ps = a.備註, temp_cashier = a.收費員編號, rec_send = case when a.收據寄送='N' then FALSE else TRUE end, report_send = case when a.報表寄送='N' then FALSE else TRUE end,"\
              " thanks_send = case when a.感謝狀寄送='N' then FALSE else TRUE end, prints = case when a.銀行核印='N' then FALSE else TRUE end, prints_id = a.核印批號, self_iden = a.身份證號, bank_id = a.扣款銀行代碼, bank = a.扣款銀行,"\
              " bank_id2 = a.扣款分行代碼, bank2 = a.扣款分行, account = a.銀行帳號, prints_date = a.核印日期,"\
              " ps2 = a.約定轉帳備註, temp_key_in_user = a.輸入人員, db_chang_date = case when a.異動日期='' then NULL else cast(a.異動日期 as date) end"\
              " FROM 新團員檔 a, 暫存新團員檔 b WHERE a.團員編號 = normal_p.w_id and a.姓名 = normal_p.name AND normal_p.id = b.max"
        self._cr.execute(sql) # 轉入最後的戶長資料, 共 12464 筆, 花費 18.82 秒

        sql = "DROP TABLE 暫存新團員檔"
        self._cr.execute(sql)  # 刪除暫存表

        sql = "UPDATE normal_p SET temp_cashier = a.收費員編號 FROM 新團員檔2 a WHERE a.團員編號 = normal_p.w_id"
        self._cr.execute(sql) # 更新 776087 筆資料, 花費22.857秒
        sql = "UPDATE normal_p SET active = TRUE"
        self._cr.execute(sql)  # 把所有捐款者資料的active設為TRUE, 不然基本資料會什麼都看不見, 共777235筆 花費15.163秒

        # 以上全程150.288秒, 約 3 分鐘
        return True

    def set_leader(self): # 設定戶長
        sql = " UPDATE normal_p SET parent = a.id FROM normal_p a WHERE a.w_id = normal_p.w_id and a.head_of_household = 1 "
        self._cr.execute(sql) #更新778065筆資料, 花費26.471秒
        return True

    def receipt_transfer(self): # 轉捐款檔
        sql = " INSERT INTO donate_order(paid_id,donate_id,donate_w_id,donate_w_id_number,donate_type,donate,donate_total,donate_date,report_year,clerk,db_chang_date, temp_key_in_user) SELECT 收費編號,捐款編號,團員編號,序號,cast(捐助種類編號 as Integer),捐款金額,捐款總額,case when 捐款日期='' then NULL WHEN 捐款日期='.' THEN NULL else cast(捐款日期 as date) end as 捐款日期,case when 收據年度開立 = 'N' then FALSE else TRUE end as report_year,收費員編號, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期, 輸入人員 FROM 新捐款檔"
        self._cr.execute(sql)  # 新捐款檔 共3017899筆 花費約98.739秒

        sql = " DELETE FROM 新捐款歷史檔 WHERE 捐款編號 IN (SELECT a.捐款編號 FROM 新捐款歷史檔 a INNER JOIN 新捐款檔 b ON a.捐款編號=b.捐款編號 AND a.捐款日期 = b.捐款日期 AND a.團員編號 = b.團員編號)"
        self._cr.execute(sql)  # 刪除新捐款歷史檔與新捐款檔重複的資料, 共 5558 筆 , 花費26.560秒

        sql = " INSERT INTO donate_order(paid_id,donate_id,donate_w_id,donate_w_id_number,donate_type,donate,donate_total,donate_date,report_year,clerk,db_chang_date, temp_key_in_user) SELECT 收費編號,捐款編號,團員編號,序號,cast(捐助種類編號 as Integer),捐款金額,捐款總額,case when 捐款日期='' then NULL WHEN 捐款日期='.' THEN NULL else cast(捐款日期 as date) end as 捐款日期,case when 收據年度開立 = 'N' then FALSE else TRUE end as report_year,收費員編號, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期, 輸入人員 FROM 新捐款歷史檔"
        self._cr.execute(sql)  # 轉入刪除後的新捐款歷史檔, 轉入87651 筆, 花費1.707秒

        sql = " DELETE FROM 新手寫捐款檔 WHERE 捐款編號 IN (SELECT a.捐款編號 FROM 新手寫捐款檔 a INNER JOIN donate_order b ON case when a.捐款日期='' then NULL WHEN a.捐款日期='.' THEN NULL else cast(a.捐款日期 as date) end = b.donate_date AND a.捐款編號=b.donate_id AND a.團員編號 = b.donate_w_id)"
        self._cr.execute(sql)  # 刪除新手寫捐款檔與donate_order重複資料 共 53491 筆 花費約31.512秒

        sql = " INSERT INTO donate_order(paid_id, donate_book_code, donate_id,donate_w_id,donate_w_id_number,donate_type,donate,donate_total,donate_date,clerk, state, ps, db_chang_date, temp_key_in_user) SELECT 收費編號, 簿冊編號, 捐款編號,團員編號,序號,cast(捐助種類編號 as Integer),捐款金額,捐款總額,case when 捐款日期='' then NULL WHEN 捐款日期='.' THEN NULL else cast(捐款日期 as date) end as 捐款日期,收費員編號, case when 作廢 = 'N' then 2 else 1 end, 備註, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期, 輸入人員 FROM 新手寫捐款檔"
        self._cr.execute(sql)  # 轉入新手寫捐款檔 共145147 筆 花費約 2.686秒

        sql = " DELETE FROM 舊捐款檔 WHERE 捐款編號 IN (SELECT a.捐款編號 FROM 舊捐款檔 a INNER JOIN donate_order b ON case when a.捐款日期='' then NULL WHEN a.捐款日期='.' THEN NULL else cast(a.捐款日期 as date) end = b.donate_date AND a.捐款編號=b.donate_id AND a.團員編號 = b.donate_w_id)"
        self._cr.execute(sql)  # 刪除舊捐款檔與donate_order重複資料 共995746筆 花費約123.095秒

        sql = " INSERT INTO donate_order(paid_id, donate_id,donate_w_id,donate_w_id_number,donate_type,donate,donate_total,donate_date,report_year,clerk,db_chang_date, temp_key_in_user) SELECT 收費編號, 捐款編號,團員編號,序號,cast(捐助種類編號 as Integer),捐款金額,捐款總額,case when 捐款日期='' then NULL WHEN 捐款日期='.' THEN NULL else cast(捐款日期 as date) end as 捐款日期,case when 收據年度開立 = 'N' then FALSE else TRUE end as report_year,收費員編號, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期, 輸入人員 FROM 舊捐款檔"
        self._cr.execute(sql)  # 轉入舊捐款檔 共5168197 筆 花費約152.243秒

        sql = " DELETE FROM 舊手寫捐款檔 WHERE 捐款編號 IN (SELECT a.捐款編號 FROM 舊手寫捐款檔 a INNER JOIN donate_order b ON case when a.捐款日期='' then NULL WHEN a.捐款日期='.' THEN NULL else cast(a.捐款日期 as date) end = b.donate_date AND a.捐款編號=b.donate_id AND a.團員編號 = b.donate_w_id)"
        self._cr.execute(sql)  # 刪除舊手寫捐款檔與新手寫捐款檔)重複資料 共152023筆 花費約106.258秒

        sql = " INSERT INTO donate_order(paid_id, donate_book_code, donate_id,donate_w_id,donate_w_id_number,donate_type,donate,donate_total,donate_date,clerk, state, ps, db_chang_date, temp_key_in_user) SELECT 收費編號, 簿冊編號, 捐款編號,團員編號,序號,cast(捐助種類編號 as Integer),捐款金額,捐款總額,case when 捐款日期='' then NULL WHEN 捐款日期='.' THEN NULL else cast(捐款日期 as date) end as 捐款日期,收費員編號, case when 作廢 = 'N' then 2 else 1 end, 備註, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期, 輸入人員 FROM 舊手寫捐款檔"
        self._cr.execute(sql)  # 轉入舊手寫捐款檔 共 0 筆 花費 0 秒

        sql = "INSERT INTO hand_book(book_code,name,take_date,recycle_date,key_in_total_money,build_date,ps,key_in_user_data) "\
              " SELECT 簿冊編號,領取人,case when 領取日期='' then Null else cast(領取日期 as Date) end as 領取日期,case when 回收日期='' then Null else cast(回收日期 as Date) end as 回收日期,已收總金額,case when 建檔日期='' then Null else cast(建檔日期 as Date) end as 建檔日期,備註,輸入人員 from 新手寫簿冊檔"
        self._cr.execute(sql) # 轉入1539 筆資料, 花費 0.045 秒
        # 以上全程花費371.763秒, 約 6.2 分鐘
        # donate_order 全資料共8379183筆
        return True

    def set_donor(self): # normal.p 關聯捐款檔 設定捐款者
        sql = " UPDATE donate_order SET donate_member = a.id FROM normal_p a WHERE a.w_id = donate_order.donate_w_id AND a.number = donate_order.donate_w_id_number AND donate_order.donate_w_id_number <> '' "
        self._cr.execute(sql) # 關聯資料共8404465筆 花費3516.614秒, 約 58 分鐘
        return True

    def set_last_donate_data(self):
        sql = "SELECT MAX(donate_date), donate_member INTO search_last_order FROM donate_order GROUP BY donate_member"
        self._cr.execute(sql)  # 篩選出所有捐款者的最後一次捐款紀錄 共 737710 筆, 花費55.424秒
        sql = "SELECT a.donate_id, a.donate_member, a.donate_date, a.donate, a.donate_type INTO get_last_order FROM donate_order a , search_last_order b WHERE a.donate_date = b.max AND a.donate_member = b.donate_member ORDER BY a.donate_member"
        self._cr.execute(sql)  # 從donate_order 篩選出 資料共 812687 筆, 花費27.773秒
        sql = "UPDATE normal_p SET last_donate_date = a.donate_date, last_donate_type = a.donate_type, last_donate_money = a.donate FROM get_last_order a WHERE a.donate_member = normal_p.id"
        self._cr.execute(sql) # 更新normal_p 欄位資料, 共 737705 筆, 花費20.733秒
        sql = "DROP TABLE search_last_order"
        self._cr.execute(sql)  # 刪除暫存表
        sql = "DROP TABLE get_last_order"
        self._cr.execute(sql)  # 刪除暫存表
        # 以上全程花費73.881秒, 約 1.2 分鐘
        return True

    def set_worker(self): #員工檔轉進 res.users 大約15秒
        sql = "INSERT INTO worker_data(now_job,birth,sex,con_phone2,self_iden,lev_date,w_id,con_addr,ps,cellphone,name,con_phone,highest_stu,come_date,db_chang_date) " \
              " SELECT 職稱, case when 出生日期='' then NULL else cast(出生日期 as date) end as 出生日期,性別, 電話二, 身份證號,case when 離職日期='' then NULL else cast(離職日期 as date) end as 離職日期, 員工編號, 通訊地址,備註,手機,姓名, 電話一,最高學歷,case when 到職日期='' then NULL else cast(到職日期 as date) end as 到職日期,case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期  FROM 新員工檔"
        self._cr.execute(sql)
        sql = "INSERT INTO c_worker(now_job,birth,sex,con_phone2,self_iden,lev_date,w_id,con_addr,ps,cellphone,name,con_phone,highest_stu,come_date,db_chang_date) " \
              " SELECT 職稱, case when 出生日期='' then NULL else cast(出生日期 as date) end as 出生日期,性別, 電話二, 身份證號,case when 離職日期='' then NULL else cast(離職日期 as date) end as 離職日期, 員工編號, 通訊地址,備註,手機,姓名, 電話一,最高學歷,case when 到職日期='' then NULL else cast(到職日期 as date) end as 到職日期,case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期  FROM 新員工檔"
        self._cr.execute(sql)
        employee_data = self.env['worker.data'].search([])
        for line in employee_data:
            self.env['res.users'].create({
                'login': line.w_id,
                'password':line.w_id,
                'name':line.name,
                'now_job': line.now_job,
                'birth': line.birth,
                'sex': line.sex,
                'con_phone2': line.con_phone2,
                'self_iden': line.self_iden,
                'lev_date': line.lev_date,
                'w_id': line.w_id,
                'email': line.email,
                'con_addr': line.con_addr,
                'ps': line.ps,
                'cellphone': line.cellphone,
                'name': line.name,
                'con_phone': line.con_phone,
                'highest_stu': line.highest_stu,
                'come_date': line.come_date,
                'db_chang_date': line.db_chang_date,
                'job_type': line.job_type
            })

    def set_worker_associated(self):  # normal_p 關聯 res.users
        sql = " UPDATE normal_p set key_in_user = a.id from res_users a where a.login = normal_p.temp_key_in_user"
        self._cr.execute(sql) # 關聯資料共 720208 筆,  花費 19.919 秒
        return True

    def set_coffin_data(self): # 施棺檔轉入 coffin_base 共 14256筆, 花費0.21秒
        sql = "UPDATE 新施棺檔 SET 施棺日期='2009-06-30' WHERE 施棺日期='2009-06-31' "
        self._cr.execute(sql)
        sql = "UPDATE 新施棺檔 SET 施棺日期='2010-08-27' WHERE 施棺日期='2010-80-27' "
        self._cr.execute(sql)
        sql = "INSERT INTO coffin_base(coffin_id, donate_type, create_date, donate_price, finish, \"user\", coffin_date_year, coffin_date_group, coffin_date, geter, dealer, cellphone, con_phone, con_phone2, zip_code, con_addr, donater_ps, ps, temp_key_in_user, db_chang_date) " \
              " SELECT 施棺編號, 捐助方式, case when 建檔日期='' then NULL WHEN 建檔日期='.' THEN NULL else cast(建檔日期 as date) end as 建檔日期, CAST(已捐總額 AS INTEGER), case when 結案='N' then FALSE else TRUE end as 結案, 受施者, 年度, case when 期別='' then NULL else CAST(期別 AS INTEGER) end as 期別, case when 施棺日期='' then NULL WHEN 施棺日期='.' THEN NULL else cast(施棺日期 as date) end as 施棺日期, 領款人, 處理者, 手機, 電話一, 電話二, 郵遞區號, 通訊地址, 捐款者備註, 備註, 輸入人員, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期 FROM 新施棺檔"
        self._cr.execute(sql) # 輸入共15236筆資料,花費0.187秒
        # 施棺編號 00236 之施棺日期為 2009-06-31, 修改為2009-06-30
        # 施棺編號 01944, 01945, 01946, 01947 之施棺日期為 2010-80-27  修改為2010-08-27
        sql = "UPDATE coffin_base set dead_date = a.coffin_date from coffin_base a where a.id = coffin_base.id"
        self._cr.execute(sql)  # 計算資料共15236筆, 花費0.092秒 ; 舊資料設定領款日期等於死亡日期
        sql = "UPDATE coffin_base set donate_apply_price = a.donate_price from coffin_base a where a.id = coffin_base.id and a.finish IS TRUE"
        self._cr.execute(sql)  # 計算資料共12521筆, 花費 0.091秒 ; 已結案的舊資料設定累積金額等於申請金額
        return True

    def set_coffin_donate(self): # 施棺捐款檔轉入 old_coffin_donation
        sql = "INSERT INTO old_coffin_donation(coffin_id, donate_id, donate_price) SELECT 施棺編號, 捐款編號, CAST(捐款金額 AS INTEGER) FROM 新施棺捐款檔"
        self._cr.execute(sql) # 施棺捐款檔轉入 old_coffin_donation 共187017筆, 花費0.898秒
        return True

    def set_donate_single(self):
        sql = "SELECT donate_id,donate_w_id,MIN(donate_w_id_number), donate_date INTO temp_table2 FROM donate_order WHERE donate_w_id_number <> '' AND donate_w_id <> '' GROUP BY donate_id, donate_w_id, donate_date"
        self._cr.execute(sql)  # 挑選捐款編號作為唯一值, 並挑出序號值最小的資料共3123219筆, 花費128.377秒
        sql = "INSERT INTO donate_single(donate_id,donate_member_w_id,donate_member_number, donate_date) SELECT donate_id,donate_w_id, min, donate_date FROM temp_table2"
        self._cr.execute(sql)  # 寫入收據編號, 舊團員編號, 團員序號及捐款日期 資料共3123219筆, 花費約57.505秒
        sql = "UPDATE donate_single SET donate_member_w_id = a.donate_w_id, donate_total = a.donate_total, donate_date = case when a.donate_date IS NULL then NULL else cast(a.donate_date as date) end, temp_work_id=a.clerk,year_receipt_send =case when a.report_year='N' then FALSE else TRUE end,paid_id=a.paid_id,temp_key_in_user = a.temp_key_in_user FROM donate_order a WHERE donate_single.donate_id = a.donate_id AND donate_single.donate_member_number = a.donate_w_id_number AND donate_single.donate_date = a.donate_date"
        self._cr.execute(sql)  # 更新資料共3123153筆, 花費約410.914秒
        sql = "UPDATE donate_single SET donate_member = a.id, receipt_send = a.rec_send, report_send = a.report_send, year_receipt_send = a.merge_report, name = a.name, self_iden = a.self_iden, cellphone = a.cellphone, con_phone = a.con_phone, zip_code = a.zip_code ,con_addr = a.con_addr, zip = a.zip, rec_addr = a.rec_addr FROM normal_p a WHERE a.w_id = donate_single.donate_member_w_id AND a.number = donate_single.donate_member_number"
        self._cr.execute(sql)  # 更新資料共3120807筆, 花費約538.129秒
        # 共有 2392 筆 捐款資料關聯不到normal_p, 也就是依照團員編號還是找不到人

        sql = "UPDATE donate_single SET active = TRUE, state = 2, sreceipt_number = 1"
        self._cr.execute(sql) # 更新 3123219 筆資料, 花費208.516秒
        sql = "DROP TABLE temp_table2"
        self._cr.execute(sql)  # 刪除暫存表
        # 以上全程花費1620.507秒, 約 27 分鐘
        return True

    def set_donate_single_associated(self): # donate_single 關聯 donate_order
        sql = "UPDATE donate_order SET donate_list_id = a.id FROM donate_single a WHERE a.donate_id = donate_order.donate_id AND a.donate_date = donate_order.donate_date"
        self._cr.execute(sql) # 關聯資料共8378848筆, 原需花費6040.240秒, 資料庫優化後, 只需3053.407秒, 前提是沒有建索引
        sql = "UPDATE donate_order SET state = 1 , active = TRUE WHERE state IS NULL" # 將所有的捐款明細的狀態設為已產生
        self._cr.execute(sql) # 資料共8273747筆, 花費1847.032秒
        # 以上全程花費3602.243秒, 約 61 分鐘
        return True

    def set_coffin_id(self): # 舊施棺明細關聯施棺檔
        sql = "UPDATE old_coffin_donation SET old_coffin_donation_id = a.id FROM coffin_base a WHERE a.coffin_id = old_coffin_donation.coffin_id"
        self._cr.execute(sql)  # 關聯資料共187004筆, 花費2.360秒
        return True

    def set_coffin_donate_single_associated(self): # 舊施棺明細關聯donate_single, 將捐款者姓名寫入old_coffin_donation的donor欄位
        sql = "UPDATE old_coffin_donation SET donor = a.name FROM donate_single a WHERE a.donate_id = old_coffin_donation.donate_id"
        self._cr.execute(sql)  # 更新資料共186999筆, 花費27.913秒
        return True

    def compute_coffin_donate(self):
        sql = "SELECT SUM(donate),MAX(donate_total),donate_id, donate_date INTO donate_difference_table FROM donate_order WHERE donate_type = 3 AND donate_total <> 0 GROUP BY donate_id, donate_date HAVING SUM(donate) <> MAX(donate_total)"
        self._cr.execute(sql) # 全捐款明細所計算資料共15907筆, 花費13.893秒
        sql = "ALTER TABLE donate_difference_table RENAME donate_id TO temp_donate_id"
        self._cr.execute(sql) # 變更臨時表的欄位名稱
        sql = "ALTER TABLE donate_difference_table RENAME donate_date TO temp_donate_date"
        self._cr.execute(sql)  # 變更臨時表的欄位名稱
        sql = "SELECT * INTO reorganization_table FROM donate_order a INNER JOIN donate_difference_table b ON a.donate_id = b.temp_donate_id AND a.donate_date = b.temp_donate_date"
        self._cr.execute(sql)  # 需計算的資料共59066筆, 花費2.830秒
        sql = "SELECT * FROM donate_difference_table"
        self._cr.execute(sql)
        index_donate = self._cr.dictfetchall()
        donate_total = 0
        num = 0
        j=0
        for line in index_donate:
            j=j+1
            # if j % 100 == 0:
            #     print u"第%s筆 捐款編號: %s" % (j,line['temp_donate_id'])
            donate_total = line['max']
            if line['temp_donate_date']:
                sql = "SELECT * FROM reorganization_table WHERE donate_id = '%s' AND donate_date = '%s' ORDER BY donate_w_id_number" % (line['temp_donate_id'],line['temp_donate_date'])
                self._cr.execute(sql)
            else:
                continue
            group_donate_data = self._cr.dictfetchall()
            num = len(group_donate_data)
            check_donate_data = True
            temp_donate_w_id = ''
            if num != 0:
                for line in group_donate_data:
                    if temp_donate_w_id == '':
                        temp_donate_w_id = line['donate_w_id']
                    elif temp_donate_w_id == line['donate_w_id']:
                        continue
                    elif temp_donate_w_id != line['donate_w_id']:
                        check_donate_data = False
                if check_donate_data == True:
                    for row in group_donate_data[0:1]:
                        sql = "UPDATE reorganization_table SET donate = %s WHERE donate_id = '%s' AND donate_w_id_number = '%s' AND donate_date = '%s'" % (donate_total,line['temp_donate_id'], row['donate_w_id_number'], line['temp_donate_date'])
                        self._cr.execute(sql) # 17821筆資料, 花費約4分鐘

        sql = "UPDATE donate_order SET donate = a.donate FROM reorganization_table a where donate_order.donate_id = a.donate_id and donate_order.donate_w_id = a.donate_w_id AND donate_order.donate_w_id_number = a.donate_w_id_number AND donate_order.donate_date = a.donate_date"
        self._cr.execute(sql) # 共68725筆資料, 更新至donate_order, 原需花費 266.807 秒, 資料庫優化後, 花費68.162秒
        sql = "DROP TABLE reorganization_table"
        self._cr.execute(sql)  # 刪除暫存表
        sql = "DROP TABLE donate_difference_table"
        self._cr.execute(sql)  # 刪除暫存表
        # 以上花費約 10 分鐘

        sql = "UPDATE donate_order SET available_balance = donate_order.donate"
        self._cr.execute(sql)  # 計算資料共8379183筆, 原需花費961.930秒, 資料庫優化後, 花費383.514秒
        sql = "UPDATE donate_order SET available_balance = 0 FROM old_coffin_donation a WHERE a.donate_id = donate_order.donate_id AND donate_order.donate_type = 3"
        self._cr.execute(sql)  # 計算資料共342300筆, 花費132.583秒 ;  共341528筆資料施棺的捐款金額為 0
        sql = "UPDATE donate_order SET use_amount = TRUE WHERE available_balance = 0 and donate_type = 3"
        self._cr.execute(sql)  # 計算資料共368147筆, 花費52.629秒
        sql = "UPDATE donate_order SET used_money = donate_order.donate WHERE available_balance = 0 and donate_type = 3"
        self._cr.execute(sql)  # 計算資料共368147筆, 花費29.987秒
        # 全程花費約 40 分鐘
        return True

    def set_consultant_data(self): # 轉顧問檔資料進normal.p, 顧問檔共131筆資料
        sql = "INSERT INTO normal_p(name , con_addr) SELECT 姓名, 戶籍通訊地址 FROM 新顧問檔 EXCEPT SELECT name, con_addr FROM normal_p"
        self._cr.execute(sql) #  轉入資料共130 筆, 花費5.583秒

        sql = "UPDATE normal_p " \
              " SET consultant_id = a.顧問編號, cellphone = a.手機, con_phone = a.電話一, con_phone2 = a.電話二, zip_code = a.戶籍郵遞區號, con_addr = a.戶籍通訊地址, zip = a.郵遞區號, rec_addr = a.通訊地址, hire_date = case when a.聘顧日期='' then NULL else cast(a.聘顧日期 as date) end, build_date = case when a.建檔日期='' then NULL else cast(a.建檔日期 as date) end, " \
              " ps = a.備註, temp_cashier = a.收費員編號, rec_send = case when a.收據寄送='N' then FALSE else TRUE end, report_send = case when a.報表寄送='N' then FALSE else TRUE end, thanks_send = case when a.感謝狀寄送='N' then FALSE else TRUE end, self = a.自訂排序,temp_key_in_user = a.輸入人員, db_chang_date = case when a.異動日期='' then NULL else cast(a.異動日期 as date) end " \
              " FROM 新顧問檔 a WHERE a.姓名 = normal_p.name and a.戶籍通訊地址 = normal_p.con_addr"
        self._cr.execute(sql) #顧問檔更新normal.p的資料共202筆, 花費 0.711 秒
        return True

    def set_member_data(self): # 轉會員檔資料進normal.p, 會員檔共7303筆資料
        sql = "INSERT INTO normal_p(name , con_addr) SELECT 姓名, 戶籍通訊地址 FROM 新會員檔 EXCEPT SELECT name, con_addr FROM normal_p"
        self._cr.execute(sql)  # 轉入新會員檔有資料但normal.p沒有資料的, 共有4730筆資料, 花費0.701 秒

        sql = "UPDATE normal_p " \
              " SET member_id = a.會員編號, cellphone = a.手機, con_phone = a.電話一, con_phone2 = a.電話二, zip_code = a.戶籍郵遞區號, con_addr = a.戶籍通訊地址, zip = a.郵遞區號, rec_addr = a.通訊地址, build_date = case when a.建檔日期='' then NULL else cast(a.建檔日期 as date) end, self_iden = a.身份證號, member_type = case when 會員種類編號='' then NULL else CAST(會員種類編號 AS INTEGER) end, " \
              " ps = a.備註, temp_cashier = a.收費員編號, rec_send = case when a.收據寄送='N' then FALSE else TRUE end, booklist = case when a.名冊列印='N' then FALSE else TRUE end, self = a.自訂排序,temp_key_in_user = a.輸入人員, db_chang_date = case when a.異動日期='' then NULL else cast(a.異動日期 as date) end " \
              " FROM 新會員檔 a WHERE a.姓名 = normal_p.name and a.戶籍通訊地址 = normal_p.con_addr"
        self._cr.execute(sql)  # 會員檔更新normal.p的資料共7399筆, 花費1.643 秒
        return True

    def set_consultant(self): #顧問收費檔轉檔
        sql = "INSERT INTO consultant_fee(consultant_id,year,fee_code,fee_payable,fee_date,clerk_id,temp_key_in_user,create_date) " \
              " SELECT 顧問編號,年度,收費編號,應繳金額,case when 收費日期='' then NULL else cast(收費日期 as date) end as 收費日期,收費員編號,輸入人員,case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期 from 新顧問收費檔 "
        self._cr.execute(sql)  # 顧問收費檔共516筆資料, 花費0.013秒
        sql = "UPDATE consultant_fee SET normal_p_id = a.id FROM normal_p a WHERE a.consultant_id = consultant_fee.consultant_id"
        self._cr.execute(sql) # 更新顧問收費檔共515筆資料, 花費0.563 秒, 顧問編號 V00198在normal_p沒有找到, 顧問檔也沒有找到
        return True

    def set_member(self): #會員收費檔轉檔
        sql = "SELECT DISTINCT on (member_id) * FROM normal_p WHERE member_id <>'' "
        self._cr.execute(sql)
        dict = self._cr.dictfetchall()  #normal.p有會員編號的資料共7304筆資料, 篩選不重複資料後, 總共7286筆資料
        # SELECT member_id FROM normal_p GROUP BY member_id HAVING (COUNT(*) > 1)  篩選出現不只一次的資料有49筆
        sql = ''
        sql = "INSERT INTO associatemember_fee(member_id,member_note_code,year,fee_code,fee_payable,fee_date,clerk_id,temp_key_in_user,create_date) " \
              " SELECT 會員編號, 會員名冊編號,年度,收費編號,應繳金額,case when 收費日期='' then NULL else cast(收費日期 as date) end as 日期,收費員編號,輸入人員,case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期 from 新會員收費檔 "
        self._cr.execute(sql)  # 會員收費檔 65499筆資料, 花費 0.600 秒
        sql = " DELETE FROM 舊會員收費檔 WHERE 收費編號 IN (SELECT a.收費編號 FROM 舊會員收費檔 a INNER JOIN 新會員收費檔 b ON a.收費編號=b.收費編號)"
        self._cr.execute(sql)  # 刪除舊會員收費檔與新會員收費檔重複的資料,共43552筆 花費0.259秒
        sql = "INSERT INTO associatemember_fee(member_id,member_note_code,year,fee_code,fee_payable,fee_date,clerk_id,temp_key_in_user,create_date) " \
              " SELECT 會員編號, 會員名冊編號,年度,收費編號,應繳金額,case when 收費日期='' then NULL else cast(收費日期 as date) end as 日期,收費員編號,輸入人員,case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期 from 舊會員收費檔 "
        self._cr.execute(sql)  # 轉入舊會員收費檔 232 筆資料, 花費 0.012 秒
        sql = "SELECT DISTINCT on (member_id) * into member_temp FROM normal_p WHERE member_id <>'' "
        self._cr.execute(sql) # 共7351筆資料, 花費0.448秒
        sql = " UPDATE associatemember_fee SET normal_p_id = b.id FROM member_temp b WHERE associatemember_fee.member_id = b.member_id"
        self._cr.execute(sql)  # 篩選不重複資料的65509筆資料寫入臨時創建的資料表中, 並與normal.p進行關聯共65509筆資料, 花費0.885 秒
        sql = "DROP TABLE member_temp"
        self._cr.execute(sql)  # 刪除暫存表
        return True

    def set_cashier_data(self): # 收費員檔轉入 cashier_base 及收費員&輸入人員對各資料表的關聯
        sql = "INSERT INTO cashier_base(c_id, name, self_iden, con_phone, con_phone2, cellphone, zip_code, con_addr, build_date, ps, temp_key_in_user, db_chang_date) "\
              " SELECT 收費員編號, 姓名, 身份證號, 電話一, 電話二, 手機, 郵遞區號, 通訊地址, case when 建檔日期='' then NULL WHEN 建檔日期='.' THEN NULL else cast(建檔日期 as date) end as 建檔日期, 備註, 輸入人員, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期 from 新收費員檔"
        self._cr.execute(sql) # 收費員檔共輸入1385 筆資料, 花費0.041秒
        sql = " DELETE FROM 舊收費員檔 WHERE 收費員編號 IN (SELECT a.收費員編號 FROM 舊收費員檔 a INNER JOIN 新收費員檔 b ON a.收費員編號=b.收費員編號)"
        self._cr.execute(sql)  # 刪除舊收費員檔與新收費員檔共1259筆 資料, 花費0.020秒
        sql = "INSERT INTO cashier_base(c_id, name, self_iden, con_phone, con_phone2, cellphone, zip_code, con_addr, build_date, ps, temp_key_in_user, db_chang_date) " \
              " SELECT 收費員編號, 姓名, 身份證號, 電話一, 電話二, 手機, 郵遞區號, 通訊地址, case when 建檔日期='' then NULL WHEN 建檔日期='.' THEN NULL else cast(建檔日期 as date) end as 建檔日期, 備註, 輸入人員, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期 from 舊收費員檔"
        self._cr.execute(sql)  # 轉入舊收費員檔共輸入 19 筆資料, 花費0.002秒

        sql = " UPDATE cashier_base set key_in_user = a.id from res_users a where a.login = cashier_base.temp_key_in_user"
        self._cr.execute(sql)  # 更新資料共1392筆, 花費0.028秒
        sql = " UPDATE normal_p set cashier_name = a.id from cashier_base a where a.c_id = normal_p.temp_cashier"
        self._cr.execute(sql)  # 更新資料共765990筆, 花費49.222秒
        sql = " UPDATE normal_p set key_in_user = a.id from res_users a where a.login = normal_p.temp_key_in_user"
        self._cr.execute(sql)  # 關聯資料共 722760 筆,花費29.335秒
        sql = " UPDATE donate_single set work_id = a.id from cashier_base a where a.c_id = donate_single.temp_work_id"
        self._cr.execute(sql)  # 更新資料共3099319筆, 花費144.298秒
        sql = " UPDATE donate_order set cashier = a.id from cashier_base a where a.c_id = donate_order.clerk"
        self._cr.execute(sql)  # 關聯資料共8553439筆, 花費1094.490秒
        sql = " UPDATE donate_single set key_in_user = a.id from res_users a where a.login = donate_single.temp_key_in_user"
        self._cr.execute(sql)  # 關聯資料共2899375筆, 花費156.132秒
        sql = " UPDATE donate_order set key_in_user = a.id from res_users a where a.login = donate_order.temp_key_in_user"
        self._cr.execute(sql)  # 關聯資料共7907563筆, 花費1609.759秒
        sql = " UPDATE associatemember_fee set key_in_user = a.id from res_users a where a.login = associatemember_fee.temp_key_in_user"
        self._cr.execute(sql)  # 關聯資料共64613筆, 花費1.247秒
        sql = " UPDATE associatemember_fee set cashier = a.id from cashier_base a where a.c_id = associatemember_fee.clerk_id"
        self._cr.execute(sql)  # 關聯資料共50254筆, 花費0.785秒
        sql = " UPDATE consultant_fee set key_in_user = a.id from res_users a where a.login = consultant_fee.temp_key_in_user"
        self._cr.execute(sql)  # 關聯資料共514筆, 花費0.018秒
        sql = " UPDATE consultant_fee set cashier = a.id from cashier_base a where a.c_id = consultant_fee.clerk_id"
        self._cr.execute(sql)  # 關聯資料共413筆, 花費 0.017 秒
        sql = " UPDATE coffin_base set key_in_user = a.id from res_users a where a.login = coffin_base.temp_key_in_user"
        self._cr.execute(sql)  # 關聯資料共15114筆, 花費0.342秒
        sql = " UPDATE donate_order set handbook_code = a.id from hand_book a where a.book_code = donate_order.donate_book_code"
        self._cr.execute(sql)  # 關聯資料共145112筆, 花費29.627秒
        # 以上全程花費3056.401秒, 約 51 分鐘
        return True

    def set_donate_family_line(self): # 關聯歷史捐款者名冊
        sql = "INSERT INTO donate_family_line(parent_id, donate_member) SELECT donate_list_id, donate_member FROM donate_order GROUP BY donate_member, donate_list_id order by donate_list_id"
        self._cr.execute(sql) # 關聯資料共8371351筆, 花費926.074秒, 約 15.5 分鐘
        return True

    def active_data(self):
        sql = "UPDATE normal_p  SET active = TRUE"
        self._cr.execute(sql)  # 把所有捐款者資料的active設為TRUE, 不然基本資料會什麼都看不見, 共782095筆 花費49.790秒
        sql = "UPDATE normal_p SET new_coding = '' "
        self._cr.execute(sql)  # 將所有的捐款者編號全部設為空 而並非是NULL, 共777235筆資料, 花費14.094秒
        sql = "UPDATE normal_p set member_type = '2' where member_type = '99' "
        self._cr.execute(sql)  # 修改資料共6639 筆, 花費0.715秒
        sql = 'UPDATE normal_p SET sequence = 1' # 團員眷屬排序用的, 將 sequence
        self._cr.execute(sql)  # 修改資料共782095 筆, 花費10.469秒
        return True

    def set_people_type(self): # 人員種類關聯
        sql = " INSERT INTO people_type(name) VALUES ('%s'),('%s'),('%s'),('%s') " % (u'捐款者',u'基本會員',u'贊助會員',u'顧問')
        self._cr.execute(sql) # 新增 4 筆資料, 花費 0.012 秒
        sql = " INSERT INTO normal_p_people_type_rel(normal_p_id, people_type_id) SELECT id, 2 FROM normal_p a WHERE member_type = 1 "
        self._cr.execute(sql)  # 新增 704 筆資料, 花費 0.261 秒
        sql = " INSERT INTO normal_p_people_type_rel(normal_p_id, people_type_id) SELECT id, 3 FROM normal_p a WHERE member_type = 2 "
        self._cr.execute(sql)  # 新增6609筆資料, 花費0.381秒
        sql = " INSERT INTO normal_p_people_type_rel(normal_p_id, people_type_id) SELECT id, 4 FROM normal_p a WHERE consultant_id IS NOT NULL "
        self._cr.execute(sql)  # 新增199筆資料, 花費 0.221秒
        return True

    def set_donate_id(self): # 約 3 分鐘
        y = 2018 # 轉檔太久了! 所以從2018年3月份開始
        m = 4
        now_month = int(datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').month)
        end_while = True
        while y<=2018:
            if y == 2018 and m == 4:
                end_while = False
            while m<=4:
                if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
                    d2 = 31
                elif m == 2:
                    d2 = 28
                else:
                    d2 = 30
                count_datas_number = 0
                count_datas_receipt_number = 0
                sql = " SELECT COUNT(*) FROM donate_order WHERE donate_date BETWEEN '%s-%s-%s' AND '%s-%s-%s' AND donate_date IS NOT NULL" % (y, m, 1, y, m, d2)
                self._cr.execute(sql)
                for count in self._cr.dictfetchall():  # 依照捐款日期計算的捐款人數
                    count_datas_number = count['count']

                sql = " SELECT donate_w_id, donate_w_id_number FROM donate_order WHERE donate_date BETWEEN '%s-%s-%s' AND '%s-%s-%s' AND donate_date IS NOT NULL GROUP BY donate_w_id, donate_w_id_number" % (y, m, 1, y, m, d2)
                self._cr.execute(sql)
                number_of_people = len(self._cr.dictfetchall()) # 依照捐款日期計算的捐款人數, 但是濾掉重複捐款的人

                code = 'A' + str(y)[2:] + str(m).zfill(2) + '%' # 迴圈跑年份及月份
                sql = " SELECT donate_id FROM donate_single WHERE donate_id LIKE '%s' ORDER BY donate_id desc limit 1" % (code)
                self._cr.execute(sql) # 取出舊資料該年該月份捐款編號的末5碼最大值
                for count in self._cr.dictfetchall():
                    count_datas_receipt_number = int(count['donate_id'][5:])

                sql = " SELECT DISTINCT ON (donate_member_w_id) * FROM donate_single WHERE donate_date BETWEEN '%s-%s-%s' AND '%s-%s-%s' AND donate_date IS NOT NULL" % (y, m, 1, y, m, d2)
                self._cr.execute(sql)
                count_datas_households_number = len(self._cr.dictfetchall()) #依照捐款日期去計算已開出的收據張數並濾掉重複捐款團員編號, 確認該年該月份的捐款戶數

                if count_datas_number != 0 or count_datas_receipt_number != 0:
                    sql = " INSERT INTO donate_statistics(year, month, number, number_of_people, receipt_number, households) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (y, m, count_datas_number, number_of_people, int(count_datas_receipt_number), count_datas_households_number)
                    self._cr.execute(sql)
                m = m + 1
            m = 1
            y = y + 1
        return True

    # def set_postal_code1(self):  # 花費時間約18分鐘
    #     lines = self.env['normal.p'].search([])
    #     s = collections.Counter()
    #     zip = ''
    #     for line in lines[0:420000]:
    #         zip = ''
    #         flag = True
    #         if line.rec_addr is False and line.con_addr:  # 收據地址為空, 但卻有報表寄送地址
    #             zip = zipcodetw.find(line.con_addr)[0:3]  # 藉由報表寄送地址判讀該地址的郵遞區號, 並只取郵遞區號前3碼
    #             line.zip = zip  # 將郵遞區號寫入 收據地址的郵遞區號
    #             line.rec_addr = line.con_addr  # 將報表寄送地址寫入收據地址, 前提是收據地址是空的
    #         elif line.rec_addr:  # 有收據地址
    #             zip = zipcodetw.find(line.rec_addr)[0:3]  # 直接取郵遞區號前3碼
    #
    #         if (len(zip) < 3 or zip =='')and line.rec_addr:  # 藉由程式判讀出來的郵遞區號, 若小於3碼則代表地址填寫錯誤, 找不到郵遞區號, 條件是收據地址不為空
    #             if len(line.zip) < 3:
    #                 s['999'] += 1  # 該郵遞區號出現次數 +1
    #                 line.new_coding = '999' + str(s.get('999')).zfill(5)  # 什麼都沒有的一般捐款者
    #             elif len(line.zip) >= 3 and (u'\u0030' <= line.zip[0] <= u'\u0039'):
    #                 for ch in line.zip[0:3]:
    #                     if int(line.zip[0]) == 0:
    #                         flag = False
    #                     if not u'\u0030' <= ch <=u'\u0039':
    #                         flag = False
    #                 if flag:
    #                     zip = line.zip[0:3]
    #                     s[zip] += 1  # 該郵遞區號的出現次數 +1
    #                     line.new_coding = zip + str(s.get(zip)).zfill(5)
    #         elif len(zip) == 3:  # 郵遞區號有3碼, 代表該筆資料的地址可以找到相對應的郵遞區號
    #             line.zip = zip  # 將程式判斷的郵遞區號寫入該捐款者的收據地址郵遞區號
    #             s[zip] += 1  # 該郵遞區號的出現次數 +1
    #             line.new_coding = zip + str(s.get(zip)).zfill(5)
    #
    #     postal_code_list = list(s.items())  # 將python 的 counter 轉換為陣列
    #     for i in range(len(postal_code_list)):
    #         sql = " INSERT INTO auto_donateid(zip, area_number) VALUES ('%s', '%s')" % (postal_code_list[i][0], postal_code_list[i][1])
    #         self._cr.execute(sql)  # 將counter內的計數寫入資料庫之中
    #     s.clear()
    #     return True
    #
    # def set_postal_code2(self):  # 花費時間約18分鐘
    #     lines = self.env['normal.p'].search([])
    #     last_time_data = self.env['auto.donateid'].search([])
    #     s = collections.Counter()
    #     zip = ''
    #     for row in last_time_data:  # 將資料庫計數器的資料撈出來, 放入python 的 counter之中, 以便繼續統計個郵遞區號的出現次數
    #         zip = row.zip
    #         s[zip] = int(row.area_number)
    #     zip = ''
    #
    #     for line in lines[420000:]:
    #         zip = ''
    #         flag = True
    #         if line.rec_addr is False and line.con_addr:  # 收據地址為空, 但卻有報表寄送地址
    #             zip = zipcodetw.find(line.con_addr)[0:3]  # 藉由報表寄送地址判讀該地址的郵遞區號, 並只取郵遞區號前3碼
    #             line.zip = zip  # 將郵遞區號寫入 收據地址的郵遞區號
    #             line.rec_addr = line.con_addr  # 將報表寄送地址寫入收據地址, 前提是收據地址是空的
    #         elif line.rec_addr:  # 有收據地址
    #             zip = zipcodetw.find(line.rec_addr)[0:3]  # 直接取郵遞區號前3碼
    #
    #         if (len(zip) < 3 or zip == '') and line.rec_addr:  # 藉由程式判讀出來的郵遞區號, 若小於3碼則代表地址填寫錯誤, 找不到郵遞區號, 條件是收據地址不為空
    #             if len(line.zip) < 3:
    #                 s['999'] += 1  # 該郵遞區號出現次數 +1
    #                 line.new_coding = '999' + str(s.get('999')).zfill(5)  # 什麼都沒有的一般捐款者
    #             elif len(line.zip) >= 3 and (u'\u0030' <= line.zip[0] <= u'\u0039'):
    #                 for ch in line.zip[0:3]:
    #                     if int(line.zip[0]) == 0:
    #                         flag = False
    #                     if not u'\u0030' <= ch <= u'\u0039':
    #                         flag = False
    #                 if flag:
    #                     zip = line.zip[0:3]
    #                     s[zip] += 1  # 該郵遞區號的出現次數 +1
    #                     line.new_coding = zip + str(s.get(zip)).zfill(5)
    #         elif len(zip) == 3:  # 郵遞區號有3碼, 代表該筆資料的地址可以找到相對應的郵遞區號
    #             line.zip = zip  # 將程式判斷的郵遞區號寫入該捐款者的收據地址郵遞區號
    #             s[zip] += 1  # 該郵遞區號的出現次數 +1
    #             line.new_coding = zip + str(s.get(zip)).zfill(5)
    #
    #     postal_code_list = list(s.items())
    #     for i in range(len(postal_code_list)):
    #         postal_code_data = self.env['auto.donateid'].search([('zip', '=', postal_code_list[i][0])])  # 搜尋資料庫的計數器是否具有該郵遞區號
    #         if postal_code_data:
    #             postal_code_data.area_number = postal_code_data.area_number + int(postal_code_list[i][1])  # 有搜尋到 則更新資料庫計數器的數量
    #         else:
    #             sql = " INSERT INTO auto_donateid(zip, area_number) VALUES ('%s', '%s')" % (postal_code_list[i][0], postal_code_list[i][1])  # 沒有搜尋到則重新建立該郵遞區號的資料
    #             self._cr.execute(sql)
    #     s.clear()
    #     return True
    #
    # def set_postal_code3(self):  # 沒有收據寄送地址, 也沒有報表寄送地址
    #     lines = self.env['normal.p'].search([('new_coding', '=', '')])
    #     last_time_data = self.env['auto.donateid'].search([])
    #     s = collections.Counter()
    #     zip = ''
    #     for row in last_time_data:  # 將資料庫計數器的資料撈出來, 放入python 的 counter之中, 以便繼續統計個郵遞區號的出現次數
    #         zip = row.zip
    #         s[zip] = int(row.area_number)
    #
    #     for line in lines:
    #         flag = True
    #         zip = ''
    #         if line.zip == False:
    #             s['999'] += 1
    #             line.new_coding = '999' + str(s.get('999')).zfill(5)
    #         elif len(line.zip) >= 3 and (u'\u0030' <= line.zip[0] <= u'\u0039'):
    #             for ch in line.zip[0:3]:
    #                 if int(line.zip[0]) == 0:
    #                     flag = False
    #                 if not u'\u0030' <= ch <= u'\u0039':
    #                     flag = False
    #             if flag:
    #                 zip = line.zip[0:3]
    #                 s[zip] += 1  # 該郵遞區號的出現次數 +1
    #                 line.new_coding = zip + str(s.get(zip)).zfill(5)
    #             else:
    #                 s['999'] += 1
    #                 line.new_coding = '999' + str(s.get('999')).zfill(5)
    #         else:
    #             s['999'] += 1
    #             line.new_coding = '999' + str(s.get('999')).zfill(5)
    #
    #     postal_code_list = list(s.items())
    #     for i in range(len(postal_code_list)):
    #         postal_code_data = self.env['auto.donateid'].search([('zip', '=', postal_code_list[i][0])])  # 搜尋資料庫的計數器是否具有該郵遞區號
    #         if postal_code_data:
    #             postal_code_data.area_number = postal_code_data.area_number + int(postal_code_list[i][1])  # 有搜尋到 則更新資料庫計數器的數量
    #         else:
    #             sql = " INSERT INTO auto_donateid(zip, area_number) VALUES ('%s', '%s')" % (postal_code_list[i][0], postal_code_list[i][1])  # 沒有搜尋到則重新建立該郵遞區號的資料
    #             self._cr.execute(sql)
    #     s.clear()
    #     return True

    def postal_code_normal_p(self):
        sql = "UPDATE normal_p SET postal_code_id = a.id FROM postal_code a WHERE SUBSTRING(a.zip, 1, 3)  = normal_p.zip_code"
        self._cr.execute(sql) # 共231688筆資料, 花費8.547秒
        return True
    # 全部轉檔程式費時358.4分鐘, 約 6 小時

    def bridge_transfer(self):
        sql = "INSERT INTO bridge_data(bridge_code,name,length,width,height,bridge_addr,donate_date_start,donate_date_end,build_date,completed_date,db_change_date,temp_key_in_user)"\
              " SELECT 橋樑編號,橋樑名稱,長度,寬度,高度,橋樑地址,case when 募捐起日='' then NULL else cast(募捐起日 as date) end as 募捐起日,case when 募捐迄日='' then NULL else cast(募捐迄日 as date) end as 募捐迄日,case when 建造日期='' then NULL else cast(建造日期 as date) end as 建造日期,case when 完工日期='' then NULL else cast(完工日期 as date) end as 完工日期,case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期,輸入人員 FROM 橋樑檔"
        self._cr.execute(sql)
        sql = "UPDATE bridge_data SET key_in_user = res_users.id FROM res_users WHERE bridge_data.temp_key_in_user = res_users.w_id"
        self._cr.execute(sql)
        return True

    def move_donate_data(self): # 把捐款資料轉移至舊案查詢系統的資料表
        basic_setting = self.env['ir.config_parameter'].search([])
        year =''
        for line in basic_setting:
            if line.key == 'move_data_year':
                line.value = self.move_data_year
                year = str(int(line.value) + 1911) + '-12-31'

        sql = "INSERT INTO old_donate_single (id, bridge, create_date, write_date, payment_method, noassign, write_uid, old_donate_total, report_donate, donate_member, temp_work_id, key_in_user, noassign_money, donate_id, ps, self_iden, current_donate_project, donate_date, state, print_date, paid_id, print_user, print_count, report_price_big, current_donate_total, create_uid, con_addr, last_donate_type, cashier_name, set_today, year_receipt_send, temp_key_in_user, last_donate_date, coffin_money, cellphone, clear_all_is_merge, clear_all_is_donate, current_donate_people, name, receipt_send, con_phone, road_money, poor_help, poor_help_money, road, bridge_money, year_fee, report_send, zip_code, sreceipt_number, coffin, work_id, print_all_donor_list, rec_addr, zip, donor_show, active, donate_total, donate_member_w_id, donate_member_number)"\
              " SELECT id, bridge, create_date, write_date, payment_method, noassign, write_uid, old_donate_total, report_donate, donate_member, temp_work_id, key_in_user, noassign_money, donate_id, ps, self_iden, current_donate_project, donate_date, state, print_date, paid_id, print_user, print_count, report_price_big, current_donate_total, create_uid, con_addr, last_donate_type, cashier_name, set_today, year_receipt_send, temp_key_in_user, last_donate_date, coffin_money, cellphone, clear_all_is_merge, clear_all_is_donate, current_donate_people, name, receipt_send, con_phone, road_money, poor_help, poor_help_money, road, bridge_money, year_fee, report_send, zip_code, sreceipt_number, coffin, work_id, print_all_donor_list, rec_addr, zip, donor_show, active, donate_total, donate_member_w_id, donate_member_number FROM donate_single WHERE donate_date BETWEEN '1911-01-01' AND '%s'" % (year)
        self._cr.execute(sql) # 搬移 donate_single 1年份的資料至old_donate_single, ex: 2014年 共285374筆, 花費32.222秒
        sql = "ALTER TABLE donate_single DISABLE TRIGGER ALL"
        self._cr.execute(sql)  # 解除 donate_single 所有的觸發器, 不然會超級慢, 刪資料會刪到天荒地老
        sql = "DELETE FROM donate_single WHERE donate_date BETWEEN '1911-01-01' AND '%s'" % (year)
        self._cr.execute(sql)  # 刪除 donate_single 1年份的資料 ex: 2014年 共285374筆, 花費24.627秒
        sql = "ALTER TABLE donate_single ENABLE TRIGGER ALL"
        self._cr.execute(sql)  # 啟動 donate_single 所有的觸發器, 很重要!
        sql = "INSERT INTO old_donate_order (id, bridge, use_amount, sequence, create_date, write_date, payment_method,others,p_type,db_key_in_user, key_in_user, donate_id, ps, report_price, report_big,donate_date, used_money, state, donate_member, mail, donate, paid_id, create_uid, donate_list_id, city, others_money, clerk, cashier, year_receipt_send, credit_card, available_balance, donate_w_id, donate_w_id_number, address, donate_type, donate_total, bank, temp_key_in_user, self_id, report_year, donate_book_code, cash, receipt_send, con_phone, road_money, poor_help_money, poor_help, bridge_money, report_send, db_chang_date, coffin, road, active)"\
              "SELECT id, bridge, use_amount, sequence, create_date, write_date, payment_method,others,p_type,db_key_in_user, key_in_user, donate_id, ps, report_price, report_big,donate_date, used_money, state, donate_member, mail, donate, paid_id, create_uid, donate_list_id, city, others_money, clerk, cashier, year_receipt_send, credit_card, available_balance, donate_w_id, donate_w_id_number, address, donate_type, donate_total, bank, temp_key_in_user, self_id, report_year, donate_book_code, cash, receipt_send, con_phone, road_money, poor_help_money, poor_help, bridge_money, report_send, db_chang_date, coffin, road, active FROM donate_order WHERE NOT EXISTS (SELECT id FROM donate_single WHERE donate_single.id = donate_order.donate_list_id)"
        self._cr.execute(sql) # 搬移 donate_order 1年份的資料至old_donate_order ex: 2014年 共749661筆, 花費115.025秒
        sql = "ALTER TABLE donate_order DISABLE TRIGGER ALL"
        self._cr.execute(sql)  # 解除 donate_order 所有的觸發器, 不然會很慢
        sql = "DELETE FROM donate_order WHERE NOT EXISTS (SELECT id FROM donate_single WHERE donate_single.id = donate_order.donate_list_id)"
        self._cr.execute(sql) # 刪除 donate_order 1年份的資料  ex: 2014年 共749661筆, 花費85.06秒
        sql = "ALTER TABLE donate_order ENABLE TRIGGER ALL"
        self._cr.execute(sql) # 啟動 donate_order 所有的觸發器, 很重要!
        sql = "INSERT INTO old_donate_family_line (id, create_uid, create_date, write_uid, parent_id, donate_member, poor_help_money, bridge_money, write_date, coffin_money, noassign_money, road_money) SELECT id, create_uid, create_date, write_uid, parent_id, donate_member, poor_help_money, bridge_money, write_date, coffin_money, noassign_money, road_money FROM donate_family_line WHERE NOT EXISTS (SELECT id FROM donate_single WHERE donate_single.id = donate_family_line.parent_id)"
        self._cr.execute(sql)  # 搬移old_donate_family_line的資料 ex: 2014年 共749403筆, 花費52.338秒
        sql = "ALTER TABLE donate_family_line DISABLE TRIGGER ALL"
        self._cr.execute(sql)  # 解除 donate_family_line 所有的觸發器
        sql = "DELETE FROM donate_family_line WHERE NOT EXISTS (SELECT id FROM donate_single WHERE donate_single.id = donate_family_line.parent_id)"
        self._cr.execute(sql)  # 刪除 donate_family_line 1年份的資料  ex: 2014年 共749403筆, 花費48.521秒
        sql = "ALTER TABLE donate_family_line ENABLE TRIGGER ALL"
        self._cr.execute(sql) # 啟動donate_family_line 所有的觸發器
        sql = " Vacuum donate_single"
        self._cr.execute(sql) # 刪除資料後, 資料庫不一定會刪得很乾淨, 要用 Vacuum 重新清理一次資料表
        sql = " Vacuum donate_order"
        self._cr.execute(sql) # 刪除資料後, 資料庫不一定會刪得很乾淨, 要用 Vacuum 重新清理一次資料表
        return True

    def reset_newcoding(self):
        sql = "UPDATE normal_p SET temp_new_coding = a.new_coding FROM normal_p a WHERE a.new_coding = normal_p.new_coding"
        self._cr.execute(sql)
        postal_code_collection = self.env['postal.code'].search([])

        for line in postal_code_collection:
            sql = "update normal_p a "\
                  " set new_coding = b.rownubmer "\
                  " from (select id, "\
                  " SUBSTRING(cast(zip as text),1,3) || LPAD(CAST(ROW_NUMBER () OVER (ORDER BY build_date,db_chang_date) AS text), 5, '0') as rownubmer "\
                  " from normal_p "\
                  " where zip like '%s' "\
                  " ) b "\
                  "where a.id = b.id and a.zip like '%s' " % (line.zip + '%', line.zip + '%')
            self._cr.execute(sql)
            sql = "select count(*) from normal_p where zip LIKE '%s' " % (line.zip + '%')
            self._cr.execute(sql)
            number = self._cr.dictfetchall()

            for row in number:
                sql = "UPDATE auto_donateid SET area_number =  '%s' WHERE zip = '%s'" % (int(row['count']), line.zip)
                self._cr.execute(sql)

    def postal_code_database(self):
        sql = " INSERT INTO postal_code (city, area, zip) VALUES " \
                "('台北市', '中正區', '100')," \
                "('台北市', '大同區', '103')," \
                "('台北市', '中山區', '104')," \
                "('台北市', '松山區', '105')," \
                "('台北市', '大安區', '106')," \
                "('台北市', '萬華區', '108')," \
                "('台北市', '信義區', '110')," \
                "('台北市', '士林區', '111')," \
                "('台北市', '北投區', '112')," \
                "('台北市', '內湖區', '114')," \
                "('台北市', '南港區', '115')," \
                "('台北市', '文山區', '116')," \
                "('基隆市', '仁愛區', '200')," \
                "('基隆市', '信義區', '201')," \
                "('基隆市', '中正區', '202')," \
                "('基隆市', '中山區', '203')," \
                "('基隆市', '安樂區', '204')," \
                "('基隆市', '暖暖區', '205')," \
                "('基隆市', '七堵區', '206')," \
                "('新北市', '萬里區', '207')," \
                "('新北市', '金山區', '208')," \
                "('新北市', '板橋區', '220')," \
                "('新北市', '汐止區', '221')," \
                "('新北市', '深坑區', '222')," \
                "('新北市', '石碇區', '223')," \
                "('新北市', '瑞芳區', '224')," \
                "('新北市', '平溪區', '226')," \
                "('新北市', '雙溪區', '227')," \
                "('新北市', '貢寮區', '228')," \
                "('新北市', '新店區', '231')," \
                "('新北市', '坪林區', '232')," \
                "('新北市', '烏來區', '233')," \
                "('新北市', '永和區', '234')," \
                "('新北市', '中和區', '235')," \
                "('新北市', '土城區', '236')," \
                "('新北市', '三峽區', '237')," \
                "('新北市', '樹林區', '238')," \
                "('新北市', '鶯歌區', '239')," \
                "('新北市', '三重區', '241')," \
                "('新北市', '新莊區', '242')," \
                "('新北市', '泰山區', '243')," \
                "('新北市', '林口區', '244')," \
                "('新北市', '蘆洲區', '247')," \
                "('新北市', '五股區', '248')," \
                "('新北市', '八里區', '249')," \
                "('新北市', '淡水區', '251')," \
                "('新北市', '三芝區', '252')," \
                "('新北市', '石門區', '253')," \
                "('宜蘭縣', '宜蘭市', '260')," \
                "('宜蘭縣', '頭城鎮', '261')," \
                "('宜蘭縣', '礁溪鄉', '262')," \
                "('宜蘭縣', '壯圍鄉', '263')," \
                "('宜蘭縣', '員山鄉', '264')," \
                "('宜蘭縣', '羅東鎮', '265')," \
                "('宜蘭縣', '三星鄉', '266')," \
                "('宜蘭縣', '大同鄉', '267')," \
                "('宜蘭縣', '五結鄉', '268')," \
                "('宜蘭縣', '冬山鄉', '269')," \
                "('宜蘭縣', '蘇澳鎮', '270')," \
                "('宜蘭縣', '南澳鄉', '272')," \
                "('宜蘭縣', '釣魚台列嶼', '290')," \
                "('新竹市', '', '300')," \
                "('新竹縣', '竹北市', '302')," \
                "('新竹縣', '湖口鄉', '303')," \
                "('新竹縣', '新豐鄉', '304')," \
                "('新竹縣', '新埔鎮', '305')," \
                "('新竹縣', '關西鎮', '306')," \
                "('新竹縣', '芎林鄉', '307')," \
                "('新竹縣', '寶山鄉', '308')," \
                "('新竹縣', '竹東鎮', '310')," \
                "('新竹縣', '五峰鄉', '311')," \
                "('新竹縣', '橫山鄉', '312')," \
                "('新竹縣', '尖石鄉', '313')," \
                "('新竹縣', '北埔鄉', '314')," \
                "('新竹縣', '峨眉鄉', '315')," \
                "('桃園縣', '中壢市', '320')," \
                "('桃園縣', '平鎮市', '324')," \
                "('桃園縣', '龍潭鄉', '325')," \
                "('桃園縣', '楊梅市', '326')," \
                "('桃園縣', '新屋鄉', '327')," \
                "('桃園縣', '觀音鄉', '328')," \
                "('桃園縣', '桃園市', '330')," \
                "('桃園縣', '龜山鄉', '333')," \
                "('桃園縣', '八德市', '334')," \
                "('桃園縣', '大溪鎮', '335')," \
                "('桃園縣', '復興鄉', '336')," \
                "('桃園縣', '大園鄉', '337')," \
                "('桃園縣', '蘆竹鄉', '338')," \
                "('苗栗縣', '竹南鎮', '350')," \
                "('苗栗縣', '頭份鎮', '351')," \
                "('苗栗縣', '三灣鄉', '352')," \
                "('苗栗縣', '南庄鄉', '353')," \
                "('苗栗縣', '獅潭鄉', '354')," \
                "('苗栗縣', '後龍鎮', '356')," \
                "('苗栗縣', '通霄鎮', '357')," \
                "('苗栗縣', '苑裡鎮', '358')," \
                "('苗栗縣', '苗栗市', '360')," \
                "('苗栗縣', '造橋鄉', '361')," \
                "('苗栗縣', '頭屋鄉', '362')," \
                "('苗栗縣', '公館鄉', '363')," \
                "('苗栗縣', '大湖鄉', '364')," \
                "('苗栗縣', '泰安鄉', '365')," \
                "('苗栗縣', '銅鑼鄉', '366')," \
                "('苗栗縣', '三義鄉', '367')," \
                "('苗栗縣', '西湖鄉', '368')," \
                "('苗栗縣', '卓蘭鎮', '369')," \
                "('台中市', '中區', '400')," \
                "('台中市', '東區', '401')," \
                "('台中市', '南區', '402')," \
                "('台中市', '西區', '403')," \
                "('台中市', '北區', '404')," \
                "('台中市', '北屯區', '406')," \
                "('台中市', '西屯區', '407')," \
                "('台中市', '南屯區', '408')," \
                "('台中市', '太平區', '411')," \
                "('台中市', '大里區', '412')," \
                "('台中市', '霧峰區', '413')," \
                "('台中市', '烏日區', '414')," \
                "('台中市', '豐原區', '420')," \
                "('台中市', '后里區', '421')," \
                "('台中市', '石岡區', '422')," \
                "('台中市', '東勢區', '423')," \
                "('台中市', '和平區', '424')," \
                "('台中市', '新社區', '426')," \
                "('台中市', '潭子區', '427')," \
                "('台中市', '大雅區', '428')," \
                "('台中市', '神岡區', '429')," \
                "('台中市', '大肚區', '432')," \
                "('台中市', '沙鹿區', '433')," \
                "('台中市', '龍井區', '434')," \
                "('台中市', '梧棲區', '435')," \
                "('台中市', '清水區', '436')," \
                "('台中市', '大甲區', '437')," \
                "('台中市', '外埔區', '438')," \
                "('台中市', '大安區', '439')," \
                "('彰化縣', '彰化市', '500')," \
                "('彰化縣', '芬園鄉', '502')," \
                "('彰化縣', '花壇鄉', '503')," \
                "('彰化縣', '秀水鄉', '504')," \
                "('彰化縣', '鹿港鎮', '505')," \
                "('彰化縣', '福興鄉', '506')," \
                "('彰化縣', '線西鄉', '507')," \
                "('彰化縣', '和美鎮', '508')," \
                "('彰化縣', '伸港鄉', '509')," \
                "('彰化縣', '員林鎮', '510')," \
                "('彰化縣', '社頭鄉', '511')," \
                "('彰化縣', '永靖鄉', '512')," \
                "('彰化縣', '埔心鄉', '513')," \
                "('彰化縣', '溪湖鎮', '514')," \
                "('彰化縣', '大村鄉', '515')," \
                "('彰化縣', '埔鹽鄉', '516')," \
                "('彰化縣', '田中鎮', '520')," \
                "('彰化縣', '北斗鎮', '521')," \
                "('彰化縣', '田尾鄉', '522')," \
                "('彰化縣', '埤頭鄉', '523')," \
                "('彰化縣', '溪州鄉', '524')," \
                "('彰化縣', '竹塘鄉', '525')," \
                "('彰化縣', '二林鎮', '526')," \
                "('彰化縣', '大城鄉', '527')," \
                "('彰化縣', '芳苑鄉', '528')," \
                "('彰化縣', '二水鄉', '530')," \
                "('南投縣', '南投市', '540')," \
                "('南投縣', '中寮鄉', '541')," \
                "('南投縣', '草屯鎮', '542')," \
                "('南投縣', '國姓鄉', '544')," \
                "('南投縣', '埔里鎮', '545')," \
                "('南投縣', '仁愛鄉', '546')," \
                "('南投縣', '名間鄉', '551')," \
                "('南投縣', '集集鎮', '552')," \
                "('南投縣', '水里鄉', '553')," \
                "('南投縣', '魚池鄉', '555')," \
                "('南投縣', '信義鄉', '556')," \
                "('南投縣', '竹山鎮', '557')," \
                "('南投縣', '鹿谷鄉', '558')," \
                "('雲林縣', '斗南鎮', '630')," \
                "('雲林縣', '大埤鄉', '631')," \
                "('雲林縣', '虎尾鎮', '632')," \
                "('雲林縣', '土庫鎮', '633')," \
                "('雲林縣', '褒忠鄉', '634')," \
                "('雲林縣', '東勢鄉', '635')," \
                "('雲林縣', '臺西鄉', '636')," \
                "('雲林縣', '崙背鄉', '637')," \
                "('雲林縣', '麥寮鄉', '638')," \
                "('雲林縣', '斗六市', '640')," \
                "('雲林縣', '林內鄉', '643')," \
                "('雲林縣', '古坑鄉', '646')," \
                "('雲林縣', '莿桐鄉', '647')," \
                "('雲林縣', '西螺鎮', '648')," \
                "('雲林縣', '二崙鄉', '649')," \
                "('雲林縣', '北港鎮', '651')," \
                "('雲林縣', '水林鄉', '652')," \
                "('雲林縣', '口湖鄉', '653')," \
                "('雲林縣', '四湖鄉', '654')," \
                "('雲林縣', '元長鄉', '655')," \
                "('嘉義市', '', '600')," \
                "('嘉義縣', '番路鄉', '602')," \
                "('嘉義縣', '梅山鄉', '603')," \
                "('嘉義縣', '竹崎鄉', '604')," \
                "('嘉義縣', '阿里山鄉', '605')," \
                "('嘉義縣', '中埔鄉', '606')," \
                "('嘉義縣', '大埔鄉', '607')," \
                "('嘉義縣', '水上鄉', '608')," \
                "('嘉義縣', '鹿草鄉', '611')," \
                "('嘉義縣', '太保市', '612')," \
                "('嘉義縣', '朴子市', '613')," \
                "('嘉義縣', '東石鄉', '614')," \
                "('嘉義縣', '六腳鄉', '615')," \
                "('嘉義縣', '新港鄉', '616')," \
                "('嘉義縣', '民雄鄉', '621')," \
                "('嘉義縣', '大林鎮', '622')," \
                "('嘉義縣', '溪口鄉', '623')," \
                "('嘉義縣', '義竹鄉', '624')," \
                "('嘉義縣', '布袋鎮', '625')," \
                "('台南市', '中西區', '700')," \
                "('台南市', '東區', '701')," \
                "('台南市', '南區', '702')," \
                "('台南市', '北區', '704')," \
                "('台南市', '安平區', '708')," \
                "('台南市', '安南區', '709')," \
                "('台南市', '永康區', '710')," \
                "('台南市', '歸仁區', '711')," \
                "('台南市', '新化區', '712')," \
                "('台南市', '左鎮區', '713')," \
                "('台南市', '玉井區', '714')," \
                "('台南市', '楠西區', '715')," \
                "('台南市', '南化區', '716')," \
                "('台南市', '仁德區', '717')," \
                "('台南市', '關廟區', '718')," \
                "('台南市', '龍崎區', '719')," \
                "('台南市', '官田區', '720')," \
                "('台南市', '麻豆區', '721')," \
                "('台南市', '佳里區', '722')," \
                "('台南市', '西港區', '723')," \
                "('台南市', '七股區', '724')," \
                "('台南市', '將軍區', '725')," \
                "('台南市', '學甲區', '726')," \
                "('台南市', '北門區', '727')," \
                "('台南市', '新營區', '730')," \
                "('台南市', '後壁區', '731')," \
                "('台南市', '白河區', '732')," \
                "('台南市', '東山區', '733')," \
                "('台南市', '六甲區', '734')," \
                "('台南市', '下營區', '735')," \
                "('台南市', '柳營區', '736')," \
                "('台南市', '鹽水區', '737')," \
                "('台南市', '善化區', '741')," \
                "('台南市', '大內區', '742')," \
                "('台南市', '山上區', '743')," \
                "('台南市', '新市區', '744')," \
                "('台南市', '安定區', '745')," \
                "('高雄市', '新興區', '800')," \
                "('高雄市', '前金區', '801')," \
                "('高雄市', '苓雅區', '802')," \
                "('高雄市', '鹽埕區', '803')," \
                "('高雄市', '鼓山區', '804')," \
                "('高雄市', '旗津區', '805')," \
                "('高雄市', '前鎮區', '806')," \
                "('高雄市', '三民區', '807')," \
                "('高雄市', '楠梓區', '811')," \
                "('高雄市', '小港區', '812')," \
                "('高雄市', '左營區', '813')," \
                "('高雄市', '仁武區', '814')," \
                "('高雄市', '大社區', '815')," \
                "('高雄市', '岡山區', '820')," \
                "('高雄市', '路竹區', '821')," \
                "('高雄市', '阿蓮區', '822')," \
                "('高雄市', '田寮區', '823')," \
                "('高雄市', '燕巢區', '824')," \
                "('高雄市', '橋頭區', '825')," \
                "('高雄市', '梓官區', '826')," \
                "('高雄市', '彌陀區', '827')," \
                "('高雄市', '永安區', '828')," \
                "('高雄市', '湖內區', '829')," \
                "('高雄市', '鳳山區', '830')," \
                "('高雄市', '大寮區', '831')," \
                "('高雄市', '林園區', '832')," \
                "('高雄市', '鳥松區', '833')," \
                "('高雄市', '大樹區', '840')," \
                "('高雄市', '旗山區', '842')," \
                "('高雄市', '美濃區', '843')," \
                "('高雄市', '六龜區', '844')," \
                "('高雄市', '內門區', '845')," \
                "('高雄市', '杉林區', '846')," \
                "('高雄市', '甲仙區', '847')," \
                "('高雄市', '桃源區', '848')," \
                "('高雄市', '那瑪夏區', '849')," \
                "('高雄市', '茂林區', '851')," \
                "('高雄市', '茄萣區', '852')," \
                "('南海諸島', '東沙', '817')," \
                "('南海諸島', '南沙', '819')," \
                "('澎湖縣', '馬公市', '880')," \
                "('澎湖縣', '西嶼鄉', '881')," \
                "('澎湖縣', '望安鄉', '882')," \
                "('澎湖縣', '七美鄉', '883')," \
                "('澎湖縣', '白沙鄉', '884')," \
                "('澎湖縣', '湖西鄉', '885')," \
                "('屏東縣', '屏東市', '900')," \
                "('屏東縣', '三地門鄉', '901')," \
                "('屏東縣', '霧臺鄉', '902')," \
                "('屏東縣', '瑪家鄉', '903')," \
                "('屏東縣', '九如鄉', '904')," \
                "('屏東縣', '里港鄉', '905')," \
                "('屏東縣', '高樹鄉', '906')," \
                "('屏東縣', '鹽埔鄉', '907')," \
                "('屏東縣', '長治鄉', '908')," \
                "('屏東縣', '麟洛鄉', '909')," \
                "('屏東縣', '竹田鄉', '911')," \
                "('屏東縣', '內埔鄉', '912')," \
                "('屏東縣', '萬丹鄉', '913')," \
                "('屏東縣', '潮州鎮', '920')," \
                "('屏東縣', '泰武鄉', '921')," \
                "('屏東縣', '來義鄉', '922')," \
                "('屏東縣', '萬巒鄉', '923')," \
                "('屏東縣', '崁頂鄉', '924')," \
                "('屏東縣', '新埤鄉', '925')," \
                "('屏東縣', '南州鄉', '926')," \
                "('屏東縣', '林邊鄉', '927')," \
                "('屏東縣', '東港鄉', '928')," \
                "('屏東縣', '琉球鄉', '929')," \
                "('屏東縣', '佳冬鄉', '931')," \
                "('屏東縣', '新園鄉', '932')," \
                "('屏東縣', '枋寮鄉', '940')," \
                "('屏東縣', '枋山鄉', '941')," \
                "('屏東縣', '春日鄉', '942')," \
                "('屏東縣', '獅子鄉', '943')," \
                "('屏東縣', '車城鄉', '944')," \
                "('屏東縣', '牡丹鄉', '945')," \
                "('屏東縣', '恆春鄉', '946')," \
                "('屏東縣', '滿州鄉', '947')," \
                "('台東縣', '臺東市', '950')," \
                "('台東縣', '綠島鄉', '951')," \
                "('台東縣', '蘭嶼鄉', '952')," \
                "('台東縣', '延平鄉', '953')," \
                "('台東縣', '卑南鄉', '954')," \
                "('台東縣', '鹿野鄉', '955')," \
                "('台東縣', '關山鎮', '956')," \
                "('台東縣', '海端鄉', '957')," \
                "('台東縣', '池上鄉', '958')," \
                "('台東縣', '東河鄉', '959')," \
                "('台東縣', '成功鎮', '961')," \
                "('台東縣', '長濱鄉', '962')," \
                "('台東縣', '太麻里鄉', '963')," \
                "('台東縣', '金峰鄉', '964')," \
                "('台東縣', '大武鄉', '965')," \
                "('台東縣', '達仁鄉', '966')," \
                "('花蓮縣', '花蓮市', '970')," \
                "('花蓮縣', '新城鄉', '971')," \
                "('花蓮縣', '秀林鄉', '972')," \
                "('花蓮縣', '吉安鄉', '973')," \
                "('花蓮縣', '壽豐鄉', '974')," \
                "('花蓮縣', '鳳林鎮', '975')," \
                "('花蓮縣', '光復鄉', '976')," \
                "('花蓮縣', '豐濱鄉', '977')," \
                "('花蓮縣', '瑞穗鄉', '978')," \
                "('花蓮縣', '萬榮鄉', '979')," \
                "('花蓮縣', '玉里鎮', '981')," \
                "('花蓮縣', '卓溪鄉', '982')," \
                "('花蓮縣', '富里鄉', '983')," \
                "('金門縣', '金沙鎮', '890')," \
                "('金門縣', '金湖鎮', '891')," \
                "('金門縣', '金寧鄉', '892')," \
                "('金門縣', '金城鎮', '893')," \
                "('金門縣', '烈嶼鄉', '894')," \
                "('金門縣', '烏坵鄉', '896')," \
                "('連江縣', '南竿鄉', '209')," \
               "('連江縣', '北竿鄉', '210')," \
                "('連江縣', '莒光鄉', '211')," \
                "('連江縣', '東引鄉', '212')"
        self._cr.execute(sql)
        return True