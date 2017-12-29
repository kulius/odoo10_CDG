# -*- coding: utf-8 -*-

import logging

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


    def data_transfer(self):
        sql = "INSERT INTO normal_p(w_id,number,name,cellphone,con_phone,con_phone2,zip_code,address,con_addr,habbit_donate,donate_cycle,rec_type,ps,cashier_code,rec_send,is_donate,report_send,thanks_send,bank_check"\
              " ,prints_id,self_iden,bank_id,bank,bank_id2,account,prints_date,ps2)"\
              " SELECT code,number,name,cellphone,phone1,phone2, zip,addr,addr,cast(donate_code as Integer),cycle,case when annual_receipt = 'N' then 1 else 2 end as annualreceipt"\
              " ,ps,collector_code ,case when rec_send='N' then FALSE else TRUE end as rec_send"\
              " ,case when is_donate='N' then FALSE else TRUE end as is_donate "\
              " ,case when report_send='N' then FALSE else TRUE end as report_send ,case when thanks_send='N' then FALSE else TRUE end as thanks_send"\
              " ,case when bank_check='N' then FALSE else TRUE end as bank_check"\
              " ,check_num,p_id,bank_id,bankname,bank_id2,bankaccount,checkdate,transfer_note"\
              " from (SELECT 團員編號 AS code, '1' AS number, 姓名 AS name, 出生日期 AS birth, 手機 AS cellphone, 電話一 AS phone1, 電話二 AS phone2,郵遞區號 AS zip, 通訊地址 AS addr, 捐助種類編號 AS donate_code,捐助週期 AS cycle, 年收據 AS annual_receipt, 建檔日期 AS build_date, 備註 AS ps,收費員編號 AS collector_code, 收據寄送 AS rec_send,NULL AS is_donate, 自訂排序 AS sorting, 報表寄送 AS report_send, 感謝狀寄送 AS thanks_send, 銀行核印 AS bank_check, 核印批號 AS check_num, 身份證號 AS p_id, 扣款銀行代碼 AS bank_id, 扣款銀行 AS bankname, 扣款分行代碼 AS bank_id2, 扣款分行 AS bankname2, 銀行帳號 AS bankaccount, 核印日期 AS checkdate, 約定轉帳備註 AS transfer_note,輸入人員 AS key_in_user, 異動日期 AS db_chang_date"\
              " FROM 團員檔"\
              " where 郵遞區號='111'"\
              " UNION"\
              " SELECT 團員編號 AS code, 序號 AS number, 姓名 AS name, 出生日期 AS birth, 手機 AS cellphone, 電話一 AS phone1, 電話二 AS phone2, 郵遞區號 AS zip, 通訊地址 AS addr, 捐助種類編號 AS donate_code, NULL AS cycle, NULL AS annual_receipt , NULL AS build_date, NULL AS ps, NULL AS collector_code, 收據寄送 AS rec_send, 是否捐助 AS is_donate, 自訂排序 AS sorting , NULL AS report_send, NULL AS thanks_send, NULL AS bank_check, NULL AS check_num, NULL AS p_id, NULL AS bank_id, NULL AS bankname, NULL AS bank_id2, NULL AS bankname2, NULL AS bankaccount, NULL AS checkdate, NULL AS transfer_note,輸入人員 AS key_in_user, 異動日期 AS db_chang_date"\
              " FROM 團員眷屬檔"\
              " where 郵遞區號='111' and 序號 <> '1'"\
              " ) as aaa"\
              " LIMIT 1000"
        self._cr.execute(sql)
        return True

    def set_leader(self):
        sql = "UPDATE normal_p SET parent = a.id FROM normal_p a WHERE a.w_id = normal_p.w_id and a.number='1' "
        self._cr.execute(sql)
        return True

    def receipt_transfer(self):
        sql = " INSERT INTO donate_order(paid_id,donate_id,donate_w_id,donate_w_id_number,donate_type,donate,donate_total,donate_date,report_year,clerk,db_chang_date) select 收費編號,捐款編號,團員編號,序號,cast(捐助種類編號 as Integer),捐款金額,捐款總額,cast(捐款日期 as DATE ),case when 收據年度開立 = 'N' then FALSE else TRUE end as report_year,收費員編號, cast(異動日期 as Date) from 捐款檔 where 團員編號  in (select w_id from normal_p)"
        self._cr.execute(sql)
        return True

    def set_donor(self):
        sql = 'update donate_order set donate_member = a.id from normal_p a where a.w_id = donate_order.donate_w_id and  a.number = donate_order.donate_w_id_number '
        self._cr.execute(sql)
        return True

    def set_worker(self):
        sql = "INSERT INTO worker_data(now_job,birth,sex,con_phone2,self_iden,lev_date,w_id,con_addr,ps,cellphone,name,con_phone,highest_stu,come_date,db_chang_date) " \
              "SELECT 職稱, case when 出生日期='' then NULL else cast(出生日期 as date) end as 出生日期,性別, 電話二, 身份證號,case when 離職日期='' then NULL else cast(離職日期 as date) end as 離職日期, 員工編號, 通訊地址,備註,手機,姓名, 電話一,最高學歷,case when 到職日期='' then NULL else cast(到職日期 as date) end as 到職日期,case when 異動日期='' then NULL else cast(異動日期 as date) end as 異動日期  FROM 員工檔"
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

    def set_coffin_id(self):
        sql = 'update coffin_donation set coffin_donation_id = a.id from coffin_base a where a.coffin_id = coffin_donation.coffin_id '
        self._cr.execute(sql)
        return True

    def set_consultant(self):
        sql = "UPDATE normal_p SET consultant_id = a.顧問編號 FROM 顧問檔 a WHERE a.姓名 = normal_p.name and a.戶籍通訊地址 = normal_p.con_addr"
        self._cr.execute(sql)
        sql = ''
        sql = "SELECT DISTINCT on (consultant_id) * FROM normal_p WHERE consultant_id <>'' and con_addr<>'' "
        self._cr.execute(sql)
        dict = self._cr.dictfetchall()  #
        sql = ''
        sql = "INSERT INTO consultant_fee(consultant_id,year,fee_code,fee_payable,fee_date,clerk_id) " \
              " SELECT 顧問編號,年度,收費編號,應繳金額,case when 收費日期='' then NULL else cast(收費日期 as date) end as 日期,收費員編號 from 顧問收費檔 "
        self._cr.execute(sql)  #
        datas = self.env['consultant.fee'].search([])
        for i in range(len(dict)):
            for data in datas:
                if data.consultant_id == dict[i]['consultant_id'] and data.consultant_id != '':
                    data.normal_p_id = dict[i]['id']
        return True

    def set_member(self):
        sql = "UPDATE normal_p SET member_id = a.會員編號 FROM 會員檔 a WHERE a.姓名 = normal_p.name and a.戶籍通訊地址 = normal_p.con_addr"
        self._cr.execute(sql)
        sql = ''
        sql = "SELECT DISTINCT on (member_id) * FROM normal_p WHERE member_id <>'' and con_addr<>'' "
        self._cr.execute(sql)
        dict = self._cr.dictfetchall()  # 6940
        sql = ''
        sql = "INSERT INTO associatemember_fee(member_id,member_note_code,year,fee_code,fee_payable,fee_date,clerk_id) " \
              " SELECT 會員編號, 會員名冊編號,年度,收費編號,應繳金額,case when 收費日期='' then NULL else cast(收費日期 as date) end as 日期,收費員編號 from 會員收費檔 "
        self._cr.execute(sql)  # 58000
        datas = self.env['associatemember.fee'].search([], limit=100)
        for i in range(len(dict)):
            for data in datas:
                if data.member_id == dict[i]['member_id'] and data.member_id != '':
                    data.normal_p_id = dict[i]['id']
        return True

    def auto_zip_insert(self):

        sql = "INSERT INTO auto_donateid(zip) SELECT DISTINCT SUBSTRING(zip_code,1,3) FROM normal_p"
        self._cr.execute(sql)
        sql = "INSERT INTO auto_donateid(zip) VALUES (0)"
        self._cr.execute(sql)
        data = self.env['normal.p'].search()
        data2 = self.env['auto.donateid'].search()

        for i in data:
            for j in data2:
                if i.zip_code == j.zip:
                    j.area_number += 1
                    i.auto_num = j.area_number
                    i.auto_num = i.auto_num.zfill(5)
                    i.new_coding = j.zip + i.auto_num
                # elif i.zip_code == '' and j.zip == '000' :
                #     j.area_number += 1
                #     i.auto_num = j.area_number
                #     j.zip = j.zip.zfill(3)
                #     i.auto_num = i.auto_num.zfill(5)
                #     i.new_coding = j.zip + i.auto_num
                #     若郵政區號為NULL處理未完成





