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

import json
import logging
import base64
from cStringIO import StringIO

import openerp.exceptions
from werkzeug.exceptions import HTTPException
from openerp import http,tools, api,SUPERUSER_ID
from openerp.http import request
#~ from openerp.addons.website_apiform.controladores import panel, base_tools
from datetime import datetime, date, time, timedelta

#~ from openerp.addons.ept_rendicion.controladores import ept_rnd_rendicion_c
_logger = logging.getLogger(__name__)

class planilla_inscripcion_asignatura(http.Controller):
            
    @http.route(['/descargar/planilla_inscripcion/<model("unefa.inscripcion_asignatura"):inscripcion_data>'],
                type='http', auth='user', website=True)
    def descargar_planilla_inscripcion(self,inscripcion_data, **post):
       
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        reportname='unefa_inscripcion.planilla_inscripcion_qweb'
        
        carrera_id = inscripcion_data.user_id.carrera_id.id
        regimen = inscripcion_data.user_id.regimen
        coordinacion_obj=registry('unefa.coordinacion')
        coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('regimen','=',regimen)])
        coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_id)
        
    
        coordinador_obj=registry('unefa.usuario_coordinador')
        coordinador_id=coordinador_obj.search(cr,uid,[('coordinacion_id','=',coordinacion_id[0])])
        coordinador_data=coordinador_obj.browse(cr,uid,coordinador_id)
        
        
        sede_data=coordinacion_data['sede_id']
        valores={
            'inscripcion_data':inscripcion_data,
            'regimen':regimen,
            'sede_data':sede_data,
            'coordinacion_data':coordinacion_data,
            'coordinador_data':coordinador_data,
            }
        nombre_archivo =inscripcion_data.user_id.nombre_completo+'_'+inscripcion_data.user_id.cedula
        pdf = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        response=request.make_response(pdf, headers=pdfhttpheaders)
        response.headers.add('Content-Disposition', 'attachment; filename='+nombre_archivo+'.pdf;')
        return response
  
