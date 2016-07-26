# -*- coding: utf-8 -*-
##############################################################################
#
#    Programa realizado por, Jeison Pernía y Jonathan Reyes en el marco
#    del plan de estudios de la UNEFA, como TRABAJO ESPECIAL DE GRADO,
#    con el fin de optar al título de Ingeniero de Sistemas.
#    
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com
#
##############################################################################

from openerp.osv import osv
import time
from openerp.report import report_sxw

class oferta_academica(report_sxw.rml_parse):
    def __init__(self , cr, uid, name, context):
        super(oferta_academica,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time':time,
            'get_data': self.get_data,
        })
        self.context = context
    
    def get_data(self):
        return 'hola mundo'

        
class report_oferta_academica(osv.AbstractModel):
    _name = "report.unefa_oferta_academica.oferta_academica_qweb"
    _inherit = "report.abstract_report"
    _template = "unefa_oferta_academica.oferta_academica_qweb"
    _wrapped_report_class = oferta_academica
# report_sxw.report_sxw('report.report_oferta_academica', 'unefa.oferta_academica', 'local_addons_ep1561/unefa_oferta_academica/report/report_oferta_academica.rml', parser=oferta_academica,header=False)




