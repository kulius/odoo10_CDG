# -*- coding: utf-8 -*-

import logging, datetime
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
            exception_coffin_amount = exception_coffin_amount
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
        # 轉團員眷屬檔, 其中團員編號為空的資料共334筆未轉入
        sql = "INSERT INTO normal_p(w_id, number, name, cellphone, con_phone, con_phone2, zip, rec_addr, habbit_donate, is_merge, is_donate, temp_key_in_user, db_chang_date) "\
              " SELECT 團員編號, 序號, 姓名, 手機, 電話一, 電話二, 郵遞區號, 通訊地址, cast(捐助種類編號 as Integer), case when 收據寄送='N' then FALSE else TRUE end as 收據寄送, case when 是否捐助='N' then FALSE else TRUE end as 是否捐助, 輸入人員, case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期 FROM 團員眷屬檔 WHERE 團員編號 <>'' "
        self._cr.execute(sql) # 輸入765486筆資料, 花費9.687秒

        #轉入不在眷屬檔，在團員檔的資料，共7848筆, 花費7.251秒
        sql = "INSERT INTO normal_p(w_id, name) "\
              " SELECT 團員編號, 姓名 FROM 團員檔"\
              " EXCEPT "\
              " SELECT 團員編號, 姓名 FROM 團員眷屬檔"
        self._cr.execute(sql)

        # 團員檔的資料比較齊全，因此把團員檔的資料寫入normal.p, 更新255014筆資料, 共花費8.871秒
        sql = "UPDATE normal_p " \
              " SET cellphone = a.手機, con_phone = a.電話一, con_phone2 = a.電話二, donate_cycle = cast(a.捐助週期 as Integer), zip_code = a.郵遞區號, con_addr = a.通訊地址, " \
              " merge_report = case when a.年收據='N' then FALSE else TRUE end, ps = a.備註, temp_cashier = a.收費員編號, rec_send = case when a.收據寄送='N' then FALSE else TRUE end, report_send = case when a.報表寄送='N' then FALSE else TRUE end," \
              " thanks_send = case when a.感謝狀寄送='N' then FALSE else TRUE end, prints = case when a.銀行核印='N' then FALSE else TRUE end, prints_id = a.核印批號, self_iden = a.身份證號, bank_id = a.扣款銀行代碼, bank = a.扣款銀行," \
              " bank_id2 = a.扣款分行代碼, bank2 = a.扣款分行, account = a.銀行帳號, prints_date = a.核印日期," \
              " ps2 = a.約定轉帳備註, temp_key_in_user = a.輸入人員, db_chang_date = case when a.異動日期='' then NULL else cast(a.異動日期 as date) end" \
              " FROM 團員檔 a WHERE a.團員編號 = normal_p.w_id and a.姓名 = normal_p.name"
        self._cr.execute(sql) # 全資料共773334筆
        sql = "UPDATE normal_p SET temp_cashier = a.收費員編號 FROM 團員檔 a WHERE a.團員編號 = normal_p.w_id"
        self._cr.execute(sql) # 更新772197筆資料, 花費17.647秒
        sql = "UPDATE normal_p  SET active = TRUE"
        self._cr.execute(sql)  # 把所有捐款者資料的active設為TRUE, 不然基本資料會什麼都看不見, 共773334筆 花費11.692秒
        return True

    def set_leader(self): # 設定戶長
        sql = " UPDATE normal_p SET parent = a.id FROM normal_p a WHERE a.w_id = normal_p.w_id and a.number='1' "
        self._cr.execute(sql) #更新770896筆資料, 花費47.314秒
        return True

    def receipt_transfer(self): # 轉捐款檔
        sql = " INSERT INTO donate_order(paid_id,donate_id,donate_w_id,donate_w_id_number,donate_type,donate,donate_total,donate_date,report_year,clerk,db_chang_date, temp_key_in_user ) SELECT 收費編號,捐款編號,團員編號,序號,cast(捐助種類編號 as Integer),捐款金額,捐款總額,case when 捐款日期='' then NULL WHEN 捐款日期='.' THEN NULL else cast(捐款日期 as date) end as 捐款日期,case when 收據年度開立 = 'N' then FALSE else TRUE end as report_year,收費員編號, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期, 輸入人員 from 捐款歷史檔 where 團員編號  in (select w_id from normal_p)"
        self._cr.execute(sql)  # 捐款歷史檔 共89676筆資料, 轉入89415筆, 差261筆資料, 花費2.784秒

        sql = " INSERT INTO donate_order(paid_id,donate_id,donate_w_id,donate_w_id_number,donate_type,donate,donate_total,donate_date,report_year,clerk,db_chang_date, temp_key_in_user ) SELECT 收費編號,捐款編號,團員編號,序號,cast(捐助種類編號 as Integer),捐款金額,捐款總額,case when 捐款日期='' then NULL WHEN 捐款日期='.' THEN NULL else cast(捐款日期 as date) end as 捐款日期,case when 收據年度開立 = 'N' then FALSE else TRUE end as report_year,收費員編號, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期, 輸入人員 from 捐款檔 where 團員編號  in (select w_id from normal_p)"
        self._cr.execute(sql) # 捐款檔 共2911750筆 花費約70.620秒, 序號為空的有10筆 團員編號皆是E1204971
        return True

    def set_donor(self): # normal.p 關聯捐款檔 設定捐款者
        sql = " UPDATE donate_order SET donate_member = a.id FROM normal_p a WHERE a.w_id = donate_order.donate_w_id AND a.number = donate_order.donate_w_id_number AND donate_order.donate_w_id_number <> '' "
        self._cr.execute(sql) # 全資料共3001165筆, 關聯資料共3000603 筆 花費662.986秒, 序號為空的資料共10筆, 全部共差 562 筆資料(donate_member is None)
        return True

    def set_worker(self): #員工檔轉進 res.users
        sql = "INSERT INTO worker_data(now_job,birth,sex,con_phone2,self_iden,lev_date,w_id,con_addr,ps,cellphone,name,con_phone,highest_stu,come_date,db_chang_date) " \
              " SELECT 職稱, case when 出生日期='' then NULL else cast(出生日期 as date) end as 出生日期,性別, 電話二, 身份證號,case when 離職日期='' then NULL else cast(離職日期 as date) end as 離職日期, 員工編號, 通訊地址,備註,手機,姓名, 電話一,最高學歷,case when 到職日期='' then NULL else cast(到職日期 as date) end as 到職日期,case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期  FROM 員工檔"
        self._cr.execute(sql)
        sql = "INSERT INTO c_worker(now_job,birth,sex,con_phone2,self_iden,lev_date,w_id,con_addr,ps,cellphone,name,con_phone,highest_stu,come_date,db_chang_date) " \
              " SELECT 職稱, case when 出生日期='' then NULL else cast(出生日期 as date) end as 出生日期,性別, 電話二, 身份證號,case when 離職日期='' then NULL else cast(離職日期 as date) end as 離職日期, 員工編號, 通訊地址,備註,手機,姓名, 電話一,最高學歷,case when 到職日期='' then NULL else cast(到職日期 as date) end as 到職日期,case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期  FROM 員工檔"
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
        self._cr.execute(sql) # 關聯資料共 714017 筆,  共59316筆資料未關聯到, 其中59315筆 輸入人員欄位有資料, 但其輸入人員已不在現職的員工名單之中, 其中有1名捐款者原資料的輸入人員欄位為空
        return True

    def set_coffin_data(self): # 施棺檔轉入 coffin_base 共 14256筆, 花費0.21秒
        sql = "UPDATE 施棺檔 SET 施棺日期='2009-06-30' WHERE 施棺日期='2009-06-31' "
        self._cr.execute(sql)
        sql = "UPDATE 施棺檔 SET 施棺日期='2010-08-27' WHERE 施棺日期='2010-80-27' "
        self._cr.execute(sql)
        sql = "INSERT INTO coffin_base(coffin_id, donate_type, create_date, donate_price, finish, \"user\", coffin_date_year, coffin_date_group, coffin_date, geter, dealer, cellphone, con_phone, con_phone2, zip_code, con_addr, donater_ps, ps, temp_key_in_user, db_chang_date) " \
              " SELECT 施棺編號, 捐助方式, case when 建檔日期='' then NULL WHEN 建檔日期='.' THEN NULL else cast(建檔日期 as date) end as 建檔日期, CAST(已捐總額 AS INTEGER), case when 結案='N' then FALSE else TRUE end as 結案, 受施者, 年度, case when 期別='' then NULL else CAST(期別 AS INTEGER) end as 期別, case when 施棺日期='' then NULL WHEN 施棺日期='.' THEN NULL else cast(施棺日期 as date) end as 施棺日期, 領款人, 處理者, 手機, 電話一, 電話二, 郵遞區號, 通訊地址, 捐款者備註, 備註, 輸入人員, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期 FROM 施棺檔"
        self._cr.execute(sql) # 輸入共14768筆資料,花費0.180秒
        # 施棺編號 00236 之施棺日期為 2009-06-31, 修改為2009-06-30
        # 施棺編號 01944, 01945, 01946, 01947 之施棺日期為 2010-80-27  修改為2010-08-27
        sql = "UPDATE coffin_base set dead_date = a.coffin_date from coffin_base a where a.id = coffin_base.id"
        self._cr.execute(sql)  # 計算資料共14768筆, 花費0.151秒 ; 舊資料設定領款日期等餘死亡日期
        sql = "UPDATE coffin_base set donate_apply_price = a.donate_price from coffin_base a where a.id = coffin_base.id and a.finish IS TRUE"
        self._cr.execute(sql)  # 計算資料共12102筆, 花費 0.126秒 ; 已結案的舊資料設定累積金額等於申請金額
        return True

    def set_coffin_donate(self): # 施棺捐款檔轉入 old_coffin_donation
        sql = "INSERT INTO old_coffin_donation(coffin_id, donate_id, donate_price) SELECT 施棺編號, 捐款編號, CAST(捐款金額 AS INTEGER) FROM 施棺捐款檔"
        self._cr.execute(sql) # 施棺捐款檔轉入 old_coffin_donation 共180220筆, 花費1.322秒
        return True

    def set_donate_single(self): # 捐款檔及捐款歷史檔篩選捐款編號作為唯一值, 以便做關聯
        sql = "SELECT 捐款編號,MIN(序號) INTO temp_table2 FROM 捐款歷史檔 WHERE 序號<>'' GROUP BY 捐款編號"
        self._cr.execute(sql)  # 挑選捐款編號作為唯一值, 並挑出序號值最小的資料共32004筆, 花費0.107秒
        sql = "INSERT INTO donate_single(donate_id,donate_member_number) SELECT 捐款編號,min FROM temp_table2"
        self._cr.execute(sql)  # 寫入收據編號及舊團員序號資料共32004筆, 花費約0.366秒
        sql = "UPDATE donate_single SET donate_member_w_id = a.團員編號,old_donate_total = a.捐款總額, donate_date = case when a.捐款日期='' then NULL WHEN a.捐款日期='.' THEN NULL else cast(a.捐款日期 as date) end, temp_work_id=a.收費員編號,year_receipt_send =case when a.收據年度開立='N' then FALSE else TRUE end,paid_id=a.收費編號,temp_key_in_user = a.輸入人員 FROM 捐款歷史檔 a WHERE donate_single.donate_id = a.捐款編號 AND donate_single.donate_member_number = a.序號"
        self._cr.execute(sql)  # 更新資料共35446筆, 花費約3.597秒
        sql = "UPDATE donate_single SET name = a.name, self_iden = a.self_iden, cellphone = a.cellphone, con_phone = a.con_phone, zip_code = a.zip_code ,con_addr = a.con_addr FROM normal_p a WHERE a.w_id = donate_single.donate_member_w_id AND a.number = donate_single.donate_member_number"
        self._cr.execute(sql)  # 更新資料共1146809筆, 花費約44.808秒

        sql = "SELECT 捐款編號,MIN(序號) INTO temp_table FROM 捐款檔 WHERE 序號<>'' GROUP BY 捐款編號"
        self._cr.execute(sql) # 挑選捐款編號作為唯一值, 並挑出序號值最小的資料共1115080筆, 花費26.740秒
        sql = "INSERT INTO donate_single(donate_id,donate_member_number) SELECT 捐款編號,\"min\" FROM temp_table"
        self._cr.execute(sql)  # 寫入收據編號及舊團員序號資料共1115080筆, 花費約13.957秒
        sql = "UPDATE donate_single SET donate_member_w_id = a.團員編號,old_donate_total = a.捐款總額, donate_date = case when a.捐款日期='' then NULL WHEN a.捐款日期='.' THEN NULL else cast(a.捐款日期 as date) end, temp_work_id=a.收費員編號,year_receipt_send =case when a.收據年度開立='N' then FALSE else TRUE end,paid_id=a.收費編號,temp_key_in_user = a.輸入人員 FROM 捐款檔 a WHERE donate_single.donate_id = a.捐款編號 AND donate_single.donate_member_number = a.序號"
        self._cr.execute(sql)  # 更新資料共1115080筆, 花費約28.725秒
        sql = "UPDATE donate_single SET name = a.name, self_iden = a.self_iden, cellphone = a.cellphone, con_phone = a.con_phone, zip_code = a.zip_code ,con_addr = a.con_addr FROM normal_p a WHERE a.w_id = donate_single.donate_member_w_id AND a.number = donate_single.donate_member_number"
        self._cr.execute(sql)  # 更新資料共1115055筆, 花費約63.721秒

        sql = "UPDATE donate_single SET donate_member = a.id, receipt_send = a.rec_send, report_send = a.report_send, year_receipt_send = a.merge_report FROM normal_p a WHERE donate_single.donate_member_w_id = a.w_id AND donate_single.donate_member_number = a.number"
        self._cr.execute(sql)  # 更新資料共1146809筆, 花費約54.058秒
        return True

    def set_donate_single_associated(self): # donate_single 關聯 donate_order
        sql = "UPDATE donate_order SET donate_list_id = a.id FROM donate_single a WHERE a.donate_id = donate_order.donate_id"
        self._cr.execute(sql) # 關聯資料共3001165筆, 花費547.055秒
        sql = "UPDATE donate_order SET state = 1 " # 將所有的捐款明細的狀態設為已產生
        self._cr.execute(sql) # 資料共3001165筆, 花費166.141秒
        sql = "UPDATE donate_single SET state = 2 "  # 將所有的捐款檔的狀態設為已列印
        self._cr.execute(sql)  # 資料共1147084筆, 花費28.811秒
        return True

    def set_coffin_id(self): # 舊施棺明細關聯施棺檔
        sql = "UPDATE old_coffin_donation SET old_coffin_donation_id = a.id FROM coffin_base a WHERE a.coffin_id = old_coffin_donation.coffin_id"
        self._cr.execute(sql)  # 關聯資料共180207筆, 花費3.048秒, 差13筆資料未關聯到, 因為沒有施棺編號
        return True

    def set_coffin_donate_single_associated(self): # 舊施棺明細關聯donate_single
        sql = "UPDATE old_coffin_donation SET donate_single_id = a.id FROM donate_single a WHERE a.donate_id = old_coffin_donation.donate_id"
        self._cr.execute(sql)  # 關聯資料共162068筆, 花費7.007秒
        return True

    def compute_coffin_donate(self): # 計算 coffin_donation的捐款編號與donate_order的捐款編號相符者, 將可用餘額(available_balance)設為 0 ; 不相符者則將可用餘額設為捐款金額(donate)

        sql = "UPDATE donate_order SET available_balance = donate_order.donate"
        self._cr.execute(sql)  # 計算資料共3001165筆, 花費101.806秒
        sql = "UPDATE donate_order SET available_balance = 0 FROM old_coffin_donation a WHERE a.donate_id = donate_order.donate_id AND donate_order.donate_type = 3"
        self._cr.execute(sql)  # 計算資料共298074筆, 花費40.667秒 ;  共303549筆資料施棺的捐款金額為 0
        sql = "UPDATE donate_order SET use_amount = TRUE WHERE available_balance = 0 and donate_type = 3"
        self._cr.execute(sql)  # 計算資料共303549筆, 花費15.818秒
        sql = "UPDATE donate_order SET used_money = donate_order.donate WHERE available_balance = 0 and donate_type = 3"
        self._cr.execute(sql)  # 計算資料共303549筆, 花費6.952秒
        return True

    def set_consultant_data(self): # 轉顧問檔資料進normal.p, 顧問檔共199筆資料
        sql = "INSERT INTO normal_p(name , con_addr) SELECT 姓名, 戶籍通訊地址 FROM 顧問檔 EXCEPT SELECT name, con_addr FROM normal_p"
        self._cr.execute(sql) # 轉入顧問檔有資料但normal.p沒有資料的, 共有71筆資料, 轉入資料共128筆
        sql = "UPDATE normal_p " \
              " SET consultant_id = a.顧問編號, cellphone = a.手機, con_phone = a.電話一, con_phone2 = a.電話二, zip_code = a.戶籍郵遞區號, con_addr = a.戶籍通訊地址, zip = a.郵遞區號, rec_addr = a.通訊地址, hire_date = case when a.聘顧日期='' then NULL else cast(a.聘顧日期 as date) end, build_date = case when a.建檔日期='' then NULL else cast(a.建檔日期 as date) end, " \
              " ps = a.備註, temp_cashier = a.收費員編號, rec_send = case when a.收據寄送='N' then FALSE else TRUE end, report_send = case when a.報表寄送='N' then FALSE else TRUE end, thanks_send = case when a.感謝狀寄送='N' then FALSE else TRUE end, self = a.自訂排序,temp_key_in_user = a.輸入人員, db_chang_date = case when a.異動日期='' then NULL else cast(a.異動日期 as date) end " \
              " FROM 顧問檔 a WHERE a.姓名 = normal_p.name and a.戶籍通訊地址 = normal_p.con_addr"
        self._cr.execute(sql) #顧問檔更新normal.p的資料共199筆, 花費 0.574 秒
        return True

    def set_member_data(self): # 轉會員檔資料進normal.p, 會員檔共7303筆資料
        sql = "INSERT INTO normal_p(name , con_addr) SELECT 姓名, 戶籍通訊地址 FROM 會員檔 EXCEPT SELECT name, con_addr FROM normal_p"
        self._cr.execute(sql)  # 轉入會員檔有資料但normal.p沒有資料的, 共有4688筆資料, 花費0.603 秒
        sql = "UPDATE normal_p " \
              " SET member_id = a.會員編號, cellphone = a.手機, con_phone = a.電話一, con_phone2 = a.電話二, zip_code = a.戶籍郵遞區號, con_addr = a.戶籍通訊地址, zip = a.郵遞區號, rec_addr = a.通訊地址, build_date = case when a.建檔日期='' then NULL else cast(a.建檔日期 as date) end, self_iden = a.身份證號, member_type = case when 會員種類編號='' then NULL else CAST(會員種類編號 AS INTEGER) end, " \
              " ps = a.備註, temp_cashier = a.收費員編號, rec_send = case when a.收據寄送='N' then FALSE else TRUE end, booklist = case when a.名冊列印='N' then FALSE else TRUE end, self = a.自訂排序,temp_key_in_user = a.輸入人員, db_chang_date = case when a.異動日期='' then NULL else cast(a.異動日期 as date) end " \
              " FROM 會員檔 a WHERE a.姓名 = normal_p.name and a.戶籍通訊地址 = normal_p.con_addr"
        self._cr.execute(sql)  # 會員檔更新normal.p的資料共7349筆, 花費1.074 秒
        return True

    def set_consultant(self): #顧問收費檔轉檔
        sql = "INSERT INTO consultant_fee(consultant_id,year,fee_code,fee_payable,fee_date,clerk_id) " \
              " SELECT 顧問編號,年度,收費編號,應繳金額,case when 收費日期='' then NULL else cast(收費日期 as date) end as 收費日期,收費員編號 from 顧問收費檔 "
        self._cr.execute(sql)  # 顧問收費檔共508筆資料, 花費0.030秒
        sql = "UPDATE consultant_fee SET normal_p_id = a.id FROM normal_p a WHERE a.consultant_id = consultant_fee.consultant_id"
        self._cr.execute(sql) # 更新顧問收費檔共507筆資料, 花費0.4 秒, 顧問編號 V00198在normal_p沒有找到, 顧問檔也沒有找到
        return True

    def set_member(self): #會員收費檔轉檔
        sql = "SELECT DISTINCT on (member_id) * FROM normal_p WHERE member_id <>'' "
        self._cr.execute(sql)
        dict = self._cr.dictfetchall()  #normal.p有會員編號的資料共7304筆資料, 篩選不重複資料後, 總共7286筆資料
        # SELECT member_id FROM normal_p GROUP BY member_id HAVING (COUNT(*) > 1)  篩選出現不只一次的資料有49筆
        sql = ''
        sql = "INSERT INTO associatemember_fee(member_id,member_note_code,year,fee_code,fee_payable,fee_date,clerk_id) " \
              " SELECT 會員編號, 會員名冊編號,年度,收費編號,應繳金額,case when 收費日期='' then NULL else cast(收費日期 as date) end as 日期,收費員編號 from 會員收費檔 "
        self._cr.execute(sql)  # 會員收費檔 65416筆資料, 花費 0.485 秒
        sql = "SELECT DISTINCT on (member_id) * into member_temp FROM normal_p WHERE member_id <>'' "
        self._cr.execute(sql) # 共7286筆資料, 花費0.313秒
        sql = " UPDATE associatemember_fee SET normal_p_id = b.id FROM member_temp b WHERE associatemember_fee.member_id = b.member_id"
        self._cr.execute(sql)  # 篩選不重複資料的7286筆資料寫入臨時創建的資料表中, 並與normal.p進行關聯共65195筆資料, 花費1.324 秒
        return True

    def set_cashier_data(self): # 收費員檔轉入 cashier_base 及收費員&輸入人員對各資料表的關聯
        sql = "INSERT INTO cashier_base(c_id, name, self_iden, con_phone, con_phone2, cellphone, zip_code, con_addr, build_date, ps, temp_key_in_user, db_chang_date) "\
              " SELECT 收費員編號, 姓名, 身份證號, 電話一, 電話二, 手機, 郵遞區號, 通訊地址, case when 建檔日期='' then NULL WHEN 建檔日期='.' THEN NULL else cast(建檔日期 as date) end as 建檔日期, 備註, 輸入人員, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期 from 收費員檔"
        self._cr.execute(sql) # 收費員檔共輸入 1385 筆資料, 花費0.037秒
        sql = " UPDATE cashier_base set key_in_user = a.id from res_users a where a.login = cashier_base.temp_key_in_user"
        self._cr.execute(sql)  # 更新資料共1374筆, 花費0.031秒
        sql = " UPDATE normal_p set cashier_name = a.id from cashier_base a where a.c_id = normal_p.temp_cashier"
        self._cr.execute(sql)  # 更新資料共762123筆, 花費22.080秒
        sql = " UPDATE donate_single set work_id = a.id from cashier_base a where a.c_id = donate_single.temp_work_id"
        self._cr.execute(sql)  # 更新資料共1147032筆, 花費44.450秒
        sql = " UPDATE donate_order set cashier = a.id from cashier_base a where a.c_id = donate_order.clerk"
        self._cr.execute(sql)  # 關聯資料共3001037筆, 花費113.045秒
        sql = " UPDATE donate_single set key_in_user = a.id from res_users a where a.login = donate_single.temp_key_in_user"
        self._cr.execute(sql)  # 關聯資料共1072573筆, 花費46.664秒
        sql = " UPDATE donate_order set key_in_user = a.id from res_users a where a.login = donate_order.temp_key_in_user"
        self._cr.execute(sql)  # 關聯資料共2814283筆, 花費133.597秒
        return True

    def active_data(self):
        sql = "UPDATE normal_p  SET active = TRUE"
        self._cr.execute(sql)  # 把所有捐款者資料的active設為TRUE, 不然基本資料會什麼都看不見, 共778150筆 花費15.093秒
        sql = " UPDATE normal_p set key_in_user = a.id from res_users a where a.login = normal_p.temp_key_in_user"
        self._cr.execute(sql)  # 關聯資料共 718619 筆,花費17.781秒
        sql = " UPDATE normal_p set member_type = '2' where member_type = '99' "
        self._cr.execute(sql) # 修改資料共6609 筆, 花費0.569秒
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

    def set_donate_id(self):
        y = 2003 # 資料庫存在的最早資料是2003年9月
        m = 8
        while y<=2018:
            while m<=12:
                if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
                    d2 = 31
                elif m == 2:
                    d2 = 28
                else:
                    d2 = 30

                sql = " SELECT COUNT(*) FROM donate_order WHERE donate_date BETWEEN '%s-%s-%s' AND '%s-%s-%s' AND donate_date IS NOT NULL" % (y, m, 1, y, m, d2)
                self._cr.execute(sql)
                for count in self._cr.dictfetchall():  # 取出計算捐款人數後的資料筆數
                    count_datas_number = count['count']

                sql = " SELECT donate_w_id, donate_w_id_number FROM donate_order WHERE donate_date BETWEEN '%s-%s-%s' AND '%s-%s-%s' AND donate_date IS NOT NULL GROUP BY donate_w_id, donate_w_id_number" % (y, m, 1, y, m, d2)
                self._cr.execute(sql)
                number_of_people = len(self._cr.dictfetchall()) #濾掉重複捐款後的人數

                sql = " SELECT COUNT(*)  FROM donate_single WHERE donate_date BETWEEN '%s-%s-%s' AND '%s-%s-%s' AND donate_date IS NOT NULL" % (y, m, 1, y, m, d2)
                self._cr.execute(sql)
                for count in self._cr.dictfetchall():  # 取出計算收據數量後的資料筆數
                    count_datas_receipt_number = count['count']

                sql = " SELECT DISTINCT ON (donate_member_w_id) * FROM donate_single WHERE donate_date BETWEEN '%s-%s-%s' AND '%s-%s-%s' AND donate_date IS NOT NULL" % (y, m, 1, y, m, d2)
                self._cr.execute(sql)
                count_datas_households_number = len(self._cr.dictfetchall()) #濾掉重複捐款後的捐款戶數

                if count_datas_number != 0 or count_datas_receipt_number != 0:
                    sql = " INSERT INTO donate_statistics(year, month, number, number_of_people, receipt_number, households) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (y, m, count_datas_number, number_of_people, count_datas_receipt_number, count_datas_households_number)
                    self._cr.execute(sql)
                m = m + 1
            m = 1
            y = y + 1
            if y == 2018 and m == 2:
                break
            # 總共費時約 12 分鐘, 資料追朔至2003年
        return True

    # def set_postal_code1(self):  # 花費時間約18分鐘
    #     lines = self.env['normal.p'].search([])
    #     s = collections.Counter()
    #     zip = ''
    #     for line in lines[0:400000]:
    #         zip = ''
    #         if line.rec_addr is False and line.con_addr:  # 收據地址為空, 但卻有報表寄送地址
    #             zip = zipcodetw.find(line.con_addr)[0:3]  # 藉由報表寄送地址判讀該地址的郵遞區號, 並只取郵遞區號前3碼
    #             line.zip = zip  # 將郵遞區號寫入 收據地址的郵遞區號
    #             line.rec_addr = line.con_addr  # 將報表寄送地址寫入收據地址, 前提是收據地址是空的
    #         elif line.rec_addr:  # 有收據地址
    #             zip = zipcodetw.find(line.rec_addr)[0:3]  # 直接取郵遞區號前3碼
    #         if len(zip) < 3 and line.rec_addr:  # 藉由程式判讀出來的郵遞區號, 若小於3碼則代表地址填寫錯誤, 找不到郵遞區號, 條件是收據地址不為空
    #             s['999'] += 1  # 該郵遞區號出現次數 +1
    #             line.new_coding = '999' + str(s.get('999')).zfill(5)  # 什麼都沒有的一般捐款者
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
    #         s[zip] += int(row.area_number)
    #     zip = ''
    #
    #     for line in lines[400000:]:
    #         zip = ''
    #         if line.rec_addr is False and line.con_addr:
    #             zip = zipcodetw.find(line.con_addr)[0:3]
    #             line.zip = zip
    #             line.rec_addr = line.con_addr
    #         elif line.rec_addr:
    #             zip = zipcodetw.find(line.rec_addr)[0:3]
    #         if len(zip) < 3 and line.rec_addr:
    #             s['999'] += 1
    #             line.new_coding = '999' + str(s.get('999')).zfill(5)
    #         elif len(zip) == 3:
    #             line.zip = zip
    #             s[zip] += 1
    #             line.new_coding = zip + str(s.get(zip)).zfill(5)
    #
    #     postal_code_list = list(s.items())
    #     for i in range(len(postal_code_list)):
    #         postal_code_data = self.env['auto.donateid'].search(
    #             [('zip', '=', postal_code_list[i][0])])  # 搜尋資料庫的計數器是否具有該郵遞區號
    #         if postal_code_data:
    #             postal_code_data.area_number = postal_code_data.area_number + int(
    #                 postal_code_list[i][1])  # 有搜尋到 則更新資料庫計數器的數量
    #         else:
    #             sql = " INSERT INTO auto_donateid(zip, area_number) VALUES ('%s', '%s')" % (postal_code_list[i][0], postal_code_list[i][1])  # 沒有搜尋到則重新建立該郵遞區號的資料
    #             self._cr.execute(sql)
    #     s.clear()
    #     return True
    #
    # def set_postal_code3(self):  # 沒有收據寄送地址, 也沒有報表寄送地址
    #     lines = self.env['normal.p'].search([('new_coding', '=', False)])
    #     last_time_data = self.env['auto.donateid'].search([])
    #     s = collections.Counter()
    #     zip = ''
    #     for row in last_time_data:  # 將資料庫計數器的資料撈出來, 放入python 的 counter之中, 以便繼續統計個郵遞區號的出現次數
    #         zip = row.zip
    #         s[zip] += int(row.area_number)
    #     zip = ''
    #
    #     for line in lines:
    #         s['999'] += 1
    #         line.new_coding = '999' + str(s.get('999')).zfill(5)
    #
    #     postal_code_list = list(s.items())
    #     for i in range(len(postal_code_list)):
    #         postal_code_data = self.env['auto.donateid'].search(
    #             [('zip', '=', postal_code_list[i][0])])  # 搜尋資料庫的計數器是否具有該郵遞區號
    #         if postal_code_data:
    #             postal_code_data.area_number = postal_code_data.area_number + int(
    #                 postal_code_list[i][1])  # 有搜尋到 則更新資料庫計數器的數量
    #         else:
    #             sql = " INSERT INTO auto_donateid(zip, area_number) VALUES ('%s', '%s')" % (postal_code_list[i][0], postal_code_list[i][1])  # 沒有搜尋到則重新建立該郵遞區號的資料
    #             self._cr.execute(sql)
    #     s.clear()
    #     return True

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