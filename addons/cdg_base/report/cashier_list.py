# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class CashierListXlsx(ReportXlsx):


    def generate_xlsx_report(self,workbook, datas, env):
        data_count = 1
        area = ""
        zip = 0
        count = 1


        donor_data = self.env['normal.p'].browse(datas['docs'])

        for data in donor_data:

            if zip != data.postal_code_id.zip:
                data_count = 1
                zip = data.postal_code_id.zip
                sheet = workbook.add_worksheet(zip + data.postal_code_id.city)
                sheet.write(0, 0,u'捐款者編號')
                sheet.write(0, 1, u'舊團員編號')
                sheet.write(0, 2, u'姓名')
                sheet.write(0, 3, u'連絡電話')
                sheet.write(0, 4, u'手機')
                sheet.write(0, 5, u'報表寄送地址')
            sheet.write(data_count, 0, data.new_coding)
            sheet.write(data_count, 1, data.w_id)
            sheet.write(data_count, 2, data.name)
            sheet.write(data_count, 3, data.con_phone)
            sheet.write(data_count, 4, data.cellphone)
            sheet.write(data_count, 5, data.zip_code + data.con_addr)
            data_count += 1

        # sheet1 = workbook.add_worksheet(u'中正區')
        # sheet2 = workbook.add_worksheet(u'大同區')
        # sheet3 = workbook.add_worksheet(u'中山區')
        # sheet4 = workbook.add_worksheet(u'松山區')
        # sheet5 = workbook.add_worksheet(u'大安區')
        # sheet6 = workbook.add_worksheet(u'萬華區')
        # sheet7 = workbook.add_worksheet(u'信義區')
        # sheet8 = workbook.add_worksheet(u'士林區')
        # sheet9 = workbook.add_worksheet(u'北投區')
        # sheet10 = workbook.add_worksheet(u'內湖區')
        # sheet11 = workbook.add_worksheet(u'南港區')
        # sheet12 = workbook.add_worksheet(u'文山區')
        #
        # sheet = [sheet1,sheet2,sheet3,sheet4,sheet5,sheet6,
        #          sheet7,sheet8,sheet9,sheet10,sheet11,sheet12]
        #
        # for record in sheet:
        #     record.write(0, 0,u'捐款者編號')
        #     record.write(0, 1, u'舊團員編號')
        #     record.write(0, 2, u'姓名')
        #     record.write(0, 3, u'連絡電話')
        #     record.write(0, 4, u'手機')
        #     record.write(0, 5, u'報表寄送地址')
        #
        #     record.set_column(0, 1, 12)
        #     record.set_column(3, 4, 12)
        #     record.set_column(5, 5, 40)
        #     record.set_column(6, 8, 4)
        #
        # for i in range(0,12):
        #     self.count.append(1)
        #
        #
        # for line in datas['docs']:
        #     data = self.env['normal.p'].browse(line)
        #     if data.zip == '100':
        #         sheet1.write(self.count[0], 0, data.new_coding)
        #         sheet1.write(self.count[0], 1, data.w_id)
        #         sheet1.write(self.count[0], 2, data.name)
        #         sheet1.write(self.count[0], 3, data.con_phone)
        #         sheet1.write(self.count[0], 4, data.cellphone)
        #         sheet1.write(self.count[0], 5, data.zip_code + data.con_addr)
        #         self.count[0] += 1
        #
        #     elif data.zip == '103':
        #         sheet2.write(self.count[1], 0, data.new_coding)
        #         sheet2.write(self.count[1], 1, data.w_id)
        #         sheet2.write(self.count[1], 2, data.name)
        #         sheet2.write(self.count[1], 3, data.con_phone)
        #         sheet2.write(self.count[1], 4, data.cellphone)
        #         sheet2.write(self.count[1], 5, data.zip_code + data.con_addr)
        #         self.count[1] = self.count[1] + 1
        #
        #     elif data.zip == '104':
        #         sheet3.write(self.count[2], 0, data.new_coding)
        #         sheet3.write(self.count[2], 1, data.w_id)
        #         sheet3.write(self.count[2], 2, data.name)
        #         sheet3.write(self.count[2], 3, data.con_phone)
        #         sheet3.write(self.count[2], 4, data.cellphone)
        #         sheet3.write(self.count[2], 5, data.zip_code + data.con_addr)
        #         self.count[2] += 1
        #     elif data.zip == '105':
        #         sheet4.write(self.count[3], 0, data.new_coding)
        #         sheet4.write(self.count[3], 1, data.w_id)
        #         sheet4.write(self.count[3], 2, data.name)
        #         sheet4.write(self.count[3], 3, data.con_phone)
        #         sheet4.write(self.count[3], 4, data.cellphone)
        #         sheet4.write(self.count[3], 5, data.zip_code + data.con_addr)
        #         self.count[3] += 1
        #
        #     elif data.zip == '106':
        #         sheet5.write(self.count[4], 0, data.new_coding)
        #         sheet5.write(self.count[4], 1, data.w_id)
        #         sheet5.write(self.count[4], 2, data.name)
        #         sheet5.write(self.count[4], 3, data.con_phone)
        #         sheet5.write(self.count[4], 4, data.cellphone)
        #         sheet5.write(self.count[4], 5, data.zip_code + data.con_addr)
        #         self.count[4] += 1
        #
        #     elif data.zip == '108':
        #         sheet6.write(self.count[5], 0, data.new_coding)
        #         sheet6.write(self.count[5], 1, data.w_id)
        #         sheet6.write(self.count[5], 2, data.name)
        #         sheet6.write(self.count[5], 3, data.con_phone)
        #         sheet6.write(self.count[5], 4, data.cellphone)
        #         sheet6.write(self.count[5], 5, data.zip_code + data.con_addr)
        #         self.count[5] += 1
        #
        #     elif data.zip == '110':
        #         sheet7.write(self.count[6], 0, data.new_coding)
        #         sheet7.write(self.count[6], 1, data.w_id)
        #         sheet7.write(self.count[6], 2, data.name)
        #         sheet7.write(self.count[6], 3, data.con_phone)
        #         sheet7.write(self.count[6], 4, data.cellphone)
        #         sheet7.write(self.count[6], 5, data.zip_code + data.con_addr)
        #         self.count[6] += 1
        #
        #     elif data.zip == '111':
        #         sheet8.write(self.count[7], 0, data.new_coding)
        #         sheet8.write(self.count[7], 1, data.w_id)
        #         sheet8.write(self.count[7], 2, data.name)
        #         sheet8.write(self.count[7], 3, data.con_phone)
        #         sheet8.write(self.count[7], 4, data.cellphone)
        #         sheet8.write(self.count[7], 5, data.zip_code + data.con_addr)
        #         self.count[7] += 1
        #
        #     elif data.zip == '112':
        #         sheet9.write(self.count[8], 0, data.new_coding)
        #         sheet9.write(self.count[8], 1, data.w_id)
        #         sheet9.write(self.count[8], 2, data.name)
        #         sheet9.write(self.count[8], 3, data.con_phone)
        #         sheet9.write(self.count[8], 4, data.cellphone)
        #         sheet9.write(self.count[8], 5, data.zip_code + data.con_addr)
        #         self.count[8] += 1
        #
        #     elif data.zip == '114':
        #         sheet10.write(self.count[9], 0, data.new_coding)
        #         sheet10.write(self.count[9], 1, data.w_id)
        #         sheet10.write(self.count[9], 2, data.name)
        #         sheet10.write(self.count[9], 3, data.con_phone)
        #         sheet10.write(self.count[9], 4, data.cellphone)
        #         sheet10.write(self.count[9], 5, data.zip_code + data.con_addr)
        #         self.count[9] += 1
        #
        #     elif data.zip == '115':
        #         sheet11.write(self.count[10], 0, data.new_coding)
        #         sheet11.write(self.count[10], 1, data.w_id)
        #         sheet11.write(self.count[10], 2, data.name)
        #         sheet11.write(self.count[10], 3, data.con_phone)
        #         sheet11.write(self.count[10], 4, data.cellphone)
        #         sheet11.write(self.count[10], 5, data.zip_code + data.con_addr)
        #         self.count[10] += 1
        #
        #     elif data.zip == '116':
        #         sheet12.write(self.count[11], 0, data.new_coding)
        #         sheet12.write(self.count[11], 1, data.w_id)
        #         sheet12.write(self.count[11], 2, data.name)
        #         sheet12.write(self.count[11], 3, data.con_phone)
        #         sheet12.write(self.count[11], 4, data.cellphone)
        #         sheet12.write(self.count[11], 5, data.zip_code + data.con_addr)
        #         self.count[11] += 1
        #
        #
        # self.count = []

        # 先創一個空白陣列用來增加新的sheet
        #
        # for 跑單筆資料
        #     if zip 不同於目前的zip
        #       用一個陣列來存區的名稱
        #       新加一個頁千



        #     if zip != data.zip:
        #         zip = data.zip
        #         sheet[] = workbook.add_worksheet(line[X].area)
        #
        #         sheet12.write(self.count[11], 0, data.new_coding)
        #         sheet12.write(self.count[11], 1, data.w_id)
        #         sheet12.write(self.count[11], 2, data.name)
        #         sheet12.write(self.count[11], 3, data.con_phone)
        #         sheet12.write(self.count[11], 4, data.cellphone)
        #         sheet12.write(self.count[11], 5, data.zip_code + data.con_addr)









CashierListXlsx('report.cdg_base.cashier_list.xlsx', 'normal.p')