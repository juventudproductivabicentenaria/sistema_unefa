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

class unefa_gestionar_semestre(http.Controller):
    
    
    @http.route(['/descargar/listas_estudiantes/<int:id_gestion_semestre>'],
                type='http', auth='user', website=True)
    def descargar_lista_estudiantes(self,id_gestion_semestre,**post):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        reportname='unefa_gestion_semestre.listas_estudiantes_qweb'
        
        gestion_semestre_obj=registry('unefa.gestion_semestre')
        gestion_semestre_data=gestion_semestre_obj.browse(cr,uid,int(id_gestion_semestre))
        
        asignaturas_inscritas_total_ids=[]
        list_estudiantes_ids=[]

        asignaturas_inscritas_obj=registry('unefa.asignatura_inscritas')
        asignaturas_inscritas_ids=asignaturas_inscritas_obj.search(cr,uid,[('asignatura_id','=',gestion_semestre_data['asignatura_id']['id']),('seccion_id','=',gestion_semestre_data['seccion_id']['id']),('inscripcion_especial','=',False)])
        asignaturas_inscritas_especial_ids=asignaturas_inscritas_obj.search(cr,uid,[('asignatura_relacion_id','=',gestion_semestre_data['asignatura_id']['id']),('seccion_id','=',gestion_semestre_data['seccion_id']['id']),('inscripcion_especial','=',True)])
        asignaturas_inscritas_total_ids=list(set(asignaturas_inscritas_ids) | set(asignaturas_inscritas_especial_ids))
        asignaturas_inscritas_data=asignaturas_inscritas_obj.browse(cr,uid,asignaturas_inscritas_total_ids)
        for asignatura in asignaturas_inscritas_data:
            list_estudiantes_ids.append(asignatura.inscripcion_id.user_id.id)
       
        usuario_estudiante_obj=registry('unefa.usuario_estudiante')
        estudiantes_ids=usuario_estudiante_obj.search(cr,uid,[('id','in',list_estudiantes_ids)],order='primer_apellido')
        usuario_estudiante_data=usuario_estudiante_obj.browse(cr,uid,estudiantes_ids)
        carrera_id = gestion_semestre_data['carrera_id']
        regimen = gestion_semestre_data['turno']
        coordinacion_obj=registry('unefa.coordinacion')
        coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('regimen','=',regimen)])
        coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_id)
        sede_data=coordinacion_data['sede_id']
        valores={
            'regimen':regimen,
            'sede_data':sede_data,
            'coordinacion_data':coordinacion_data,
            'gestion_semestre_data':gestion_semestre_data,
            'usuario_estudiante_data':usuario_estudiante_data,
            }
        pdf = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        response=request.make_response(pdf, headers=pdfhttpheaders)
        response.headers.add('Content-Disposition', 'attachment; filename=Lista_Estudiantes_'+gestion_semestre_data['asignatura_id']['asignatura']+'_'+gestion_semestre_data['seccion_id']['seccion']+'_'+gestion_semestre_data['periodo_id']['periodo_academico']+'_.pdf;')
        return response
    
    
    
    @http.route(['/descargar/contrato_aprendizaje/<int:id_gestion_semestre>'],
                type='http', auth='user', website=True)
    def descargar_contrato_aprendizaje(self,id_gestion_semestre,**post):
        
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        reportname='unefa_gestion_semestre.contrato_aprendizaje_qweb'
        
        gestion_semestre_obj=registry('unefa.gestion_semestre')
        gestion_semestre_data=gestion_semestre_obj.browse(cr,uid,int(id_gestion_semestre))
        
        asignaturas_inscritas_total_ids=[]
        list_estudiantes_ids=[]

        asignaturas_inscritas_obj=registry('unefa.asignatura_inscritas')
        asignaturas_inscritas_ids=asignaturas_inscritas_obj.search(cr,uid,[('asignatura_id','=',gestion_semestre_data['asignatura_id']['id']),('seccion_id','=',gestion_semestre_data['seccion_id']['id']),('inscripcion_especial','=',False)])
        asignaturas_inscritas_especial_ids=asignaturas_inscritas_obj.search(cr,uid,[('asignatura_relacion_id','=',gestion_semestre_data['asignatura_id']['id']),('seccion_id','=',gestion_semestre_data['seccion_id']['id']),('inscripcion_especial','=',True)])
        asignaturas_inscritas_total_ids=list(set(asignaturas_inscritas_ids) | set(asignaturas_inscritas_especial_ids))
        asignaturas_inscritas_data=asignaturas_inscritas_obj.browse(cr,uid,asignaturas_inscritas_total_ids)
        
        
        
        
        for asignatura in asignaturas_inscritas_data:
            list_estudiantes_ids.append(asignatura.inscripcion_id.user_id.id)
       
        usuario_estudiante_obj=registry('unefa.usuario_estudiante')
        estudiantes_ids=usuario_estudiante_obj.search(cr,uid,[('id','in',list_estudiantes_ids)],order='primer_apellido')
        usuario_estudiante_data=usuario_estudiante_obj.browse(cr,uid,estudiantes_ids)
        carrera_id = gestion_semestre_data['carrera_id']
        regimen = gestion_semestre_data['turno']
        coordinacion_obj=registry('unefa.coordinacion')
        coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('regimen','=',regimen)])
        coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_id)
        sede_data=coordinacion_data['sede_id']
        
        horario_seccion_obj=registry('unefa.horarios_seccion')
        horario_seccion_id=horario_seccion_obj.search(cr,uid,[('seccion_id','=',gestion_semestre_data['seccion_id']['id'])])
        horario_seccion_data=horario_seccion_obj.browse(cr,uid,horario_seccion_id)
        
        coordinador_obj=registry('unefa.usuario_coordinador')
        coordinador_id=coordinador_obj.search(cr,uid,[('coordinacion_id','=',coordinacion_id[0])])
        coordinador_data=coordinador_obj.browse(cr,uid,coordinador_id)

        formato_mes = "%B" 
        formato_anio = "%Y" 
        hoy = datetime.today()
        mes = hoy.strftime(formato_mes)
        anio = hoy.strftime(formato_anio)
        valores={
            'regimen':regimen,
            'sede_data':sede_data,
            'coordinacion_data':coordinacion_data,
            'gestion_semestre_data':gestion_semestre_data,
            'usuario_estudiante_data':usuario_estudiante_data,
            'horario_seccion_data':horario_seccion_data,
            'coordinador_data':coordinador_data,
            'mes':mes,
            'anio':anio,
            }


        pdf = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        response=request.make_response(pdf, headers=pdfhttpheaders)
        response.headers.add('Content-Disposition', 'attachment; filename=Contrato_aprendizaje_'+gestion_semestre_data['asignatura_id']['asignatura']+'_'+gestion_semestre_data['seccion_id']['seccion']+'_'+gestion_semestre_data['periodo_id']['periodo_academico']+'_.pdf;')
        return response
        
        
    @http.route(['/descargar/plan_evaluacion/<int:id_gestion_semestre>'],
                type='http', auth='user', website=True)
    def descargar_plan_evaluacion(self,id_gestion_semestre,**post):
        
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        reportname='unefa_gestion_semestre.plan_evaluacion_qweb'
        
        gestion_semestre_obj=registry('unefa.gestion_semestre')
        gestion_semestre_data=gestion_semestre_obj.browse(cr,uid,int(id_gestion_semestre))
        
       
        
        
        asignaturas_inscritas_total_ids=[]
        list_estudiantes_ids=[]

        asignaturas_inscritas_obj=registry('unefa.asignatura_inscritas')
        asignaturas_inscritas_ids=asignaturas_inscritas_obj.search(cr,uid,[('asignatura_id','=',gestion_semestre_data['asignatura_id']['id']),('seccion_id','=',gestion_semestre_data['seccion_id']['id'])])
        asignaturas_inscritas_especial_ids=asignaturas_inscritas_obj.search(cr,uid,[('asignatura_relacion_id','=',gestion_semestre_data['asignatura_id']['id']),('seccion_id','=',gestion_semestre_data['seccion_id']['id'])])
        asignaturas_inscritas_total_ids=list(set(asignaturas_inscritas_ids) | set(asignaturas_inscritas_especial_ids))
        asignaturas_inscritas_data=asignaturas_inscritas_obj.browse(cr,uid,asignaturas_inscritas_total_ids)
        
        
        
        
        for asignatura in asignaturas_inscritas_data:
            list_estudiantes_ids.append(asignatura.inscripcion_id.user_id.id)
        
        horario_seccion_obj=registry('unefa.horarios_seccion')
        horario_seccion_id=horario_seccion_obj.search(cr,uid,[('seccion_id','=',gestion_semestre_data['seccion_id']['id'])])
        horario_seccion_data=horario_seccion_obj.browse(cr,uid,horario_seccion_id)
        
        estudiante=len(list_estudiantes_ids)
        
        carrera_id = gestion_semestre_data['carrera_id']
        regimen = gestion_semestre_data['turno']
        coordinacion_obj=registry('unefa.coordinacion')
        coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('regimen','=',regimen)])
        coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_id)
        sede_data=coordinacion_data['sede_id']
        
        
        
        coordinador_obj=registry('unefa.usuario_coordinador')
        coordinador_id=coordinador_obj.search(cr,uid,[('coordinacion_id','=',coordinacion_id[0])])
        coordinador_data=coordinador_obj.browse(cr,uid,coordinador_id)

       
        valores={
            'regimen':regimen,
            'sede_data':sede_data,
            'coordinacion_data':coordinacion_data,
            'gestion_semestre_data':gestion_semestre_data,
            'horario_seccion_data':horario_seccion_data,
            'coordinador_data':coordinador_data,
            'estudiante':estudiante,
            }

        
        pdf = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        response=request.make_response(pdf, headers=pdfhttpheaders)
        response.headers.add('Content-Disposition', 'attachment; filename=Plan_evaluacion_'+gestion_semestre_data['asignatura_id']['asignatura']+'_'+gestion_semestre_data['seccion_id']['seccion']+'_'+gestion_semestre_data['periodo_id']['periodo_academico']+'_.pdf;')
        return response
    
    @http.route(['/actas/crear/<model("unefa.acta_notas_pensum"):acta_data>'],
                                            type='http', auth='user', website=True)
    def crear_actas_notas(self,acta_data):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        if acta_data['creado']!=True:
            if uid==acta_data['gestion_semestre_id']['profesor_id']['id']:
                inscripcion_obj=registry('unefa.inscripcion_asignatura')
                inscripcion_asignatura_obj=registry('unefa.asignatura_inscritas')
                estudiante_obj=registry('unefa.usuario_estudiante')
                inscripcion_id=inscripcion_obj.search(cr,uid,[('periodo_id','=',acta_data['gestion_semestre_id']['periodo_id']['id']),('state','in',['inscrito'])])
                inscripcion_data=inscripcion_obj.browse(cr,uid,inscripcion_id)
                list_inscripcion_ids=[]
                list_estudiantes_ids=[]
                for inscripcion in inscripcion_data:
                    if inscripcion.user_id.pensum_id.id==acta_data['pensum_id']['id']:
                        list_inscripcion_ids.append(inscripcion.id)
                inscripcion_asignatura_id=inscripcion_asignatura_obj.search(cr,uid,
                                                [('inscripcion_id','in',list_inscripcion_ids),
                                                ('asignatura_id','=',acta_data['gestion_semestre_id']['asignatura_id']['id']),
                                                ('seccion_id','=',acta_data['gestion_semestre_id']['seccion_id']['id']),
                                                ('inscripcion_especial','=',False)])
                inscripcion_especial_asignatura_id=inscripcion_asignatura_obj.search(cr,uid,
                                                [('inscripcion_id','in',list_inscripcion_ids),
                                                ('asignatura_relacion_id','=',acta_data['gestion_semestre_id']['asignatura_id']['id']),
                                                ('seccion_id','=',acta_data['gestion_semestre_id']['seccion_id']['id']),
                                                ('inscripcion_especial','=',True)])
                asignaturas_inscritas_total_ids=list(set(inscripcion_asignatura_id) | set(inscripcion_especial_asignatura_id))
                inscripcion_asignatura_data=inscripcion_asignatura_obj.browse(cr,uid,asignaturas_inscritas_total_ids)
                for ins_asig in inscripcion_asignatura_data:
                    list_estudiantes_ids.append(ins_asig.inscripcion_id.user_id.id)
                estudiantes_ids=estudiante_obj.search(cr,uid,[('id','in',list_estudiantes_ids)],order='primer_apellido')
                usuario_estudiante_data=estudiante_obj.browse(cr,uid,estudiantes_ids)
                datos={'parametros':{
                            'titulo':'Actas de Notas',
                            'template':'unefa_gestion_semestre.crear_acta_notas',
                            'url_boton_list':'',
                            'css':'info',
                            'id_form':'formcrearactasnotas',
                            'id_enviar':'enviar_acta_notas',
                            'action':'/actas/guardar',
                            },
                            'acta_data':acta_data,
                            'usuario_estudiante_data':usuario_estudiante_data,
                            }
                return panel.panel_post(datos)
            else:
                mensaje_usuario={
                    'titulo':'Aviso!',
                    'mensaje':'Usted no tiene permiso para acceder a estos registros',
                    'volver':'/'
                    }
                return http.request.website.render('website_apiform.mensaje', mensaje_usuario)    
        else:
            mensaje_usuario={
                'titulo':'Aviso!',
                'mensaje':'Ya ha sido creado un registro de acta de notas para esta asignatura',
                'volver':'/'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje_usuario)
    
    
    @http.route(['/actas/editar/<model("unefa.acta_notas_pensum"):acta_data>'],
                                            type='http', auth='user', website=True)
    def editar_actas_notas(self,acta_data):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        if uid==acta_data['gestion_semestre_id']['profesor_id']['id']:
            if acta_data['gestion_semestre_id']['acta_aprobada']==False:
                inscripcion_obj=registry('unefa.inscripcion_asignatura')
                inscripcion_asignatura_obj=registry('unefa.asignatura_inscritas')
                estudiante_obj=registry('unefa.usuario_estudiante')
                inscripcion_id=inscripcion_obj.search(cr,uid,[('periodo_id','=',acta_data['gestion_semestre_id']['periodo_id']['id']),('state','in',['inscrito'])])
                inscripcion_data=inscripcion_obj.browse(cr,uid,inscripcion_id)
                list_inscripcion_ids=[]
                list_estudiantes_ids=[]
                for inscripcion in inscripcion_data:
                    if inscripcion.user_id.pensum_id.id==acta_data['pensum_id']['id']:
                        list_inscripcion_ids.append(inscripcion.id)
                inscripcion_asignatura_id=inscripcion_asignatura_obj.search(cr,uid,
                                                [('inscripcion_id','in',list_inscripcion_ids),
                                                ('asignatura_id','=',acta_data['gestion_semestre_id']['asignatura_id']['id']),
                                                ('seccion_id','=',acta_data['gestion_semestre_id']['seccion_id']['id']),
                                                ('inscripcion_especial','=',False)])
                inscripcion_especial_asignatura_id=inscripcion_asignatura_obj.search(cr,uid,
                                                [('inscripcion_id','in',list_inscripcion_ids),
                                                ('asignatura_relacion_id','=',acta_data['gestion_semestre_id']['asignatura_id']['id']),
                                                ('seccion_id','=',acta_data['gestion_semestre_id']['seccion_id']['id']),
                                                ('inscripcion_especial','=',True)])
                asignaturas_inscritas_total_ids=list(set(inscripcion_asignatura_id) | set(inscripcion_especial_asignatura_id))
                inscripcion_asignatura_data=inscripcion_asignatura_obj.browse(cr,uid,asignaturas_inscritas_total_ids)
                for ins_asig in inscripcion_asignatura_data:
                    list_estudiantes_ids.append(ins_asig.inscripcion_id.user_id.id)
                estudiantes_ids=estudiante_obj.search(cr,uid,[('id','in',list_estudiantes_ids)],order='primer_apellido')
                usuario_estudiante_data=estudiante_obj.browse(cr,uid,estudiantes_ids)
                lista_estudiantes=[]
                for acta in acta_data:
                    for estudiantes in acta.notas_ids:
                        lista_estudiantes.append(estudiantes.estudiante_id.id)
                datos={'parametros':{
                            'titulo':'Actas de Notas',
                            'template':'unefa_gestion_semestre.editar_acta_notas',
                            'url_boton_list':'',
                            'css':'info',
                            'id_form':'formeditaractasnotas',
                            'id_enviar':'editar_acta_notas',
                            'action':'/actas/editar',
                            },
                            'acta_data':acta_data,
                            'usuario_estudiante_data':usuario_estudiante_data,
                            'lista_estudiantes':lista_estudiantes,
                            }
                return panel.panel_post(datos)
            else:
                mensaje_usuario={
                        'titulo':'Aviso!',
                        'mensaje':'El acta de nota ya fue aprobada, No podra realizar modificacionas en las mismas.',
                        'volver':'/'
                        }
        else:
            mensaje_usuario={
                    'titulo':'Aviso!',
                    'mensaje':'Usted no tiene permiso para editar actas de notas',
                    'volver':'/'
                    }
            return http.request.website.render('website_apiform.mensaje', mensaje_usuario)
    
    
    @http.route(['/actas/consultar/<model("unefa.acta_notas_pensum"):acta_data>'],
                                            type='http', auth='user', website=True)
    def consultar_actas_notas(self,acta_data):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        user_obj=registry('res.users')
        user_ids=user_obj.search(cr,uid,[('id','=',uid)])
        user_data=user_obj.browse(cr,uid,user_ids)
        inscripcion_obj=registry('unefa.inscripcion_asignatura')
        inscripcion_asignatura_obj=registry('unefa.asignatura_inscritas')
        estudiante_obj=registry('unefa.usuario_estudiante')
        inscripcion_id=inscripcion_obj.search(cr,uid,[('periodo_id','=',acta_data['gestion_semestre_id']['periodo_id']['id']),('state','in',['inscrito'])])
        inscripcion_data=inscripcion_obj.browse(cr,uid,inscripcion_id)
        list_inscripcion_ids=[]
        list_estudiantes_ids=[]
        for inscripcion in inscripcion_data:
            if inscripcion.user_id.pensum_id.id==acta_data['pensum_id']['id']:
                list_inscripcion_ids.append(inscripcion.id)
        inscripcion_asignatura_id=inscripcion_asignatura_obj.search(cr,uid,
                                        [('inscripcion_id','in',list_inscripcion_ids),
                                        ('asignatura_id','=',acta_data['gestion_semestre_id']['asignatura_id']['id']),
                                        ('seccion_id','=',acta_data['gestion_semestre_id']['seccion_id']['id']),
                                        ('inscripcion_especial','=',False)])
        inscripcion_especial_asignatura_id=inscripcion_asignatura_obj.search(cr,uid,
                                        [('inscripcion_id','in',list_inscripcion_ids),
                                        ('asignatura_relacion_id','=',acta_data['gestion_semestre_id']['asignatura_id']['id']),
                                        ('seccion_id','=',acta_data['gestion_semestre_id']['seccion_id']['id']),
                                        ('inscripcion_especial','=',True)])
        asignaturas_inscritas_total_ids=list(set(inscripcion_asignatura_id) | set(inscripcion_especial_asignatura_id))
        inscripcion_asignatura_data=inscripcion_asignatura_obj.browse(cr,uid,asignaturas_inscritas_total_ids)
        for ins_asig in inscripcion_asignatura_data:
            list_estudiantes_ids.append(ins_asig.inscripcion_id.user_id.id)
        
        estudiantes_ids=estudiante_obj.search(cr,uid,[('id','in',list_estudiantes_ids)],order='primer_apellido')
        usuario_estudiante_data=estudiante_obj.browse(cr,uid,estudiantes_ids)
        lista_estudiantes=[]
        lista_usuarios=[]
        for acta in acta_data:
            for estudiantes in acta.notas_ids:
                lista_estudiantes.append(estudiantes.estudiante_id.id)
                lista_usuarios.append(estudiantes.estudiante_id.user_id.id)
        
        if (uid in lista_usuarios) or (uid == acta_data['gestion_semestre_id']['profesor_id']['id']) or (user_data['is_coordinador']==True) or (user_data['is_asistente']==True):
            datos={'parametros':{
                        'titulo':'Consultar Acta de Notas',
                        'template':'unefa_gestion_semestre.consultar_acta_notas',
                        'url_boton_list':'',
                        'remover_btn_enviar':'si',
                        'id_form':'formconsultaractas',
                        },
                        'usuario_estudiante_data':usuario_estudiante_data,
                        'acta_data':acta_data,
                        'lista_estudiantes':lista_estudiantes,
                        }
            return panel.panel_post(datos)
        else:
            mensaje_usuario={
                    'titulo':'Aviso!',
                    'mensaje':'Usted no tiene permiso para consultar este acta de notas',
                    'volver':'/'
                    }
            return http.request.website.render('website_apiform.mensaje', mensaje_usuario)
    
    @http.route('/actas/guardar',type='json', auth="public", website=True)
    def guardar_actas(self,**post):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        lista_campos=post.keys()
        vals={}
        id_registro=post['id']
        actas_notas_obj=registry('unefa.acta_notas_asignaturas')
        actas_pensum_obj=registry('unefa.acta_notas_pensum')
        for campos in lista_campos:
            numero=campos.split('-')[1]
            campo_guardar=panel.dict_keys_startswith2(post,numero).keys()
            for c in campo_guardar:
                vals[c.split('-')[0]]=post[c]
                lista_campos.remove(c)
            vals['pensum_acta_id']=id_registro
            actas_notas_obj.create(cr,uid,vals)
        actas_pensum_obj.write(cr,SUPERUSER_ID,int(id_registro),{'creado':True})
        ret={'redirect':'/actas/consultar/%s' % (int(id_registro))}
        return ret
        
    @http.route('/actas/editar',type='json', auth="public", website=True)
    def editar_actas(self,**post):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        lista_campos=post.keys()
        vals={}
        id_registro=post['id']
        actas_notas_obj=registry('unefa.acta_notas_asignaturas')
        id_nota=''
        for campos in lista_campos:
            numero=campos.split('-')[1]
            campo_guardar=panel.dict_keys_startswith2(post,numero).keys()
            for c in campo_guardar:
                if c.split('-')[0]!='id':
                    vals[c.split('-')[0]]=post[c]
                else:
                    id_nota=post[c]
                lista_campos.remove(c)
                vals['pensum_acta_id']=id_registro
            if id_nota=='null':
                actas_notas_obj.create(cr,uid,vals)
            else:
                actas_notas_obj.write(cr,uid,int(id_nota),vals)
        ret={'redirect':'/actas/consultar/%s' % (int(id_registro))}
        return ret
    
    @http.route(['/actas/descargar/<model("unefa.acta_notas_pensum"):acta_data>'],
                type='http', auth='user', website=True)
    def descargar_actas_notas(self,acta_data,**post):
        
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        reportname='unefa_gestion_semestre.acta_notas_qweb'
      
        carrera_id = acta_data['gestion_semestre_id']['carrera_id']['id']
        regimen = acta_data['gestion_semestre_id']['turno']
        coordinacion_obj=registry('unefa.coordinacion')
        coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('regimen','=',regimen)])
        coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_id)
        sede_data=coordinacion_data['sede_id']
        
        
        
        inscripcion_obj=registry('unefa.inscripcion_asignatura')
        inscripcion_asignatura_obj=registry('unefa.asignatura_inscritas')
        estudiante_obj=registry('unefa.usuario_estudiante')
        inscripcion_id=inscripcion_obj.search(cr,uid,[('periodo_id','=',acta_data['gestion_semestre_id']['periodo_id']['id']),('state','in',['inscrito'])])
        inscripcion_data=inscripcion_obj.browse(cr,uid,inscripcion_id)
        list_inscripcion_ids=[]
        list_estudiantes_ids=[]
        for inscripcion in inscripcion_data:
            if inscripcion.user_id.pensum_id.id==acta_data['pensum_id']['id']:
                list_inscripcion_ids.append(inscripcion.id)
        inscripcion_asignatura_id=inscripcion_asignatura_obj.search(cr,uid,
                                        [('inscripcion_id','in',list_inscripcion_ids),
                                        ('asignatura_id','=',acta_data['gestion_semestre_id']['asignatura_id']['id']),
                                        ('seccion_id','=',acta_data['gestion_semestre_id']['seccion_id']['id']),
                                        ('inscripcion_especial','=',False)])
        inscripcion_especial_asignatura_id=inscripcion_asignatura_obj.search(cr,uid,
                                        [('inscripcion_id','in',list_inscripcion_ids),
                                        ('asignatura_relacion_id','=',acta_data['gestion_semestre_id']['asignatura_id']['id']),
                                        ('seccion_id','=',acta_data['gestion_semestre_id']['seccion_id']['id']),
                                        ('inscripcion_especial','=',True)])
        asignaturas_inscritas_total_ids=list(set(inscripcion_asignatura_id) | set(inscripcion_especial_asignatura_id))
        inscripcion_asignatura_data=inscripcion_asignatura_obj.browse(cr,uid,asignaturas_inscritas_total_ids)
        for ins_asig in inscripcion_asignatura_data:
            list_estudiantes_ids.append(ins_asig.inscripcion_id.user_id.id)
        
        estudiantes_ids=estudiante_obj.search(cr,uid,[('id','in',list_estudiantes_ids)],order='primer_apellido')
        usuario_estudiante_data=estudiante_obj.browse(cr,uid,estudiantes_ids)
        lista_estudiantes=[]
        lista_usuarios=[]
        for acta in acta_data:
            for estudiantes in acta.notas_ids:
                lista_estudiantes.append(estudiantes.estudiante_id.id)
                lista_usuarios.append(estudiantes.estudiante_id.user_id.id)
        
        coordinador_obj=registry('unefa.usuario_coordinador')
        coordinador_id=coordinador_obj.search(cr,uid,[('coordinacion_id','=',coordinacion_id[0])])
        coordinador_data=coordinador_obj.browse(cr,uid,coordinador_id)
        
        
        valores={
            'regimen':regimen,
            'sede_data':sede_data,
            'coordinacion_data':coordinacion_data,
            'usuario_estudiante_data':usuario_estudiante_data,
            'acta_data':acta_data,
            'lista_estudiantes':lista_estudiantes,
            'coordinador_data':coordinador_data,
            }


        pdf = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        response=request.make_response(pdf, headers=pdfhttpheaders)
        response.headers.add('Content-Disposition', 'attachment; filename=Acta_notas_'+acta_data['gestion_semestre_id']['asignatura_id']['asignatura']+'_'+acta_data['gestion_semestre_id']['seccion_id']['seccion']+'_'+acta_data['gestion_semestre_id']['periodo_id']['periodo_academico']+'_.pdf;')
        return response
    
    
    @http.route(['/descargar/acta_notas_recuperacion/<model("unefa.gestion_semestre"):gestion_data>'],
                type='http', auth='user', website=True)
    def descargar_actas_nota_recuperacion(self,gestion_data, **post):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        
        carrera_id= gestion_data['carrera_id']
        turno= gestion_data['turno']
        periodo_id= gestion_data['periodo_id']
        
        cronograma_obj=registry('unefa.cronogramas_recuperacion')
        cronograma_id=cronograma_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('turno','=',turno),('periodo_id','=',int(periodo_id))])
        cronograma_data=cronograma_obj.browse(cr,uid,cronograma_id)
        
        coordinacion_obj=registry('unefa.coordinacion')
        coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('regimen','=',turno)])
        coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_id)
        sede_data=coordinacion_data['sede_id']
        coordinador_obj=registry('unefa.usuario_coordinador')
        coordinador_id=coordinador_obj.search(cr,uid,[('coordinacion_id','=',coordinacion_id[0])])
        coordinador_data=coordinador_obj.browse(cr,uid,coordinador_id)
        
        reportname='unefa_gestion_semestre.actas_nota_recuperacion'
        nombre_zip='acta_nota_recuperacion'+str(gestion_data['periodo_id'].periodo_academico)+'.zip'
        if os.path.exists(nombre_zip):
            os.remove(nombre_zip)
        comp_zip = zipfile.ZipFile(nombre_zip, "w" ,zipfile.ZIP_STORED, allowZip64=True)
        con=1
        
        for gestion in gestion_data:
            for actas in gestion.actas_recuperacion_ids:  
                for cronograma in cronograma_data:
                    for pensum in cronograma.pensum_ids:
                        if pensum.pensum_id.id==actas.pensum_id.id:
                            for asignatura in pensum.cronograma_line_ids:
                                if asignatura.asignatura_id.id==gestion.asignatura_id.id and asignatura.seccion_id.id==gestion.seccion_id.id:
                                    formato_mes = "%B" 
                                    formato_anio = "%Y" 
                                    
                                    fecha=datetime.strptime(asignatura.fecha_recuperacion, '%Y-%m-%d')
                                    fecha =datetime.date(fecha)
                                    mes = fecha.strftime(formato_mes)
                                    anio = fecha.strftime(formato_anio)
                                    dia=asignatura.fecha_recuperacion.split('-')[2]
                                    hora=asignatura.hora+' '+asignatura.horario
                                   
                con+=1
                valores={
                    'coordinacion_data':coordinacion_data,
                    'sede_data':sede_data,
                    'gestion_data':gestion_data,
                    'coordinador_data':coordinador_data,
                    'actas':actas,
                    'anio':anio,
                    'mes':mes,
                    'dia':dia,
                    'hora':hora,
                    }
                    
                nombre_file='Acta_nota_recuperacion_'+str(gestion.periodo_id.periodo_academico)+'_'+str(gestion.asignatura_id.asignatura)+'.pdf'
                if os.path.exists(nombre_file):
                    os.remove(nombre_file)
                acta_reporte = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
                file_tmp = open(nombre_file, "wb",buffering = 0)
                file_tmp.write('¿'+str(con)+'?\n')
                file_tmp.write(acta_reporte)
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
                
                
    @http.route(['/descargar/listas_estudiantes_semestre/<model("unefa.generar_lista_semestre"):lista_semestre_data>'],
                type='http', auth='user', website=True)
    def descargar_actas_nota_recuperacion(self,lista_semestre_data, **post):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        list_estudiante_id=[]
        list_semestre_ids=[]
        reportname='unefa_gestion_semestre.listas_estudiantes_semestre_qweb'
        nombre_zip='lista_estudiantes.zip'
        if os.path.exists(nombre_zip):
            os.remove(nombre_zip)
        comp_zip = zipfile.ZipFile(nombre_zip, "w" ,zipfile.ZIP_STORED, allowZip64=True)
        con=1
        carrera='hola'
        carrera_id=lista_semestre_data['carrera_id']['id']
        turno=lista_semestre_data['turno']
        periodo_id=lista_semestre_data['periodo_id']['id']
        pensum_id=lista_semestre_data['pensum_id']['id']
        
        coordinacion_obj=registry('unefa.coordinacion')
        coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('regimen','=',turno)])
        coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_id)
        sede_data=coordinacion_data['sede_id']
        
        for data in lista_semestre_data:
            for semestre in data.semestre_ids:
                list_semestre_ids.append(semestre.id)
            
        oferta_academica_obj=registry('unefa.oferta_academica')
        oferta_ids=oferta_academica_obj.search(cr,uid,[('carrera_id','=',carrera_id),('turno','=',turno),('periodo_id','=',periodo_id)])
        oferta_data=oferta_academica_obj.browse(cr,uid,oferta_ids)
        asignaturas_inscritas_obj=registry('unefa.asignatura_inscritas')
        for oferta in oferta_data:
            for pensum in oferta.pensum_ids:
                if pensum.pensum_id.id==pensum_id:
                    for semestre in pensum.semestres_ids:
                        if semestre.semestre_id.id in list_semestre_ids:
                            for seccion in semestre.secciones_ids:
                                asignaturas_inscritas_ids=asignaturas_inscritas_obj.search(cr,uid,[('seccion_id','=',seccion.id)])
                                asignatura_inscrita_data=asignaturas_inscritas_obj.browse(cr,uid,asignaturas_inscritas_ids)
                                for asignatura in asignatura_inscrita_data:
                                    list_estudiante_id.append(asignatura.inscripcion_id.user_id.id)
                                usuario_estudiante_obj=registry('unefa.usuario_estudiante')
                                estudiantes_ids=usuario_estudiante_obj.search(cr,uid,[('id','in',list_estudiante_id)],order='primer_apellido')
                                usuario_estudiante_data=usuario_estudiante_obj.browse(cr,uid,estudiantes_ids)
                                valores={
                                    'coordinacion_data':coordinacion_data,
                                    'sede_data':sede_data,
                                    'seccion':seccion.seccion,
                                    'semestre':semestre.semestre_id.semestre,
                                    'turno':turno,
                                    'carrera':carrera,
                                    'pensum':pensum.pensum_id.pensum,
                                    'usuario_estudiante_data':usuario_estudiante_data,
                                    }
                                
                                nombre_file='Lista_estudiantes_'+str(semestre.semestre_id.semestre)+'_'+seccion.seccion+'.pdf'
                                if os.path.exists(nombre_file):
                                    os.remove(nombre_file)
                                lista_reporte = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
                                file_tmp = open(nombre_file, "wb",buffering = 0)
                                file_tmp.write('¿'+str(con)+'?\n')
                                file_tmp.write(lista_reporte)
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
    
   
	
  
    
    
    
        
       
