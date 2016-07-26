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

class listas_generales_estudiantes(http.Controller):
            
    @http.route(['/descargar/historial_notas/<model("unefa.usuario_estudiante"):estudiante_data>'],
                type='http', auth='user', website=True)
    def descargar_lista_general_estudiante(self,estudiante_data, **post):
       
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        reportname='unefa_usuarios.historial_notas_qweb'
        
        carrera_id=estudiante_data['carrera_id']['id']
        turno=estudiante_data['regimen']
        pensum_id=estudiante_data['pensum_id']['id']
        estudiante_id=estudiante_data['id']
        gestion_obj=registry('unefa.gestion_semestre')
        
        vals={}
        coordinacion_obj=registry('unefa.coordinacion')
        coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('regimen','=',turno)])
        coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_id)
        sede_data=coordinacion_data['sede_id']
        
        inscripcion_obj=registry('unefa.inscripcion_asignatura')
        inscripcion_id=inscripcion_obj.search(cr,uid,[('user_id','=',int(estudiante_data['id']))],order='id')
        inscripcion_data=inscripcion_obj.browse(cr,uid,inscripcion_id)
        list_nota_asignatura=[]
        for inscripcion in inscripcion_data:
            for asignatura in inscripcion.asignaturas_inscritas_ids:
                gestion_id=gestion_obj.search(cr,uid,[('asignatura_id','=',asignatura.asignatura_id.id),('periodo_id','=',inscripcion.periodo_id.id),
                                            ('carrera_id','=',carrera_id),('turno','=',turno)])
                gestion_data=gestion_obj.browse(cr,uid,gestion_id)
                for gestion in gestion_data:
                    for acta in gestion.actas_ids:
                        if acta.pensum_id.id==pensum_id:
                            for nota in acta.notas_ids:
                                if nota.estudiante_id.id==estudiante_id:
                                    vals['asignatura']=asignatura.asignatura_id.asignatura
                                    vals['definitiva']=int(nota.definitiva)
                                    if int(nota.definitiva)<10:
                                        for actar in gestion.actas_recuperacion_ids:
                                            if actar.pensum_id.id==pensum_id:
                                                for notar in actar.notas_ids:
                                                    if notar.estudiante_id.id==estudiante_id:
                                                        vals['asignaturar']=asignatura.asignatura_id.asignatura
                                                        vals['calificacion']=notar.calificacion
                                    list_nota_asignatura.append(vals)
                                    
                    
        
        hoy=date.today()
            
        valores={
            'coordinacion_data':coordinacion_data,
            'sede_data':sede_data,
            'estudiante_data':estudiante_data,
            'hoy':hoy,
            'list_nota_asignatura':list_nota_asignatura,
            }
        
        pdf = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        response=request.make_response(pdf, headers=pdfhttpheaders)
        response.headers.add('Content-Disposition', 'attachment; filename=Historial_notas_.pdf;')
        return response
  
