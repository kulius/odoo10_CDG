# -*- coding: utf-8 -*-
####################################################
#  康虎云报表模板存储
#  该表中以Base64格式存储康虎云报表，可以方便地取
#  出来嵌入到康虎云报表打印数据(json)中
#
#
####################################################

import logging
import base64
from odoo import fields, models, api, http, _
from odoo.http import request
from cStringIO import StringIO
from werkzeug.utils import redirect

_logger = logging.getLogger(__name__)

def _get_cfprint_template(env, templ_id):
    """
    根据模板ID查询康虎云报表模板，如果不使用模板，可以qweb模板中使用：
    <t t-esc="user.env['cf.template'].search([('templ_id', '=', '12345')], limit=1).template" />
    取得模板
    :param env:         Env对象，在qweb模板中可以通过user.env或res_company.env取到
    :param templ_id:    模板唯一编号
    :return:
    """
    if (env is not None) and (templ_id is not None):
        templ = env['cf.template'].search([('templ_id', '=', templ_id)], limit=1)
        if len(templ)>0 :
            return templ.template.strip('\n')   #去掉Base64中的换行符然后返回

    #条件无效或无相符记录，则返回空字符串
    return ''

class Report(models.Model):
    """
    继承Report基类，增加自定义函数输出到QWeb模板中，方便在模板中便捷取康虎云报表模板
    """
    _inherit = "report"
    _description = "Report"

    @api.multi
    def render(self, template, values=None):
        """
        继承report对象的渲染方法，在上下文中增加模板对象ORM
        :param template:
        :param values:
        :return:
        """
        if values is None:
            values = {}

        cf_template = self.env['cf.template'].browse()
        values.update(
            cf_template=_get_cfprint_template       #把获取模板函数传入模板
        )

        obj = super(Report, self).render(template, values)
        return obj


class CFTemplate(models.Model):
    """
    康虎云报表模板模型类，通过该模型把康虎云报表保存在服务器数据库中，便于统一管理模板
    """
    _name = 'cf.template'
    _description = _(u"Report templates of CFPrint")

    templ_id = fields.Char(u'Template ID', required=True, help=u'Unique ID of template')
    name = fields.Char(u'Name', required=True)
    description = fields.Text(u'Description', required=False)
    preview_img = fields.Binary(u'Preview image', required=False, help=u'Picture used to preview a report')
    template = fields.Binary(u'Template', required=True, help=u'Content of template')

    _sql_constraints = [
        ('cons_cf_templ_id', 'unique(templ_id)', u'Template ID already exists!')
    ]