# -*- coding: utf-8 -*-

import json
import logging
import base64
from cStringIO import StringIO

import os
import zipfile
from shutil import rmtree
from openerp.addons.web.controllers import main


import openerp.exceptions
from werkzeug.exceptions import HTTPException
from openerp import http,tools, api,SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_apiform.controladores import panel, base_tools
from datetime import datetime, date, time, timedelta


_logger = logging.getLogger(__name__)

class unefa_crear_cronograma_academico(http.Controller):
    

    @http.route(['/cronograma_recuperacion/descargar/<model("unefa.cronogramas_recuperacion"):cronograma_data>'],
                type='http', auth='user', website=True)
    def descargar_cronograma_academico(self,cronograma_data, **post):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        
        carrera_id= cronograma_data['carrera_id']
        turno= cronograma_data['turno']
        
        
        coordinacion_obj=registry('unefa.coordinacion')
        coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('regimen','=',turno)])
        coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_id)
        sede_data=coordinacion_data['sede_id']
        coordinador_obj=registry('unefa.usuario_coordinador')
        coordinador_id=coordinador_obj.search(cr,uid,[('coordinacion_id','=',coordinacion_id[0])])
        coordinador_data=coordinador_obj.browse(cr,uid,coordinador_id)
        
        reportname='unefa_cronograma_recuperacion.cronograma_recuperacion'
        nombre_zip='cronograma_recuperacion'+str(cronograma_data['periodo_id'].periodo_academico)+'.zip'
        if os.path.exists(nombre_zip):
            os.remove(nombre_zip)
        comp_zip = zipfile.ZipFile(nombre_zip, "w" ,zipfile.ZIP_STORED, allowZip64=True)
        con=1
        for cronograma in cronograma_data:
            for pensum in cronograma.pensum_ids:          
                con+=1
                valores={
                    'coordinacion_data':coordinacion_data,
                    'sede_data':sede_data,
                    'pensum_data':pensum,
                    'cronograma_data':cronograma_data,
                    }
                nombre_file='Cronograma_Academico_'+str(cronograma.periodo_id.periodo_academico)+'_'+str(pensum.pensum_id.pensum)+'.pdf'
                if os.path.exists(nombre_file):
                    os.remove(nombre_file)
                cronograma_reporte = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
                file_tmp = open(nombre_file, "wb",buffering = 0)
                file_tmp.write('¿'+str(con)+'?\n')
                file_tmp.write(cronograma_reporte)
                comp_zip.write(nombre_file)
                file_tmp.close()
                os.remove(nombre_file)
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

    
    
   
	
  
    
    
    
        
       
