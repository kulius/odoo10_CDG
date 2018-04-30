# -*- coding: utf-8 -*-
import datetime
from odoo.exceptions import ValidationError
from odoo import models, fields, api

class PoorBase(models.Model):
    _name = 'poor.base'

    #純文字的欄位
    name = fields.Char('案主姓名',required = True)
    self_iden = fields.Char('案主身分證號',required = True)
    birth = fields.Date('案主出生年月日',required = True)
    case_id = fields.Char('案件編號',readonly=True)
    telephone = fields.Char('案主電話')
    phone = fields.Char('案主手機')
    relationship = fields.Char('聯絡人/關係')
    relate_phone = fields.Char('聯絡人電話')
    apply_method = fields.Text('申請管道')
    rec_int = fields.Text('資源整合查詢')
    Process_status = fields.Text('處理狀況')
    check_date = fields.Date('核發日期')
    visit_completed_date = fields.Date('訪視完成日期')
    pick_up_date = fields.Date('領件日期')
    apply_date = fields.Date('申請日期', default=datetime.date.today())
    visit_member = fields.Text('訪視志工人員')

    rec_zip = fields.Char(string='戶籍郵政區號',required = True)
    rec_addr = fields.Char(string='戶籍地址',required = True)
    mail_zip = fields.Char(string='通訊郵遞區號',required = True)
    mail_addr = fields.Char(string='通訊地址',required = True)
    IsApproved = fields.Boolean('是否核准')

    poor_images = fields.One2many(comodel_name='poor.image',inverse_name='case_code', string='案件影像資料')
    poor_receive = fields.One2many(comodel_name='poor.receive', inverse_name='case_code', string='案件領款時間')

    case_process = fields.Selection([(1, '訪視完成'), (2, '報告已送')], '案件進度')
    reward_method = fields.Selection([(1,'現金'),(2,'匯款')],'領款方式')

    #救助情形
    month = fields.Selection([(1, '1個月'), (2, '2個月'),(3, '3個月'),(4, '4個月'),(5, '5個月'),(6, '6個月')], '提領月數',required = True)
    allow_money = fields.Integer('申請總額',required = True)
    once_money = fields.Integer('單次金額')
    receive_money = fields.Integer('已領金額')


    @api.onchange('poor_receive')
    def compute_total_receive_money(self):

        self.receive_money = 0
        for data in self.poor_receive:
            self.receive_money += data.receive_money

        if (self.allow_money < self.receive_money):
            raise ValidationError(u"注意! 已領金額已超過申請總額")




    def print_case_photos(self):

       data = {
            'poor_images': self.poor_images.ids,
       }


       return self.env['report'].get_action([], 'cdg_base.receipt_case_images_template', data)


    @api.model
    def create(self, vals):
        res_id = super(PoorBase, self).create(vals)

        donate_date = datetime.date.today().strftime('%Y-%m-%d')

        historical_data_year = str(datetime.datetime.strptime(donate_date, '%Y-%m-%d').year) # 根據捐款日期取出捐款的年份
        historical_data_month = str(datetime.datetime.strptime(donate_date, '%Y-%m-%d').month) # 根據捐款日期取出捐款的月份
        datas = self.env['poor.statistics'].search([('year', '=', historical_data_year), ('month', '=', historical_data_month)])  # 搜尋計數器中有沒有資料

        if datas: # 如果有找到資料
            case_number = datas.case_number + 1
            res_id.write({
                'case_id': str(historical_data_year) + str(historical_data_month).zfill(2) + str(case_number).zfill(3)
            })
            datas.case_number = case_number # 捐款的收據張數寫回計數器
        else: # 如果沒有找到資料
            self.env['poor.statistics'].create({
                'year': historical_data_year,
                'month': historical_data_month,
                'case_number' : 1,
            })
            receipt_number = 1

            res_id.write({
                'case_id': str(historical_data_year) + str(historical_data_month).zfill(2) + str(receipt_number).zfill(3)
            })

        if res_id.name is False or res_id.self_iden is False:
            raise ValidationError('姓名或身分證號不能為空白')

        return res_id

