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

class report_acta_notas(report_sxw.rml_parse):
    def __init__(self , cr, uid, name, context):
        super(report_acta_notas,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time':time,
            'get_data': self.get_data,
        })
        self.context = context
    
    def get_data(self):
        return 'hola mundo'

        
class report_acta_notas_unefa(osv.AbstractModel):
    _name = "report.unefa_gestion_semestre.acta_notas_qweb"
    _inherit = "report.abstract_report"
    _template = "unefa_gestion_semestre.acta_notas_qweb"
    _wrapped_report_class = report_acta_notas
# report_sxw.report_sxw('report.report_acta_notas_unefa', 'unefa.gestion_semestre', 'local_addons_ep1561/unefa_gestion_semestre/report/report_acta_notas.rml', parser=report_acta_notas_unefa,header=False)




