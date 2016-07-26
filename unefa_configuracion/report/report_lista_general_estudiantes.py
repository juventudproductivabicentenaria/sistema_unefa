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

class lista_general_estudiantes(report_sxw.rml_parse):
    def __init__(self , cr, uid, name, context):
        super(lista_general_estudiantes,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time':time,
            'get_data': self.get_data,
        })
        self.context = context
    
    def get_data(self):
        return 'hola mundo'

        
class report_lista_general_estudiantes(osv.AbstractModel):
    _name = "report.unefa_configuracion.lista_generales_estudiantes_qweb"
    _inherit = "report.abstract_report"
    _template = "unefa_configuracion.lista_generales_estudiantes_qweb"
    _wrapped_report_class = lista_general_estudiantes
# report_sxw.report_sxw('report.report_lista_general_estudiantes', 'unefa.coordinacion', 'local_addons_ep1561/unefa_configuracion/report/report_lista_general_estudiantes.rml', parser=lista_general_estudiantes,header=False)




