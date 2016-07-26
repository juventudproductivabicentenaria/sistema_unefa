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

import os
import zipfile
from shutil import rmtree

import openerp.exceptions
from werkzeug.exceptions import HTTPException
from openerp import http,tools, api,SUPERUSER_ID
from openerp.http import request
#~ from openerp.addons.website_apiform.controladores import panel, base_tools
from datetime import datetime, date, time, timedelta
from openerp.addons.web.controllers import main

#~ from openerp.addons.ept_rendicion.controladores import ept_rnd_rendicion_c
_logger = logging.getLogger(__name__)

class oferta_academicas(http.Controller):
    

    @http.route(['/descargar/oferta_academica/<model("unefa.oferta_academica"):oferta_data>'],
                type='http', auth='user', website=True)
    def descargar_oferta_academica(self,oferta_data, **post):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        
        carrera_id= oferta_data['carrera_id']
        turno= oferta_data['turno']
        
        
        coordinacion_obj=registry('unefa.coordinacion')
        coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('regimen','=',turno)])
        coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_id)
        sede_data=coordinacion_data['sede_id']
        coordinador_obj=registry('unefa.usuario_coordinador')
        coordinador_id=coordinador_obj.search(cr,uid,[('coordinacion_id','=',coordinacion_id[0])])
        coordinador_data=coordinador_obj.browse(cr,uid,coordinador_id)
        
        reportname='unefa_oferta_academica.oferta_academica_qweb'
        nombre_zip='oferta_academica_'+str(oferta_data['periodo_id'].periodo_academico)+'.zip'
        if os.path.exists(nombre_zip):
            os.remove(nombre_zip)
        comp_zip = zipfile.ZipFile(nombre_zip, "w" ,zipfile.ZIP_STORED, allowZip64=True)
        con=1
        folio=1
        for oferta in oferta_data:
            for pensum in oferta.pensum_ids:
                for semestre in pensum.semestres_ids:
                
                    for seccion in semestre.secciones_ids:
                        
                        con+=1
                        valores={
                            'oferta':oferta,
                            'pensum':str(pensum.pensum_id.pensum),
                            'semestre':semestre,
                            'seccion':seccion,
                            'coordinador':coordinador_data['nombre_completo'],
                            'cedula_coordinador':coordinador_data['cedula'],
                            'folio':folio,
                            'sede_data':sede_data,
                            }
                        nombre_file='Oferta_academica_'+str(oferta.periodo_id.periodo_academico)+'_'+str(pensum.pensum_id.pensum)+'_'+str(semestre.semestre_id.semestre)+'_'+str(seccion.seccion)+'.pdf'
                        if os.path.exists(nombre_file):
                            os.remove(nombre_file)
                        oferta_reporte = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
                        file_tmp = open(nombre_file, "wb",buffering = 0)
                        file_tmp.write('¿'+str(con)+'?\n')
                        file_tmp.write(oferta_reporte)
                        comp_zip.write(nombre_file)
                        file_tmp.close()
                        os.remove(nombre_file)
                        folio+=1
        comp_zip.close()
        reomover_zip = open(nombre_zip, "r")
        data_zip=reomover_zip.read()
        reomover_zip.close()
        os.remove(nombre_zip)
        return request.make_response(data_zip,
                headers=[('Content-Disposition',
                                main.content_disposition(nombre_zip)),
                         ('Content-Type', 'application/zip;charset=utf8'),
                         ('Content-Length', len(data_zip))],
                cookies={'fileToken': '212123f4646546'})
