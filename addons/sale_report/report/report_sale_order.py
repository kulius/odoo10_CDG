# _*_ coding: utf-8 _*_

from odoo import models, api


class ReportSaleOrder(models.AbstractModel):
    _name = 'report.sale_report.sale_order_report_custom'



    @api.multi
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env['sale.order'].browse(docids)

        docargs = {
            'doc_ids': docids,
            'doc_model': self.model,
            'docs': docs,
        }
        return self.env['report'].render('sale_report.sale_order_report_custom', values=docargs)
