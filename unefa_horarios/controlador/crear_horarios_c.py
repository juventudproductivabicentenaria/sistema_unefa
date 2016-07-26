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

class unefa_crear_horarios(http.Controller):
    
    def buscar_clase(self,asignatura,dia,id_registro,id_hora):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        dias_obj=registry.get('unefa.horario_dias')
        dias_ids=dias_obj.search(cr,uid,[('dia','=',dia)])
        seccion_datos_horario=registry.get('unefa.horarios_seccion_datos')
        
        if asignatura.id==False:
            seccion_datos_horario_ids=seccion_datos_horario.search(cr,uid,[('secciones_horario_id','=',int(id_registro)),('asignatura_id','=',int(asignatura)),('dia_id','=',int(dias_ids[0])),('hora_id','=',int(id_hora)),])
        else:
            seccion_datos_horario_ids=seccion_datos_horario.search(cr,uid,[('secciones_horario_id','=',int(id_registro)),('asignatura_id','=',int(asignatura)),('dia_id','=',int(dias_ids[0])),])
        clase=''
        if len(seccion_datos_horario_ids)==3:
            clase='horarios_1'    
        if len(seccion_datos_horario_ids)==2:
            clase='horarios_2'    
        if len(seccion_datos_horario_ids)==4:
            clase='horarios_3'    
        if len(seccion_datos_horario_ids)==5:
            clase='horarios_4'    
        if len(seccion_datos_horario_ids)==6:
            clase='horarios_5'    
        if len(seccion_datos_horario_ids)==1:
            clase='horarios_0'    
        return clase
        
    def buscar_clase_report(self,asignatura,dia,id_registro,id_hora):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        dias_obj=registry.get('unefa.horario_dias')
        dias_ids=dias_obj.search(cr,uid,[('dia','=',dia)])
        seccion_datos_horario=registry.get('unefa.horarios_seccion_datos')
        
        if asignatura.id==False:
            seccion_datos_horario_ids=seccion_datos_horario.search(cr,uid,[('secciones_horario_id','=',int(id_registro)),('asignatura_id','=',int(asignatura)),('dia_id','=',int(dias_ids[0])),('hora_id','=',int(id_hora)),])
        else:
            seccion_datos_horario_ids=seccion_datos_horario.search(cr,uid,[('secciones_horario_id','=',int(id_registro)),('asignatura_id','=',int(asignatura)),('dia_id','=',int(dias_ids[0])),])
        clase=''
        if len(seccion_datos_horario_ids)==3:
            clase='horarios_111'    
        if len(seccion_datos_horario_ids)==2:
            clase='horarios_221'    
        if len(seccion_datos_horario_ids)==4:
            clase='horarios_331'    
        if len(seccion_datos_horario_ids)==5:
            clase='horarios_441'    
        if len(seccion_datos_horario_ids)==6:
            clase='horarios_551'    
        if len(seccion_datos_horario_ids)==1:
            clase='horarios_001'    
        return clase
        
    
    @http.route(['/horarios/crear/<model("unefa.horarios_seccion"):horarios_data>'],
                                            type='http', auth='user', website=True)
    def crear_horario(self,horarios_data):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        
        users_obj=registry.get('res.users')
        users_ids=users_obj.search(cr,uid,[('id','=',uid)])
        users_data=users_obj.browse(cr,uid,users_ids)
        list_group=[]
        for g in users_data['groups_id']:
            list_group.append(g.name)
        mensaje_usuario={
                'titulo':'Aviso!',
                'mensaje':'Disculpe su rol NO tiene permisos para realizar la elaboración de horarios, Comuníquese con el administrador del sistema',
                'volver':'/'
                }
        
        if ('Coordinador' in list_group) or ('Profesor Adjunto' in list_group) :
            print True
        else:
            return http.request.website.render('website_apiform.mensaje', mensaje_usuario)
        
        
        relacion_hora_turno=registry.get('unefa.horas_turno')
        relacion_hora_turno_ids=relacion_hora_turno.search(cr,uid,[('turno','=',horarios_data['horario_id']['turno']),('periodo_id','=',horarios_data['horario_id']['periodo_id']['id']),('state','=','aprobado')])
        relacion_hora_turno_data=relacion_hora_turno.browse(cr,uid,relacion_hora_turno_ids)
        
        if len(relacion_hora_turno_ids)==0:
            mensaje={
                'titulo':'Aviso!',
                'mensaje':'Disculpe NO esta configurado un Horario para el Período Académico '+horarios_data['horario_id']['periodo_id']['periodo_academico']+' Comuníquese con el administrador del sistema',
                'volver':'/'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje)
        
        relacion_hora_sabado_ids=relacion_hora_turno.search(cr,uid,[('turno','=','sabatino'),('periodo_id','=',horarios_data['horario_id']['periodo_id']['id']),('state','=','aprobado')])
        relacion_hora_sabado_data=relacion_hora_turno.browse(cr,uid,relacion_hora_sabado_ids)
        
        if len(relacion_hora_sabado_ids)==0:
            mensaje={
                'titulo':'Aviso!',
                'mensaje':'Disculpe NO esta configurado un Horario Sabatino para el Período Académico '+horarios_data['horario_id']['periodo_id']['periodo_academico']+' Comuníquese con el administrador del sistema',
                'volver':'/'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje)
        
        asignatura_seccion_obj=registry.get('unefa.oferta_academica_asignatura')
        asignatura_seccion_ids=asignatura_seccion_obj.search(cr,uid,[('oferta_asignatura_id','=',horarios_data['seccion_id']['id'])])
        asignatura_seccion_data=asignatura_seccion_obj.browse(cr,uid,asignatura_seccion_ids)
        
        asignatura_oferta_academica_obj=registry.get('unefa.oferta_academica_asignatura')
        asignatura_oferta_academica_ids=asignatura_oferta_academica_obj.search(cr,uid,[('oferta_asignatura_id','=',horarios_data['seccion_id']['id'])])
        asignatura_oferta_academica_data=asignatura_oferta_academica_obj.browse(cr,uid,asignatura_oferta_academica_ids)
        dic_prelacion={}
        for i in asignatura_seccion_data:
            prelacion=''
            cont=1
            for n in i.asignatura_id.asignaturas_ids:
                if len(i.asignatura_id.asignaturas_ids)==cont:
                    prelacion+=n.codigo_asignatura
                else:
                    prelacion+=n.codigo_asignatura + '-'
                cont+=1
            dic_prelacion[i.id]=prelacion
        
        datos={'parametros':{
                    'titulo':'Crear Horario',
                    'template':'unefa_horarios.crear_horarios',
                    'url_boton_list':'',
                    'css':'info',
                    'id_form':'formcrearhorarios',
                    'id_enviar':'enviar_horario',
                    'action':'/horarios/guardar',
                    },
                    'horarios_data':horarios_data,
                    'relacion_hora_turno_data':relacion_hora_turno_data,
                    'asignatura_seccion_data':asignatura_seccion_data,
                    'relacion_hora_sabado_data':relacion_hora_sabado_data,
                    'asignatura_oferta_academica_data':asignatura_oferta_academica_data,
                    'dic_prelacion':dic_prelacion,
                    }
        return panel.panel_post(datos)
        
    @http.route(['/horarios/editar/<model("unefa.horarios_seccion"):horarios_data>'],
                                            type='http', auth='user', website=True)
    def editar_horarios(self,horarios_data):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        
        users_obj=registry.get('res.users')
        users_ids=users_obj.search(cr,uid,[('id','=',uid)])
        users_data=users_obj.browse(cr,uid,users_ids)
        list_group=[]
        for g in users_data['groups_id']:
            list_group.append(g.name)
        
        mensaje_usuario={
                'titulo':'Aviso!',
                'mensaje':'Disculpe su rol NO tiene permisos para realizar la elaboración de horarios, Comuníquese con el administrador del sistema',
                'volver':'/'
                }
        
        if ('Coordinador' in list_group) or ('Profesor Adjunto' in list_group) :
            print True
        else:
            return http.request.website.render('website_apiform.mensaje', mensaje_usuario)
        
        relacion_hora_turno=registry.get('unefa.horas_turno')
        relacion_hora_turno_ids=relacion_hora_turno.search(cr,uid,[('turno','=',horarios_data['horario_id']['turno']),('periodo_id','=',horarios_data['horario_id']['periodo_id']['id']),('state','=','aprobado')])
        relacion_hora_turno_data=relacion_hora_turno.browse(cr,uid,relacion_hora_turno_ids)
        
        relacion_hora_sabado_ids=relacion_hora_turno.search(cr,uid,[('turno','=','sabatino'),('periodo_id','=',horarios_data['horario_id']['periodo_id']['id']),('state','=','aprobado')])
        relacion_hora_sabado_data=relacion_hora_turno.browse(cr,uid,relacion_hora_sabado_ids)
        
        asignatura_seccion_obj=registry.get('unefa.oferta_academica_asignatura')
        asignatura_seccion_ids=asignatura_seccion_obj.search(cr,uid,[('oferta_asignatura_id','=',horarios_data['seccion_id']['id'])])
        asignatura_seccion_data=asignatura_seccion_obj.browse(cr,uid,asignatura_seccion_ids)
        
        asignatura_oferta_academica_obj=registry.get('unefa.oferta_academica_asignatura')
        asignatura_oferta_academica_ids=asignatura_oferta_academica_obj.search(cr,uid,[('oferta_asignatura_id','=',horarios_data['seccion_id']['id'])])
        asignatura_oferta_academica_data=asignatura_oferta_academica_obj.browse(cr,uid,asignatura_oferta_academica_ids)
        dic_prelacion={}
        for i in asignatura_seccion_data:
            prelacion=''
            cont=1
            for n in i.asignatura_id.asignaturas_ids:
                if len(i.asignatura_id.asignaturas_ids)==cont:
                    prelacion+=n.codigo_asignatura
                else:
                    prelacion+=n.codigo_asignatura + '-'
                cont+=1
            dic_prelacion[i.id]=prelacion
       
        datos={'parametros':{
                    'titulo':'Editar Horario',
                    'template':'unefa_horarios.editar_horarios',
                    'url_boton_list':'',
                    'css':'info',
                    'id_form':'formeditarhorario',
                    'id_enviar':'enviar_horario_editado',
                    'action':'/horarios/editar',
                    },
                    'horarios_data':horarios_data,
                    'relacion_hora_turno_data':relacion_hora_turno_data,
                    'asignatura_seccion_data':asignatura_seccion_data,
                    'relacion_hora_sabado_data':relacion_hora_sabado_data,
                    'asignatura_oferta_academica_data':asignatura_oferta_academica_data,
                    'dic_prelacion':dic_prelacion,
                    }
        return panel.panel_post(datos)
        
    @http.route(['/horarios/consultar/<model("unefa.horarios_seccion"):horarios_data>'],
                                            type='http', auth='user', website=True)
    def consultar_horarios(self,horarios_data):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        relacion_hora_turno=registry.get('unefa.horas_turno')
        relacion_hora_turno_ids=relacion_hora_turno.search(cr,uid,[('turno','=',horarios_data['horario_id']['turno']),('periodo_id','=',horarios_data['horario_id']['periodo_id']['id']),('state','=','aprobado')])
        relacion_hora_turno_data=relacion_hora_turno.browse(cr,uid,relacion_hora_turno_ids)
        
        relacion_hora_sabado_ids=relacion_hora_turno.search(cr,uid,[('turno','=','sabatino'),('periodo_id','=',horarios_data['horario_id']['periodo_id']['id']),('state','=','aprobado')])
        relacion_hora_sabado_data=relacion_hora_turno.browse(cr,uid,relacion_hora_sabado_ids)
        
        asignatura_seccion_obj=registry.get('unefa.oferta_academica_asignatura')
        asignatura_seccion_ids=asignatura_seccion_obj.search(cr,uid,[('oferta_asignatura_id','=',horarios_data['seccion_id']['id'])])
        asignatura_seccion_data=asignatura_seccion_obj.browse(cr,uid,asignatura_seccion_ids)
        
        asignatura_oferta_academica_obj=registry.get('unefa.oferta_academica_asignatura')
        asignatura_oferta_academica_ids=asignatura_oferta_academica_obj.search(cr,uid,[('oferta_asignatura_id','=',horarios_data['seccion_id']['id'])])
        asignatura_oferta_academica_data=asignatura_oferta_academica_obj.browse(cr,uid,asignatura_oferta_academica_ids)
        dic_prelacion={}
        for i in asignatura_seccion_data:
            prelacion=''
            cont=1
            for n in i.asignatura_id.asignaturas_ids:
                if len(i.asignatura_id.asignaturas_ids)==cont:
                    prelacion+=n.codigo_asignatura
                else:
                    prelacion+=n.codigo_asignatura + '-'
                cont+=1
            dic_prelacion[i.id]=prelacion
        
        datos={'parametros':{
                        'titulo':'Consultar Horarios',
                        'template':'unefa_horarios.consultar_horarios',
                        'url_boton_list':'',
                        'remover_btn_enviar':'si',
                        'id_form':'formconsultarhorario',
                        },
                        'horarios_data':horarios_data,
                        'relacion_hora_turno_data':relacion_hora_turno_data,
                        'asignatura_seccion_data':asignatura_seccion_data,
                        'relacion_hora_sabado_data':relacion_hora_sabado_data,
                        'buscar_clase':self.buscar_clase,
                        'asignatura_oferta_academica_data':asignatura_oferta_academica_data,
                        'dic_prelacion':dic_prelacion,
                            }
        return panel.panel_post(datos)
    
    
    def validar_horas_materias(self,dic,editar=None):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        dict_1={}
        if editar==1:
            for n in dic.keys():
                dict_1[n]=dic[n]
            ids_registros=panel.dict_keys_startswith2(dict_1,'id')
            for valor in ids_registros.keys():
                del dict_1[valor]
        asignatura_data_obj=registry.get('unefa.asignatura')
        list_valores=dic.values()
        list_valores_filtrada = list(set(list_valores))
        lista_evaluar=[]
        for i in list_valores_filtrada:
            if i=='':
                list_valores_filtrada.remove(i)
        for n in list_valores_filtrada:
            for p in list_valores:
                if n==p:
                    lista_evaluar.append(p)
            asignatura_data=asignatura_data_obj.browse(cr,uid,int(n))
            if int(asignatura_data['total_horas'])<len(lista_evaluar):
                ret =  {'modal':{
                    'titulo':'<strong>Aviso!</strong>',
                    'cuerpo':'<h4 class="text-danger" >Usted excedio el Total de Horas de la Asignatura '+asignatura_data['asignatura'] +'</h4>',
                            },
                        }
                return ret  
            lista_evaluar=[]
        return True
        
    def validar_horas_materias_write(self,dic,editar=None):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        dict_1={}
        
        for n in dic.keys():
            dict_1[n]=dic[n]
        ids_registros=panel.dict_keys_startswith2(dict_1,'id')
        for valor in ids_registros.keys():
            del dict_1[valor]
        
        asignatura_data_obj=registry.get('unefa.asignatura')
        list_valores=dict_1.values()
        list_valores_filtrada = list(set(list_valores))
        lista_evaluar=[]
        for i in list_valores_filtrada:
            if i=='':
                list_valores_filtrada.remove(i)
        for n in list_valores_filtrada:
            for p in list_valores:
                if n==p:
                    lista_evaluar.append(p)
            asignatura_data=asignatura_data_obj.browse(cr,uid,int(n))
            if int(asignatura_data['total_horas'])<len(lista_evaluar):
                ret =  {'modal':{
                    'titulo':'<strong>Aviso!</strong>',
                    'cuerpo':'<h4 class="text-danger" >Usted excedio el Total de Horas de la Asignatura '+asignatura_data['asignatura'] +'</h4>',
                            },
                        }
                return ret  
            lista_evaluar=[]
        return True
    
    @http.route('/horarios/guardar',type='json', auth="public", website=True)
    def guardar_horarios(self,**post):
        ret=self.validar_horas_materias(post)
        if ret!=True:
            return ret
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        lista_campos=post.keys()
        list_datos=[]
        seccion_horario_obj=registry.get('unefa.horarios_seccion')
        secciones_horarios_datos_obj=registry.get('unefa.horarios_seccion_datos')
        dias_obj=registry.get('unefa.horario_dias')
        for record in lista_campos:
            registros=record.split('-')
            ids=registros[3]
            dias_ids=dias_obj.search(cr,uid,[('dia','=',registros[0])])
            list_datos.append([{'dia_id': int(dias_ids[0]), 'secciones_horario_id': int(ids), 'hora_id':int(registros[2]), 'asignatura_id': post[record]}])
        for i in list_datos:
            secciones_horarios_datos_obj.create(cr,uid,i[0])
        seccion_horario_obj.write(cr,uid,int(ids),{'creado':True,'state':'aprobado'})
        ret={'redirect':'/horarios/consultar/%s' % (int(ids))}
        return ret
        
    @http.route('/horarios/editar',type='json', auth="public", website=True)
    def guardar_horarios_editar(self,**post):
        ret=self.validar_horas_materias_write(post,1)
        if ret!=True:
            return ret
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        lista_campos=post.keys()
        list_datos=[]
        list_ids_registros=[]
        secciones_horarios_datos_obj=registry.get('unefa.horarios_seccion_datos')
        dias_obj=registry.get('unefa.horario_dias')
        ids_registros=panel.dict_keys_startswith2(post,'id')
        for n in ids_registros.keys():
            lista_campos.remove(n)
        for record in lista_campos:
            registros=record.split('-')
            ids=registros[3]
            id_registro=post[record+'-id']
            dias_ids=dias_obj.search(cr,uid,[('dia','=',registros[0])])
            if record+'-id' in post.keys():
                id_registro=post[record+'-id']
                list_datos.append([{'dia_id': int(dias_ids[0]), 'secciones_horario_id': int(ids), 'hora_id':int(registros[2]), 'asignatura_id': post[record]}])
                list_ids_registros.append(id_registro)
        cont=0
        for i in list_datos:
            secciones_horarios_datos_obj.write(cr,uid,int(list_ids_registros[cont]),i[0])
            cont+=1
        ret={'redirect':'/horarios/consultar/%s' % (int(ids))}
        return ret
    

                
                
                
    @http.route(['/descargar/horarios/<model("unefa.horarios"):horario_data>'],
                type='http', auth='user', website=True)
    def descargar_horarios(self,horario_data,**post):
       
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        reportname='unefa_horarios.horarios'
        nombre_zip='horarios_'+horario_data['periodo_id']['periodo_academico']+'_'+horario_data['carrera_id']['nombre']+'.zip'
        if os.path.exists(nombre_zip):
            os.remove(nombre_zip)
        comp_zip = zipfile.ZipFile(nombre_zip, "w" ,zipfile.ZIP_STORED, allowZip64=True)
        con=1
        dias=['Lunes','Martes','Miercoles','Jueves','Viernes']
        for horario in horario_data:
            relacion_hora_turno=registry.get('unefa.horas_turno')
            relacion_hora_turno_ids=relacion_hora_turno.search(cr,uid,[('turno','=',horario['turno']),('periodo_id','=',horario['periodo_id']['id']),('state','=','aprobado')])
            relacion_hora_turno_data=relacion_hora_turno.browse(cr,uid,relacion_hora_turno_ids)
            
            relacion_hora_sabado_ids=relacion_hora_turno.search(cr,uid,[('turno','=','sabatino'),('periodo_id','=',horario['periodo_id']['id']),('state','=','aprobado')])
            relacion_hora_sabado_data=relacion_hora_turno.browse(cr,uid,relacion_hora_sabado_ids)
            carrera=horario.carrera_id.nombre
            pensum=horario.pensum_id.pensum
            periodo=horario.periodo_id.periodo_academico
            dic_lunes={}
            dic_martes={}
            dic_miercoles={}
            dic_jueves={}
            dic_viernes={}
            dic_sabado={}
            for h in horario.secciones_ids:
                if h.creado==True:
                    for d in h.datos_ids:
                        if d.dia_id.dia=='Lunes':
                            dic_lunes[d.id]=self.buscar_clase_report(d.asignatura_id,'Lunes',int(d.secciones_horario_id),int(d.hora_id))
                        if d.dia_id.dia=='Martes':
                            dic_martes[d.id]=self.buscar_clase_report(d.asignatura_id,'Martes',int(d.secciones_horario_id),int(d.hora_id))
                        if d.dia_id.dia=='Miercoles':
                            dic_miercoles[d.id]=self.buscar_clase_report(d.asignatura_id,'Miercoles',int(d.secciones_horario_id),int(d.hora_id))
                        if d.dia_id.dia=='Jueves':
                            dic_jueves[d.id]=self.buscar_clase_report(d.asignatura_id,'Jueves',int(d.secciones_horario_id),int(d.hora_id))
                        if d.dia_id.dia=='Viernes':
                            dic_viernes[d.id]=self.buscar_clase_report(d.asignatura_id,'Viernes',int(d.secciones_horario_id),int(d.hora_id))    
                        if d.dia_id.dia=='Sabado':
                            dic_sabado[d.id]=self.buscar_clase_report(d.asignatura_id,'Sabado',int(d.secciones_horario_id),int(d.hora_id))    
            cont=1
            for i in horario.secciones_ids:
                if i.creado==True:
                    coordinacion_obj=registry.get('unefa.coordinacion')
                    coordinacion_ids=coordinacion_obj.search(cr,uid,[('carrera_id','=',horario.carrera_id.id),('regimen','=',horario.turno)])
                    coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_ids)
                    
                    asignatura_oferta_academica_obj=registry.get('unefa.oferta_academica_asignatura')
                    asignatura_oferta_academica_ids=asignatura_oferta_academica_obj.search(cr,uid,[('oferta_asignatura_id','=',i['seccion_id']['id'])])
                    asignatura_oferta_academica_data=asignatura_oferta_academica_obj.browse(cr,uid,asignatura_oferta_academica_ids)
                    dic_prelacion={}
                    for a in asignatura_oferta_academica_data:
                        prelacion=''
                        cont2=1
                        for n in a.asignatura_id.asignaturas_ids:
                            if len(a.asignatura_id.asignaturas_ids)==cont2:
                                prelacion+=n.codigo_asignatura
                            else:
                                prelacion+=n.codigo_asignatura + '-'
                            cont2+=1
                        dic_prelacion[a.id]=prelacion
                    
                    coordinacion_obj=registry('unefa.coordinacion')
                    coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(horario.carrera_id)),('regimen','=',horario.turno)])
                    coordinador_obj=registry('unefa.usuario_coordinador')
                    coordinador_id=coordinador_obj.search(cr,uid,[('coordinacion_id','=',coordinacion_id[0])])
                    coordinador_data=coordinador_obj.browse(cr,uid,coordinador_id)
                   
                    valores={
                        'coordinacion_data':coordinacion_data['nombre'],
                        'horarios_data':horario,
                        'seccion_horario_data':i,
                        'relacion_hora_turno_data':relacion_hora_turno_data,
                        'relacion_hora_sabado_data':relacion_hora_sabado_data,
                        'relacion_hora_sabado_data':relacion_hora_sabado_data,
                        'buscar_clase':self.buscar_clase,
                        'lunes':dic_lunes,
                        'martes':dic_martes,
                        'miercoles':dic_miercoles,
                        'jueves':dic_jueves,
                        'viernes':dic_viernes,
                        'sabado':dic_sabado,
                        'asignatura_oferta_academica_data':asignatura_oferta_academica_data,
                        'dic_prelacion':dic_prelacion,
                        'coordinador':coordinador_data,
                        'carrera':carrera,
                        'periodo':periodo,
                        'pensum':pensum,
                        }
                    nombre_file='Horario_'+horario_data['periodo_id']['periodo_academico']+'_'+horario_data['carrera_id']['nombre']+'_'+i.seccion_id.seccion+'.pdf'
                    cont+=1
                    if os.path.exists(nombre_file):
                        os.remove(nombre_file)
                    horario_reporte = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
                    file_tmp = open(nombre_file, "wb",buffering = 0)
                    file_tmp.write('¿'+str(con)+'?\n')
                    file_tmp.write(horario_reporte)
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

    
    
    @http.route(['/descargar/horarios_particular/<int:id_horario>'],
                type='http', auth='user', website=True)
    def descargar_horarios_particular(self,id_horario,**post):
        
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        reportname='unefa_horarios.horarios'
        con=1
        dias=['Lunes','Martes','Miercoles','Jueves','Viernes']
        dic_lunes={}
        dic_martes={}
        dic_miercoles={}
        dic_jueves={}
        dic_viernes={}
        dic_sabado={}
        
        horario_seccion_obj=registry.get('unefa.horarios_seccion')
        horario_seccion_ids=horario_seccion_obj.search(cr,uid,[('id','=',id_horario)])
        horario_data=horario_seccion_obj.browse(cr,uid,horario_seccion_ids)
            
            
            
        for h in horario_data:
            if h.creado==True:
                for d in h.datos_ids:
                    if d.dia_id.dia=='Lunes':
                        dic_lunes[d.id]=self.buscar_clase_report(d.asignatura_id,'Lunes',int(d.secciones_horario_id),int(d.hora_id))
                    if d.dia_id.dia=='Martes':
                        dic_martes[d.id]=self.buscar_clase_report(d.asignatura_id,'Martes',int(d.secciones_horario_id),int(d.hora_id))
                    if d.dia_id.dia=='Miercoles':
                        dic_miercoles[d.id]=self.buscar_clase_report(d.asignatura_id,'Miercoles',int(d.secciones_horario_id),int(d.hora_id))
                    if d.dia_id.dia=='Jueves':
                        dic_jueves[d.id]=self.buscar_clase_report(d.asignatura_id,'Jueves',int(d.secciones_horario_id),int(d.hora_id))
                    if d.dia_id.dia=='Viernes':
                        dic_viernes[d.id]=self.buscar_clase_report(d.asignatura_id,'Viernes',int(d.secciones_horario_id),int(d.hora_id))    
                    if d.dia_id.dia=='Sabado':
                        dic_sabado[d.id]=self.buscar_clase_report(d.asignatura_id,'Sabado',int(d.secciones_horario_id),int(d.hora_id))    
                        
        for i in horario_data:
            carrera_id=i.horario_id.carrera_id.id
            pensum_id=i.horario_id.pensum_id.id
            periodo_id=i.horario_id.periodo_id.id
            turno=i.horario_id.turno
            
            relacion_hora_turno=registry.get('unefa.horas_turno')
            relacion_hora_turno_ids=relacion_hora_turno.search(cr,uid,[('turno','=',turno),('periodo_id','=',periodo_id),('state','=','aprobado')])
            relacion_hora_turno_data=relacion_hora_turno.browse(cr,uid,relacion_hora_turno_ids)
            
            relacion_hora_sabado_ids=relacion_hora_turno.search(cr,uid,[('turno','=','sabatino'),('periodo_id','=',periodo_id),('state','=','aprobado')])
            relacion_hora_sabado_data=relacion_hora_turno.browse(cr,uid,relacion_hora_sabado_ids)
            
            pensum=i.horario_id.pensum_id.pensum
            periodo=i.horario_id.periodo_id.periodo_academico
            carrera=i.horario_id.carrera_id.nombre
            estudiante=False
            nombre=''
            cedula=''
            if i.creado==True:
                coordinacion_obj=registry.get('unefa.coordinacion')
                coordinacion_ids=coordinacion_obj.search(cr,uid,[('carrera_id','=',carrera_id),('regimen','=',turno)])
                coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_ids)
                
                usuario_obj=registry.get('res.users')
                usuario_ids=usuario_obj.search(cr,uid,[('id','=',int(uid))])
                usuario_data=usuario_obj.browse(cr,uid,usuario_ids)
                
                for u in usuario_data:
                    
                    for g in u.groups_id:
                        
                        if 'Estudiante'==g.name:
                            estudiante='estudiante'
                           
                            nombre=u.nombre_completo
                            cedula=u.cedula
                
                asignatura_oferta_academica_obj=registry.get('unefa.oferta_academica_asignatura')
                asignatura_oferta_academica_ids=asignatura_oferta_academica_obj.search(cr,uid,[('oferta_asignatura_id','=',i['seccion_id']['id'])])
                asignatura_oferta_academica_data=asignatura_oferta_academica_obj.browse(cr,uid,asignatura_oferta_academica_ids)
                dic_prelacion={}
                for a in asignatura_oferta_academica_data:
                    prelacion=''
                    cont2=1
                    for n in a.asignatura_id.asignaturas_ids:
                        if len(a.asignatura_id.asignaturas_ids)==cont2:
                            prelacion+=n.codigo_asignatura
                        else:
                            prelacion+=n.codigo_asignatura + '-'
                        cont2+=1
                    dic_prelacion[a.id]=prelacion
                
                coordinacion_obj=registry('unefa.coordinacion')
                coordinacion_id=coordinacion_obj.search(cr,uid,[('carrera_id','=',int(carrera_id)),('regimen','=',turno)])
                coordinador_obj=registry('unefa.usuario_coordinador')
                coordinador_id=coordinador_obj.search(cr,uid,[('coordinacion_id','=',coordinacion_id[0])])
                coordinador_data=coordinador_obj.browse(cr,uid,coordinador_id)
                valores={
                    'coordinacion_data':coordinacion_data['nombre'],
                    'seccion_horario_data':i,
                    'relacion_hora_turno_data':relacion_hora_turno_data,
                    'relacion_hora_sabado_data':relacion_hora_sabado_data,
                    'relacion_hora_sabado_data':relacion_hora_sabado_data,
                    'buscar_clase':self.buscar_clase,
                    'lunes':dic_lunes,
                    'martes':dic_martes,
                    'miercoles':dic_miercoles,
                    'jueves':dic_jueves,
                    'viernes':dic_viernes,
                    'sabado':dic_sabado,
                    'asignatura_oferta_academica_data':asignatura_oferta_academica_data,
                    'dic_prelacion':dic_prelacion,
                    'coordinador':coordinador_data,
                    'periodo':periodo,
                    'pensum':pensum,
                    'estudiante':estudiante,
                    'nombre':nombre,
                    'cedula':cedula,
                    }
                
        
            
            pdf = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
            response=request.make_response(pdf, headers=pdfhttpheaders)
            response.headers.add('Content-Disposition', 'attachment; filename=Horario_'+periodo+'_'+carrera+'_'+i.seccion_id.seccion+'.pdf;')
        return response
    
    
    
   
	
  
    
    
    
        
       
