# -*- coding: utf-8 -*-

import logging
import zipcodetw
import collections

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
    Annual_membership_fee = fields.Char(string="會員年費")
    Annual_consultants_fee = fields.Char(string="顧問年費")
    coffin_amount = fields.Char(string="施棺滿足額")

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
        Annual_membership_fee = ir_config.get_param('Annual_membership_fee', default='1200')
        Annual_consultants_fee = ir_config.get_param('Annual_consultants_fee', default='10000')
        coffin_amount = ir_config.get_param('coffin_amount', default='30000')

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
            Annual_membership_fee = Annual_membership_fee,
            Annual_consultants_fee= Annual_consultants_fee,
            coffin_amount = coffin_amount,
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
        ir_config.set_param("Annual_membership_fee",self.Annual_membership_fee or '1200')
        ir_config.set_param("Annual_consultants_fee",self.Annual_consultants_fee or '10000')
        ir_config.set_param("coffin_amount",self.coffin_amount or '30000')
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
        # sql = "INSERT INTO normal_p(w_id,number,name,cellphone,con_phone,con_phone2,zip_code,address,con_addr,habbit_donate,donate_cycle,rec_type,ps,cashier_code,rec_send,is_donate,report_send,thanks_send,bank_check"\
        #       " ,prints_id,self_iden,bank_id,bank,bank_id2,account,prints_date,ps2)"\
        #       " SELECT code,number,name,cellphone,phone1,phone2, zip,addr,addr,cast(donate_code as Integer),cycle,case when annual_receipt = 'N' then 1 else 2 end as annualreceipt"\
        #       " ,ps,collector_code ,case when rec_send='N' then FALSE else TRUE end as rec_send"\
        #       " ,case when is_donate='N' then FALSE else TRUE end as is_donate "\
        #       " ,case when report_send='N' then FALSE else TRUE end as report_send ,case when thanks_send='N' then FALSE else TRUE end as thanks_send"\
        #       " ,case when bank_check='N' then FALSE else TRUE end as bank_check"\
        #       " ,check_num,p_id,bank_id,bankname,bank_id2,bankaccount,checkdate,transfer_note"\
        #       " from (SELECT 團員編號 AS code, '1' AS number, 姓名 AS name, 出生日期 AS birth, 手機 AS cellphone, 電話一 AS phone1, 電話二 AS phone2,郵遞區號 AS zip, 通訊地址 AS addr, 捐助種類編號 AS donate_code,捐助週期 AS cycle, 年收據 AS annual_receipt, 建檔日期 AS build_date, 備註 AS ps,收費員編號 AS collector_code, 收據寄送 AS rec_send,NULL AS is_donate, 自訂排序 AS sorting, 報表寄送 AS report_send, 感謝狀寄送 AS thanks_send, 銀行核印 AS bank_check, 核印批號 AS check_num, 身份證號 AS p_id, 扣款銀行代碼 AS bank_id, 扣款銀行 AS bankname, 扣款分行代碼 AS bank_id2, 扣款分行 AS bankname2, 銀行帳號 AS bankaccount, 核印日期 AS checkdate, 約定轉帳備註 AS transfer_note,輸入人員 AS key_in_user, 異動日期 AS db_chang_date"\
        #       " FROM 團員檔"\
        #       " where 郵遞區號='111'"\
        #       " UNION"\
        #       " SELECT 團員編號 AS code, 序號 AS number, 姓名 AS name, 出生日期 AS birth, 手機 AS cellphone, 電話一 AS phone1, 電話二 AS phone2, 郵遞區號 AS zip, 通訊地址 AS addr, 捐助種類編號 AS donate_code, NULL AS cycle, NULL AS annual_receipt , NULL AS build_date, NULL AS ps, NULL AS collector_code, 收據寄送 AS rec_send, 是否捐助 AS is_donate, 自訂排序 AS sorting , NULL AS report_send, NULL AS thanks_send, NULL AS bank_check, NULL AS check_num, NULL AS p_id, NULL AS bank_id, NULL AS bankname, NULL AS bank_id2, NULL AS bankname2, NULL AS bankaccount, NULL AS checkdate, NULL AS transfer_note,輸入人員 AS key_in_user, 異動日期 AS db_chang_date"\
        #       " FROM 團員眷屬檔"\
        #       " where 郵遞區號='111' and 序號 <> '1'"\
        #       " ) as aaa"\
        #       " LIMIT 1000"

        # 轉團員眷屬檔, 其中團員編號為空的資料共334筆未轉入
        sql = "INSERT INTO normal_p(w_id, number, name, cellphone, con_phone, con_phone2, zip, rec_addr, habbit_donate, rec_send, is_donate, temp_key_in_user, db_chang_date) "\
              " SELECT 團員編號, 序號, 姓名, 手機, 電話一, 電話二, 郵遞區號, 通訊地址, cast(捐助種類編號 as Integer), case when 收據寄送='N' then FALSE else TRUE end as 收據寄送, case when 是否捐助='N' then FALSE else TRUE end as 是否捐助, 輸入人員, case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期  FROM 團員眷屬檔 WHERE 團員編號 <>'' "
        self._cr.execute(sql)

        #轉入不在眷屬檔，在團員檔的資料，共7769筆
        sql = "INSERT INTO normal_p(w_id, name) "\
              " SELECT 團員編號, 姓名 FROM 團員檔"\
              " EXCEPT "\
              " SELECT 團員編號, 姓名 FROM 團員眷屬檔"
        self._cr.execute(sql)

        # 團員檔的資料比較齊全，因此把團員檔的資料寫入normal.p
        sql = "UPDATE normal_p " \
              " SET cellphone = a.手機, con_phone = a.電話一, con_phone2 = a.電話二, donate_cycle = cast(a.捐助週期 as Integer), zip_code = a.郵遞區號, con_addr = a.通訊地址, " \
              " merge_report = case when a.年收據='N' then FALSE else TRUE end, ps = a.備註, temp_cashier = a.收費員編號, rec_send = case when a.收據寄送='N' then FALSE else TRUE end, report_send = case when a.報表寄送='N' then FALSE else TRUE end," \
              " thanks_send = case when a.感謝狀寄送='N' then FALSE else TRUE end, prints = case when a.銀行核印='N' then FALSE else TRUE end, prints_id = a.核印批號, self_iden = a.身份證號, bank_id = a.扣款銀行代碼, bank = a.扣款銀行," \
              " bank_id2 = a.扣款分行代碼, bank2 = a.扣款分行, account = a.銀行帳號, prints_date = a.核印日期," \
              " ps2 = a.約定轉帳備註, temp_key_in_user = a.輸入人員, db_chang_date = case when a.異動日期='' then NULL else cast(a.異動日期 as date) end" \
              " FROM 團員檔 a WHERE a.團員編號 = normal_p.w_id and a.姓名 = normal_p.name"
        self._cr.execute(sql) # 全資料共768060筆
        sql = "UPDATE normal_p  SET active = TRUE"
        self._cr.execute(sql)  # 把所有捐款者資料的active設為TRUE, 不然基本資料會什麼都看不見, 共768060筆 花費12.103秒
        sql = "SELECT id,'AAA' || LPAD(CAST(row_number() OVER() AS VARCHAR),6,'0') AS new_coding into temp FROM normal_p"
        self._cr.execute(sql)
        sql = "UPDATE normal_p  SET new_coding = b.new_coding FROM temp b WHERE normal_p.id =b.id"
        self._cr.execute(sql)
        return True

    def set_leader(self): # 設定戶長
        sql = " UPDATE normal_p SET parent = a.id FROM normal_p a WHERE a.w_id = normal_p.w_id and a.number='1' "
        self._cr.execute(sql)
        return True

    def receipt_transfer(self): # 轉捐款檔
        sql = " INSERT INTO donate_order(paid_id,donate_id,donate_w_id,donate_w_id_number,donate_type,donate,donate_total,donate_date,report_year,clerk,db_chang_date, temp_key_in_user ) SELECT 收費編號,捐款編號,團員編號,序號,cast(捐助種類編號 as Integer),捐款金額,捐款總額,case when 捐款日期='' then NULL WHEN 捐款日期='.' THEN NULL else cast(捐款日期 as date) end as 捐款日期,case when 收據年度開立 = 'N' then FALSE else TRUE end as report_year,收費員編號, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期, 輸入人員 from 捐款檔 where 團員編號  in (select w_id from normal_p)"
        self._cr.execute(sql) # 捐款檔 共2795797筆 花費約56秒, 序號為空的有9筆 團員編號皆是E1204971
        sql = " INSERT INTO donate_order(paid_id,donate_id,donate_w_id,donate_w_id_number,donate_type,donate,donate_total,donate_date,report_year,clerk,db_chang_date, temp_key_in_user ) SELECT 收費編號,捐款編號,團員編號,序號,cast(捐助種類編號 as Integer),捐款金額,捐款總額,case when 捐款日期='' then NULL WHEN 捐款日期='.' THEN NULL else cast(捐款日期 as date) end as 捐款日期,case when 收據年度開立 = 'N' then FALSE else TRUE end as report_year,收費員編號, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期, 輸入人員 from 捐款歷史檔 where 團員編號  in (select w_id from normal_p)"
        self._cr.execute(sql)  # 捐款歷史檔 共86014筆, 轉入資料有85762花費2.012秒, 差252筆資料
        return True

    def set_donor(self): # normal.p 關聯捐款檔 設定捐款者
        sql = " UPDATE donate_order SET donate_member = a.id FROM normal_p a WHERE a.w_id = donate_order.donate_w_id AND a.number = donate_order.donate_w_id_number AND donate_order.donate_w_id_number <> '' "
        self._cr.execute(sql) # 全資料共2881559筆, 關聯資料共 2881015 筆 花費285.728秒, 序號為空的資料共9筆, 全部共差 544 筆資料(donate_member is None)
        return True

    def set_worker(self): #員工檔轉進 res.users
        sql = "INSERT INTO worker_data(now_job,birth,sex,con_phone2,self_iden,lev_date,w_id,con_addr,ps,cellphone,name,con_phone,highest_stu,come_date,db_chang_date) " \
              " SELECT 職稱, case when 出生日期='' then NULL else cast(出生日期 as date) end as 出生日期,性別, 電話二, 身份證號,case when 離職日期='' then NULL else cast(離職日期 as date) end as 離職日期, 員工編號, 通訊地址,備註,手機,姓名, 電話一,最高學歷,case when 到職日期='' then NULL else cast(到職日期 as date) end as 到職日期,case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期  FROM 員工檔"
        self._cr.execute(sql)
        sql = "INSERT INTO c.worker(now_job,birth,sex,con_phone2,self_iden,lev_date,w_id,con_addr,ps,cellphone,name,con_phone,highest_stu,come_date,db_chang_date) " \
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
        self._cr.execute(sql) # 關聯資料共 708306 筆,  共59754筆資料未關聯到, 其中 59753筆 輸入人員欄位有資料, 但其輸入人員已不在現職的員工名單之中, 剩下的1筆資料是原本輸入人員欄位就是空值
        return True

    def set_coffin_data(self): # 施棺檔轉入 coffin_base 共 14256筆, 花費0.21秒
        sql = "INSERT INTO coffin_base(coffin_id, donate_type, create_date, donate_price, finish, \"user\", coffin_date_year, coffin_date_group, coffin_date, geter, dealer, cellphone, con_phone, con_phone2, zip_code, dead_addr, donater_ps, ps, temp_key_in_user, db_chang_date) " \
              " SELECT 施棺編號, 捐助方式, case when 建檔日期='' then NULL WHEN 建檔日期='.' THEN NULL else cast(建檔日期 as date) end as 建檔日期, CAST(已捐總額 AS INTEGER), case when 結案='N' then FALSE else TRUE end as 結案, 受施者, 年度, case when 期別='' then NULL else CAST(期別 AS INTEGER) end as 期別, case when 施棺日期='' then NULL WHEN 施棺日期='.' THEN NULL else cast(施棺日期 as date) end as 施棺日期, 領款人, 處理者, 手機, 電話一, 電話二, 郵遞區號, 通訊地址, 捐款者備註, 備註, 輸入人員, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期 FROM 施棺檔"
        self._cr.execute(sql)
        sql = "UPDATE 施棺檔 SET 施棺日期='2009-06-30' FROM 施棺檔 WHERE 施棺日期='2009-06-31' "
        self._cr.execute(sql)
        sql = "UPDATE 施棺檔 SET 施棺日期='2010-08-27' FROM 施棺檔 WHERE 施棺日期='2010-80-27' "
        self._cr.execute(sql)
        # 施棺編號 00236 之施棺日期為 2009-06-31, 修改為2009-06-30
        # 施棺編號 01944, 01945, 01946, 01947 之施棺日期為 2010-80-27  修改為2010-08-27
        return True

    def set_coffin_donate(self): # 施棺捐款檔轉入 old_coffin_donation
        sql = "INSERT INTO old_coffin_donation(coffin_id, donate_id, donate_price)" \
              " SELECT 施棺編號, 捐款編號, CAST(捐款金額 AS INTEGER) FROM 施棺捐款檔"
        self._cr.execute(sql) # 施棺捐款檔轉入 old_coffin_donation 共166158筆, 花費 1.3秒
        return True

    def set_donate_single(self): # 捐款檔及捐款歷史檔篩選捐款編號作為唯一值, 以便做關聯
        sql = "INSERT INTO donate_single(donate_id, old_donate_total) SELECT distinct ON (捐款編號) 捐款編號, 捐款總額 FROM 捐款檔"
        self._cr.execute(sql) # 轉入資料共 1070889筆, 花費39.5秒
        sql = "INSERT INTO donate_single(donate_id, old_donate_total) SELECT distinct ON (捐款編號) 捐款編號, 捐款總額 FROM 捐款歷史檔"
        self._cr.execute(sql)  # 轉入資料共30737 筆, 花費1.125秒
        return True

    def set_donate_single_associated(self): # donate_single 關聯 donate_order
        sql = "UPDATE donate_order SET donate_list_id = a.id FROM donate_single a WHERE a.donate_id = donate_order.donate_id"
        self._cr.execute(sql) # 關聯資料共2881559筆, 花費555.758秒
        sql = "UPDATE donate_order SET state = 1 " # 將所有的捐款明細的狀態設為已產生
        self._cr.execute(sql) # 資料共2881559筆, 花費107.838秒
        sql = "UPDATE donate_single SET state = 2 "  # 將所有的捐款檔的狀態設為已列印
        self._cr.execute(sql)  # 資料共1101626筆, 花費18.343秒
        return True

    def set_coffin_id(self): # 舊施棺明細關聯施棺檔
        sql = "UPDATE old_coffin_donation SET old_coffin_donation_id = a.id FROM coffin_base a WHERE a.coffin_id = old_coffin_donation.coffin_id"
        self._cr.execute(sql)  # 關聯資料共166145筆, 花費3.442秒, 差13筆資料未關聯到, 因為沒有施棺編號
        return True

    def set_coffin_donate_single_associated(self): # 舊施棺明細關聯donate_single
        sql = "UPDATE old_coffin_donation SET donate_single_id = a.id FROM donate_single a WHERE a.donate_id = old_coffin_donation.donate_id"
        self._cr.execute(sql)  # 關聯資料共148006筆, 花費7.215秒
        return True

    def compute_coffin_donate(self): # 計算 coffin_donation的捐款編號與donate_order的捐款編號相符者, 將 可用餘額(available_balance)設為 0 ; 不相符者則將可用餘額設為捐款金額(donate)
        sql = "UPDATE donate_order SET available_balance = donate_order.donate"
        self._cr.execute(sql)  # 計算資料共2881560筆, 花費98.004秒
        sql = "UPDATE donate_order SET available_balance = 0 FROM coffin_donation a WHERE a.donate_id = donate_order.donate_id AND donate_order.donate_type = 3"
        self._cr.execute(sql)  # 計算資料共275777筆, 花費16.711秒 ;  共281565筆資料施棺的捐款金額為 0
        return True

    def set_consultant_data(self): # 轉顧問檔資料進normal.p, 顧問檔共142筆資料
        sql = "INSERT INTO normal_p(name , con_addr) SELECT 姓名, 戶籍通訊地址 FROM 顧問檔 EXCEPT SELECT name, con_addr FROM normal_p"
        self._cr.execute(sql) # 轉入顧問檔有資料但normal.p沒有資料的, 共有73筆資料
        sql = "UPDATE normal_p " \
              " SET consultant_id = a.顧問編號, cellphone = a.手機, con_phone = a.電話一, con_phone2 = a.電話二, zip_code = a.戶籍郵遞區號, con_addr = a.戶籍通訊地址, zip = a.郵遞區號, rec_addr = a.通訊地址, hire_date = case when a.聘顧日期='' then NULL else cast(a.聘顧日期 as date) end, build_date = case when a.建檔日期='' then NULL else cast(a.建檔日期 as date) end, " \
              " ps = a.備註, temp_cashier_name = a.收費員編號, rec_send = case when a.收據寄送='N' then FALSE else TRUE end, report_send = case when a.報表寄送='N' then FALSE else TRUE end, thanks_send = case when a.感謝狀寄送='N' then FALSE else TRUE end, self = a.自訂排序,temp_key_in_user = a.輸入人員, db_chang_date = case when a.異動日期='' then NULL else cast(a.異動日期 as date) end " \
              " FROM 顧問檔 a WHERE a.姓名 = normal_p.name and a.戶籍通訊地址 = normal_p.con_addr"
        self._cr.execute(sql) #顧問檔更新normal.p的資料共142筆, 花費 0.408 秒
        return True

    def set_member_data(self): # 轉會員檔資料進normal.p, 會員檔共7258筆資料
        sql = "INSERT INTO normal_p(name , con_addr) SELECT 姓名, 戶籍通訊地址 FROM 會員檔 EXCEPT SELECT name, con_addr FROM normal_p"
        self._cr.execute(sql)  # 轉入會員檔有資料但normal.p沒有資料的, 共有4654筆資料, 花費 0.398 秒
        sql = "UPDATE normal_p " \
              " SET member_id = a.會員編號, cellphone = a.手機, con_phone = a.電話一, con_phone2 = a.電話二, zip_code = a.戶籍郵遞區號, con_addr = a.戶籍通訊地址, zip = a.郵遞區號, rec_addr = a.通訊地址, build_date = case when a.建檔日期='' then NULL else cast(a.建檔日期 as date) end, self_iden = a.身份證號, member_type = case when 會員種類編號='' then NULL else CAST(會員種類編號 AS INTEGER) end, " \
              " ps = a.備註, temp_cashier_name = a.收費員編號, rec_send = case when a.收據寄送='N' then FALSE else TRUE end, booklist = case when a.名冊列印='N' then FALSE else TRUE end, self = a.自訂排序,temp_key_in_user = a.輸入人員, db_chang_date = case when a.異動日期='' then NULL else cast(a.異動日期 as date) end " \
              " FROM 會員檔 a WHERE a.姓名 = normal_p.name and a.戶籍通訊地址 = normal_p.con_addr"
        self._cr.execute(sql)  # 會員檔更新normal.p的資料共7304筆, 花費 0.804 秒
        return True

    def set_consultant(self): #顧問收費檔轉檔
        sql = "INSERT INTO consultant_fee(consultant_id,year,fee_code,fee_payable,fee_date,clerk_id) " \
              " SELECT 顧問編號,年度,收費編號,應繳金額,case when 收費日期='' then NULL else cast(收費日期 as date) end as 收費日期,收費員編號 from 顧問收費檔 "
        self._cr.execute(sql)  # 顧問收費檔共308筆資料, 花費0.008秒
        sql = "UPDATE consultant_fee SET normal_p_id = a.id FROM normal_p a WHERE a.consultant_id = consultant_fee.consultant_id"
        self._cr.execute(sql) # 更新顧問收費檔共307筆資料, 花費 0.235 秒, 顧問編號 V00198在normal_p沒有找到, 顧問檔也沒有找到
        return True

    def set_member(self): #會員收費檔轉檔
        sql = "SELECT DISTINCT on (member_id) * FROM normal_p WHERE member_id <>'' "
        self._cr.execute(sql)
        dict = self._cr.dictfetchall()  #normal.p有會員編號的資料共7304筆資料, 篩選不重複資料後, 總共7241筆資料, 重複資料共63筆
        # SELECT member_id FROM normal_p GROUP BY member_id HAVING (COUNT(*) > 1)  篩選出現不只一次的資料有49筆
        sql = ''
        sql = "INSERT INTO associatemember_fee(member_id,member_note_code,year,fee_code,fee_payable,fee_date,clerk_id) " \
              " SELECT 會員編號, 會員名冊編號,年度,收費編號,應繳金額,case when 收費日期='' then NULL else cast(收費日期 as date) end as 日期,收費員編號 from 會員收費檔 "
        self._cr.execute(sql)  # 會員收費檔 58097筆資料, 花費  0.427 秒
        sql = "SELECT DISTINCT on (member_id) * into member_temp FROM normal_p WHERE member_id <>'' "
        self._cr.execute(sql)
        sql = " UPDATE associatemember_fee SET normal_p_id = b.id FROM member_temp b WHERE associatemember_fee.member_id = b.member_id"
        self._cr.execute(sql)  # 篩選不重複資料的7241筆資料寫入臨時創建的資料表中, 並與normal.p進行關聯共57893筆資料, 花費 0.83 秒, 共204筆資料未關聯到 (會員編號在normal_p沒有找到, 會員檔也沒有找到)
        return True

    def set_cashier_data(self):
        sql = "INSERT INTO cashier_base(c_id, name, self_iden, con_phone, con_phone2, cellphone, zip_code, con_addr, build_date, ps, temp_key_in_user, db_chang_date) "\
              " SELECT 收費員編號, 姓名, 身份證號, 電話一, 電話二, 手機, 郵遞區號, 通訊地址, case when 建檔日期='' then NULL WHEN 建檔日期='.' THEN NULL else cast(建檔日期 as date) end as 建檔日期, 備註, 輸入人員, case when 異動日期='' then NULL WHEN 異動日期='.' THEN NULL else cast(異動日期 as date) end as 異動日期 from 收費員檔"
        self._cr.execute(sql) # 收費員檔共輸入 1381 筆資料, 花費0.027秒
        sql = " UPDATE cashier_base set key_in_user = a.id from res_users a where a.login = cashier_base.temp_key_in_user"
        self._cr.execute(sql)  # 關聯資料共1370筆, 花費0.03秒,  未關聯資料共11筆
        sql = " UPDATE normal_p set cashier_name = a.id from cashier_base a where a.c_id = normal_p.temp_cashier_name"
        self._cr.execute(sql)  # 關聯資料共5554筆, 花費1.544秒,  未關聯資料共767231筆
        return True

    def active_data(self):
        sql = "UPDATE normal_p  SET active = TRUE"
        self._cr.execute(sql)  # 把所有捐款者資料的active設為TRUE, 不然基本資料會什麼都看不見, 共772787筆 花費12.103秒
        sql = " UPDATE normal_p set key_in_user = a.id from res_users a where a.login = normal_p.temp_key_in_user"
        self._cr.execute(sql)  # 關聯資料共 712819 筆,  共59968 筆資料未關聯到, 判斷輸入人員已離職或temp_key_in_user為空值(1筆)
        sql = " UPDATE normal_p set member_type = '2' where member_type = '99' "
        self._cr.execute(sql) # 修改資料共6578 筆, 花費0.441秒
        return True

    def set_postal_code1(self):
        lines = self.env['normal.p'].search([])
        s = collections.Counter()
        zip=''
        for line in lines[0:400000]:
            zip = ''
            if line.rec_addr is False and line.con_addr: # 收據地址為空, 但卻有報表寄送地址
                zip = zipcodetw.find(line.con_addr)[0:3] #藉由報表寄送地址判讀該地址的郵遞區號, 並只取郵遞區號前3碼
                line.zip = zip # 將郵遞區號寫入 收據地址的郵遞區號
                line.rec_addr = line.con_addr # 將報表寄送地址寫入收據地址, 前提是收據地址是空的
            elif line.rec_addr: # 有收據地址
                zip = zipcodetw.find(line.rec_addr)[0:3] # 直接取郵遞區號前3碼
            if len(zip) < 3 and line.rec_addr: # 藉由程式判讀出來的郵遞區號, 若小於3碼則代表地址填寫錯誤, 找不到郵遞區號, 條件是收據地址不為空
                s['OOO'] += 1 # 該郵遞區號出現次數 +1
                if line.member_type == 1: # 判斷該筆捐款者資料是否為基本會員
                    if line.consultant_id: # 判斷是否具有顧問身分
                        line.new_coding = 'ACOOO' + str(s.get('OOO')).zfill(5) # 代表該捐款者是基本會員以及具有顧問身分
                    else:
                        line.new_coding = 'AOOO' + str(s.get('OOO')).zfill(5) # 代表該捐款者是基本會員
                elif line.member_type == 2: # 判斷該筆捐款者資料是否為贊助會員
                    if line.consultant_id:
                        line.new_coding = 'BCOOO' + str(s.get('OOO')).zfill(5) # 代表該捐款者是贊助會員以及具有顧問身分
                    else:
                        line.new_coding = 'BOOO' + str(s.get('OOO')).zfill(5) # 代表該捐款者是贊助會員
                elif line.member_type is False and line.consultant_id :
                    line.new_coding = 'COOO' + str(s.get('OOO')).zfill(5) #不具有任何會員身分但具有顧問身分
                else:
                    line.new_coding = 'OOO' + str(s.get('OOO')).zfill(5) # 什麼都沒有的一般捐款者
            elif len(zip) == 3 : # 郵遞區號有3碼, 代表該筆資料的地址可以找到相對應的郵遞區號
                line.zip = zip #將程式判斷的郵遞區號寫入該捐款者的收據地址郵遞區號
                s[zip] += 1 # 該郵遞區號的出現次數 +1
                if line.member_type == 1:
                    if line.consultant_id:
                        line.new_coding = 'AC' + zip + str(s.get(zip)).zfill(5)
                    else:
                        line.new_coding = 'A' + zip + str(s.get(zip)).zfill(5)
                elif line.member_type == 2:
                    if line.consultant_id:
                        line.new_coding = 'BC' + zip + str(s.get(zip)).zfill(5)
                    else:
                        line.new_coding = 'B' + zip + str(s.get(zip)).zfill(5)
                elif line.member_type is False and line.consultant_id :
                    line.new_coding = 'C' + zip + str(s.get(zip)).zfill(5)
                else:
                    line.new_coding = zip + str(s.get(zip)).zfill(5)

        postal_code_list = list(s.items()) # 將python 的 counter 轉換為陣列
        for i in range(len(postal_code_list)):
            sql = " INSERT INTO auto_donateid(zip, area_number) VALUES ('%s', '%s')" % (postal_code_list[i][0], postal_code_list[i][1])
            self._cr.execute(sql) # 將counter內的計數寫入資料庫之中
        s.clear()
        return True

    def set_postal_code2(self):
        lines = self.env['normal.p'].search([])
        last_time_data = self.env['auto.donateid'].search([])
        s = collections.Counter()
        zip=''
        for row in last_time_data: # 將資料庫計數器的資料撈出來, 放入python 的 counter之中, 以便繼續統計個郵遞區號的出現次數
            zip = row.zip
            s[zip] += int(row.area_number)
        zip = ''

        for line in lines[400001:]:
            zip = ''
            if line.rec_addr is False and line.con_addr:
                zip = zipcodetw.find(line.con_addr)[0:3]
                line.zip = zip
                line.rec_addr = line.con_addr
            elif line.rec_addr:
                zip = zipcodetw.find(line.rec_addr)[0:3]
            if len(zip) < 3 and line.rec_addr:
                s['OOO'] += 1
                if line.member_type == 1:
                    if line.consultant_id:
                        line.new_coding = 'ACOOO' + str(s.get('OOO')).zfill(5)
                    else:
                        line.new_coding = 'AOOO' + str(s.get('OOO')).zfill(5)
                elif line.member_type == 2:
                    if line.consultant_id:
                        line.new_coding = 'BCOOO' + str(s.get('OOO')).zfill(5)
                    else:
                        line.new_coding = 'BOOO' + str(s.get('OOO')).zfill(5)
                elif line.member_type is False and line.consultant_id :
                    line.new_coding = 'COOO' + str(s.get('OOO')).zfill(5)
                else:
                    line.new_coding = 'OOO' + str(s.get('OOO')).zfill(5)
            elif len(zip) == 3 :
                line.zip = zip
                s[zip] += 1
                if line.member_type == 1:
                    if line.consultant_id:
                        line.new_coding = 'AC' + zip + str(s.get(zip)).zfill(5)
                    else:
                        line.new_coding = 'A' + zip + str(s.get(zip)).zfill(5)
                elif line.member_type == 2:
                    if line.consultant_id:
                        line.new_coding = 'BC' + zip + str(s.get(zip)).zfill(5)
                    else:
                        line.new_coding = 'B' + zip + str(s.get(zip)).zfill(5)
                elif line.member_type is False and line.consultant_id :
                    line.new_coding = 'C' + zip + str(s.get(zip)).zfill(5)
                else:
                    line.new_coding = zip + str(s.get(zip)).zfill(5)

        postal_code_list = list(s.items())
        for i in range(len(postal_code_list)):
            postal_code_data = self.env['auto.donateid'].search([('zip','=',postal_code_list[i][0])]) # 搜尋資料庫的計數器是否具有該郵遞區號
            if postal_code_data:
                postal_code_data.area_number = postal_code_data.area_number + int(postal_code_list[i][1]) #有搜尋到 則更新資料庫計數器的數量
            else:
                sql = " INSERT INTO auto_donateid(zip, area_number) VALUES ('%s', '%s')" % (postal_code_list[i][0], postal_code_list[i][1]) # 沒有搜尋到則重新建立該郵遞區號的資料
                self._cr.execute(sql)
        s.clear()
        return True

    def set_postal_code3(self):

        return True

    def auto_zip_insert(self): #自動產生編號

        # sql = "INSERT INTO auto_donateid(zip) SELECT DISTINCT SUBSTRING(zip_code,1,3) FROM normal_p"
        # self._cr.execute(sql)
        # sql = "INSERT INTO auto_donateid(zip) VALUES ('000')"
        # self._cr.execute(sql)
        data = self.env['auto.donateid'].search([])
        data2 = self.env['normal.p'].search([()])

        for i in data:
            for j in data2:
                if j.zip_code == '':
                    j.zip_code = "000"
                if j.zip_code == i.zip:
                    i.area_number += 1
                    j.auto_num = i.area_number
                    j.auto_num = j.auto_num.zfill(5)
                    j.new_coding = i.zip + j.auto_num






