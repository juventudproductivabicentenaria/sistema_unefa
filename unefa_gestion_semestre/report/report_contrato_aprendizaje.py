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

class report_contrato_aprendizaje(report_sxw.rml_parse):
    def __init__(self , cr, uid, name, context):
        super(report_contrato_aprendizaje,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time':time,
            'get_data': self.get_data,
        })
        self.context = context
    
    def get_data(self):
        return 'hola mundo'

        
class report_contrato_aprendizaje_unefa(osv.AbstractModel):
    _name = "report.unefa_gestion_semestre.contrato_aprendizaje_qweb"
    _inherit = "report.abstract_report"
    _template = "unefa_gestion_semestre.contrato_aprendizaje_qweb"
    _wrapped_report_class = report_contrato_aprendizaje
# report_sxw.report_sxw('report.report_contrato_aprendizaje_unefa', 'unefa.gestion_semestre', 'local_addons_ep1561/unefa_gestion_semestre/report/report_contrato_aprendizaje.rml', parser=report_contrato_aprendizaje,header=False)




