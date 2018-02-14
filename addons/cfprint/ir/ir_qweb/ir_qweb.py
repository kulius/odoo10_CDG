# -*- coding: utf-8 -*-
import ast
from urlparse import urlparse
from lxml import html

#from .qweb import QWeb, Contextifier
#from .assetsbundle import AssetsBundle
from odoo.addons.base.ir.ir_qweb.qweb import QWeb, Contextifier, frozendict, QWebException
from odoo.addons.base.ir.ir_qweb.assetsbundle import AssetsBundle

from lxml import etree
from collections import OrderedDict

from odoo import api, models, tools
from odoo.tools.safe_eval import assert_valid_codeobj, _BUILTINS, _SAFE_OPCODES
from odoo.http import request
from odoo.modules.module import get_resource_path
import json
from time import time

import re

import logging
_logger = logging.getLogger(__name__)

unsafe_eval = eval


"""
HTML处理工具类
"""
class HTMLHelper:
    @staticmethod
    def filter_tags_re(htmlstr):
        """
        过滤HTML中的标签， 将HTML中标签等信息去掉
        使用示例：
        if __name__=='__main__':
            s=file('Google.htm').read()
            news=filter_tags(s)
            print news

        @param htmlstr HTML字符串.
        :return:
        """
        if not isinstance (htmlstr, str):
            return htmlstr;

        # 先过滤CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        ##blank_line = re.compile('\n+')
        # blank_line = re.compile('[ \n]+')
        # s = blank_line.sub('\n', s)
        # s = re.sub('[ \n]+', '', s)
        s = s.strip();
        s = HTMLHelper.replaceCharEntity(s)  # 替换实体
        return s

    @staticmethod
    def replaceCharEntity(htmlstr):
        """
        替换常用HTML字符实体.
        使用正常的字符替换HTML中特殊的字符实体.
        你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
        @param htmlstr HTML字符串.

        :return:
        """
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"',}

        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()  # entity全称，如&gt;
            key = sz.group('name')  # 去除&;后entity,如&gt;为gt
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                # 以空串代替
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

    @staticmethod
    def repalce(s, re_exp, repl_string):
        return re_exp.sub(repl_string, s)

    @staticmethod
    def strip_tags_parser(self, html):
        """
        去除文本中的HTML标签.用到了HTMLParser
        使用示例：
        str_text=strip_tags("<font color=red>hello</font>")

        :return: String
        """
        from HTMLParser import HTMLParser
        html = html.strip('\n')
        html = html.strip('\t')
        html = html.strip(' ')
        html = html.strip()

        result = []
        parser = HTMLParser()
        parser.handle_data = result.append
        parser.feed(html)
        parser.close()
        return '$'.join(result)

    @staticmethod
    def strip_tags_simple(self, html):
        """
        用正则表达式去除HTML
        :param html:
        :return:
        """
        return re.sub(r'</?\w+[^>]*>', '', html)

class IrQWebCF(models.AbstractModel, QWeb):
    """
    继承ir.qweb类，实现自定义属性的渲染输出
    """
    _name = 'ir.qweb'
    _inherit = 'ir.qweb'

    def _get_field(self, record, field_name, expression, tagName, field_options, options, values):
        """
        获取Field值
        :param record:
        :param field_name:
        :param expression:
        :param tagName:
        :param field_options:
        :param options:
        :param values:
        :return:
        """
        field = record._fields[field_name]

        field_options['tagName'] = tagName
        field_options['expression'] = expression
        field_options['type'] = field_options.get('widget', field.type)
        inherit_branding = options.get('inherit_branding',
                                       options.get('inherit_branding_auto') and record.check_access_rights('write', False))
        field_options['inherit_branding'] = inherit_branding
        translate = options.get('edit_translations') and options.get('translatable') and field.translate
        field_options['translate'] = translate

        # field converter
        model = 'ir.qweb.field.' + field_options['type']
        converter = self.env[model] if model in self.env else self.env['ir.qweb.field']

        # get content
        content = converter.record_to_html(record, field_name, field_options)
        attributes = converter.attributes(record, field_name, field_options, values)
        #TODO：可以在此把HTML标签去掉
        data_type = field_options.get('data_type')
        if data_type:
            if data_type == "raw" or data_type == "json":
                content = HTMLHelper.filter_tags_re(content)    #对于数据类型指定为raw或json，则去掉html标签

        return (attributes, content, inherit_branding or translate)

    @api.model
    def render(self, id_or_xml_id, values=None, **options):
        """
        render(id_or_xml_id, values, **options)

        解析并渲染页面模板.

        :param id_or_xml_id: name or etree (see get_template)
        :param dict values: template values to be used for rendering
        :param options: used to compile the template (the dict available for the rendering is frozen)
            * ``load`` (function) overrides the load method
            * ``profile`` (float) profile the rendering (use astor lib) (filter
              profile line with time ms >= profile)
        """
        for method in dir(self):
            if method.startswith('render_'):
                _logger.warning("Unused method '%s' is found in ir.qweb." % method)

        context = dict(self.env.context, dev_mode='qweb' in tools.config['dev_mode'])
        context.update(options)

        #根据t-field-options指定的数据类型，生成对应格式的数据
        if values and values.get("options"):
            data_type = values.get("options").get('data_type')
            if data_type == "raw":
                val = ""
                fields = values.get("fields")
                for field in fields:
                    if val != "":
                        val += ","
                    val += field + "=" +repr(values.get(field))
                return val
            elif data_type == "json":
                val = {}
                fields = values.get("fields")
                for field in fields:
                    val[field] = values.get(field)
                return json.dumps(val)
            else:
                return super(IrQWebCF, self).render(id_or_xml_id, values=values, **context)
        else:
            return super(IrQWebCF, self).render(id_or_xml_id, values=values, **context)

    def _compile_directive_field(self, el, options):
        '''
        取出t-field-options，并传递到HTML渲染界面
        :param el:          HTML元素
        :param options:     HTML渲染参数
        :return:
        '''
        field_options_str = el.attrib.get("t-field-options");
        if field_options_str:
            #解析字段属性串
            json_acceptable_string = field_options_str.replace("'", "\"")
            field_options = json.loads(json_acceptable_string)

            #判断字段属性中是否有指定数据类型，如果有指定，则把数据类型传到下一步处理
            data_type = field_options.get("data_type")
            if data_type:
                options["data_type"] = data_type

        return super(IrQWebCF, self)._compile_directive_field(el, options)

    def _compile_tag(self, el, content, options, attr_already_created=False):
        """
        把HTML元素插入AST 节点中。
        增强：如果渲染参数中指定了数据类型，并且数据类型为raw、json等值，则输出时不带HTML标签
        :param el:          HTML元素
        :param content:     HTML内容
        :param options:     渲染参数
        :param attr_already_created:
        :return:
        """

        if el.tag == 't':
            return content

        # body = [self._append(ast.Str(u'<%s' % el.tag))]
        # body.extend(self._compile_all_attributes(el, options, attr_already_created))
        # if el.tag in self._void_elements:
        #     body.append(self._append(ast.Str(u'/>')))
        #     body.extend(content)
        # else:
        #     body.append(self._append(ast.Str(u'>')))
        #     body.extend(content)
        #     body.append(self._append(ast.Str(u'</%s>' % el.tag)))

        #判断是否指定数据类型，如果指定并且是特定几种不需要输出HTML标签的，则直接输出内容
        data_type = options.get("data_type")
        is_show_tag = True      #是否显示HTML标签
        if data_type:
            if data_type == "raw" or data_type == "json":
                is_show_tag = False         #如果指定数据类型是raw或json，则不显示HTML标签

        body = [];
        if is_show_tag:     #如果是需要显示HTML标签，则按正常输出
            body.append(self._append(ast.Str(u'<%s' % el.tag)))
            body.extend(self._compile_all_attributes(el, options, attr_already_created))
            if el.tag in self._void_elements:
                body.append(self._append(ast.Str(u'/>')))
                body.extend(content)
            else:
                body.append(self._append(ast.Str(u'>')))
                body.extend(content)
                body.append(self._append(ast.Str(u'</%s>' % el.tag)))
        else:
            content = HTMLHelper.filter_tags_re(content)
            body.extend(content)        #如果不需要显示HTML，则只输出内容

        return body

############## Extende from qweb.py

    def render(self, template, values=None, **options):
        """ render(template, values, **options)

        Render the template specified by the given name.

        :param template: template identifier
        :param dict values: template values to be used for rendering
        :param options: used to compile the template (the dict available for the rendering is frozen)
            * ``load`` (function) overrides the load method
            * ``profile`` (float) profile the rendering (use astor lib) (filter
              profile line with time ms >= profile)
        """
        body = []
        self.compile(template, options)(self, body.append, values or {})
        return u''.join(body).encode('utf8')


    # def compile(self, template, options):
    #     """ Compile the given template into a rendering function::
    #
    #         render(qweb, append, values)
    #
    #     where ``qweb`` is a QWeb instance, ``append`` is a unary function to
    #     collect strings into a result, and ``values`` are the values to render.
    #     """
    #     if options is None:
    #         options = {}
    #
    #     _options = dict(options)
    #     options = frozendict(options)
    #
    #     element, document = self.get_template(template, options)
    #     name = element.get('t-name', 'unknown')
    #
    #     _options['template'] = template
    #     _options['ast_calls'] = []
    #     _options['root'] = element.getroottree()
    #     _options['last_path_node'] = None
    #
    #     # generate ast
    #
    #     astmod = self._base_module()
    #     try:
    #         body = self._compile_node(element, _options)
    #         ast_calls = _options['ast_calls']
    #         _options['ast_calls'] = []
    #         def_name = self._create_def(_options, body, prefix='template_%s' % name.replace('.', '_'))
    #         _options['ast_calls'] += ast_calls
    #     except QWebException, e:
    #         raise e
    #     except Exception, e:
    #         path = _options['last_path_node']
    #         node = element.getroottree().xpath(path)
    #         raise QWebException("Error when compiling AST", e, path, etree.tostring(node[0]), name)
    #     astmod.body.extend(_options['ast_calls'])
    #
    #     if 'profile' in options:
    #         self._profiling(astmod, _options)
    #
    #     ast.fix_missing_locations(astmod)
    #
    #     # compile ast
    #
    #     try:
    #         # noinspection PyBroadException
    #         ns = {}
    #         unsafe_eval(compile(astmod, '<template>', 'exec'), ns)
    #         compiled = ns[def_name]
    #     except QWebException, e:
    #         raise e
    #     except Exception, e:
    #         path = _options['last_path_node']
    #         node = element.getroottree().xpath(path)
    #         raise QWebException("Error when compiling AST", e, path, node and etree.tostring(node[0]), name)
    #
    #     # return the wrapped function
    #
    #     def _compiled_fn(self, append, values):
    #         log = {'last_path_node': None}
    #         values = dict(self.default_values(), **values)
    #         try:
    #             return compiled(self, append, values, options, log)
    #         except QWebException, e:
    #             raise e
    #         except Exception, e:
    #             path = log['last_path_node']
    #             element, document = self.get_template(template, options)
    #             node = element.getroottree().xpath(path)
    #             raise QWebException("Error to render compiling AST", e, path, node and etree.tostring(node[0]), name)
    #
    #     return _compiled_fn
    #
    #
    # def default_values(self):
    #     """ Return attributes added to the values for each computed template. """
    #     return dict(format=self.format)
    #
    #
    # def get_template(self, template, options):
    #     """ Retrieve the given template, and return it as a pair ``(element,
    #     document)``, where ``element`` is an etree, and ``document`` is the
    #     string document that contains ``element``.
    #     """
    #     if isinstance(template, etree._Element):
    #         document = template
    #         template = etree.tostring(template)
    #         return (document, template)
    #     else:
    #         try:
    #             document = options.get('load', self.load)(template, options)
    #         except QWebException, e:
    #             raise e
    #         except Exception, e:
    #             raise QWebException("load could not load template", name=template)
    #
    #     if document is not None:
    #         if isinstance(document, etree._Element):
    #             element = document
    #             document = etree.tostring(document)
    #         elif document.startswith("<?xml"):
    #             element = etree.fromstring(document)
    #         else:
    #             element = etree.parse(document).getroot()
    #         for node in element:
    #             if node.get('t-name') == str(template):
    #                 return (node, document)
    #
    #     raise QWebException("Template not found", name=template)
    #
    #
    # def load(self, template, options):
    #     """ Load a given template. """
    #     return template


    # def render_tag_usertime(self, element, template_attributes, generated_attributes, qwebcontext):
    #     tformat = template_attributes['usertime']
    #     if not tformat:
    #         # No format, use default time and date formats from qwebcontext
    #         lang = (
    #             qwebcontext['env'].lang or
    #             qwebcontext['env'].context['lang'] or
    #             qwebcontext['user'].lang
    #         )
    #         if lang:
    #             lang = qwebcontext['env']['res.lang'].search(
    #                 [('code', '=', lang)]
    #             )
    #             tformat = "{0.date_format} {0.time_format}".format(lang)
    #         else:
    #             tformat = DEFAULT_SERVER_DATETIME_FORMAT
    #
    #     now = datetime.now()
    #
    #     tz_name = qwebcontext['user'].tz
    #     if tz_name:
    #         try:
    #             utc = pytz.timezone('UTC')
    #             context_tz = pytz.timezone(tz_name)
    #             utc_timestamp = utc.localize(now, is_dst=False)  # UTC = no DST
    #             now = utc_timestamp.astimezone(context_tz)
    #         except Exception:
    #             _logger.debug(
    #                 "failed to compute context/client-specific timestamp, "
    #                 "using the UTC value",
    #                 exc_info=True)
    #     return now.strftime(tformat)