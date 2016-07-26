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

class ficha_profesor_general(http.Controller):
            
    @http.route(['/descargar/ficha_profesor/<model("unefa.usuario_profesor"):profesor_data>'],
                type='http', auth='user', website=True)
    def descargar_ficha_profesor(self,profesor_data, **post):
       
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        reportname='unefa_usuarios.ficha_profesores_qweb'
        
        carrera_id=profesor_data.carrera_id.id
        regimen=profesor_data.regimen
        
        coordinacion_obj=registry('unefa.coordinacion')
        coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('regimen','=',regimen)])
        coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_id)
        sede_data=coordinacion_data['sede_id']
        
                 
        valores={
            'profesor_data':profesor_data,
            'regimen':regimen,
            'sede_data':sede_data,
            'coordinacion_data':coordinacion_data,
            }
        nombre_archivo =profesor_data.nombre_completo+'_'+profesor_data.cedula
        pdf = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        response=request.make_response(pdf, headers=pdfhttpheaders)
        response.headers.add('Content-Disposition', 'attachment; filename='+nombre_archivo+'.pdf;')
        return response
  
