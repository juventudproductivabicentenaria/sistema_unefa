# -*- coding: utf-8 -*-
##############################################################################
#
#    Programa realizado por, Jeison Pernía y Jonathan Reyes en el marco
#    del plan de estudios de la UNEFA, como TRABAJO ESPECIAL DE GRADO,
#    con el fin de optar al título de Ingeniero de Sistemas.
#   
     #~ Visitanos en http://juventudproductivabicentenaria.blogspot.com
##############################################################################
#
from openerp.osv import fields, osv
from datetime import datetime, timedelta
from openerp import SUPERUSER_ID
import time

class unefa_oferta_academica(osv.osv):
    _name = 'unefa.oferta_academica'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    def default_carrera(self, cr, uid, ids, context=None):
        users_obj=self.pool.get('res.users')
        users_ids=users_obj.search(cr,uid,[('id','=',uid)],context=context)
        users_data=users_obj.browse(cr,uid,users_ids)
        return int(users_data['coordinacion_id'].carrera_id)
        
    def default_regimen(self, cr, uid, ids, context=None):
        users_obj=self.pool.get('res.users')
        users_ids=users_obj.search(cr,uid,[('id','=',uid)],context=context)
        users_data=users_obj.browse(cr,uid,users_ids)
        return users_data['coordinacion_id'].regimen
    
    _columns = {
        'carrera_id': fields.many2one('unefa.carrera', 'Carrera',required=True,readonly=True),
        'turno':fields.selection([('nocturno','NOCTURNO'),('diurno','DIURNO')],'Turno', readonly=True),
        'regimen':fields.selection([('semestre','SEMESTRE'),('modular','MODULAR'),('ninguno','NINGUNO')],'Régimen',required=True,states={'aprobado': [('readonly', True)]}),
        'modalidad_id': fields.many2one('unefa.modalidad', 'Modalidad',readonly=False, required=True,states={'borrador': [('readonly', True)],'ejecucion': [('readonly', True)],'aprobado': [('readonly', True)]}),
        'periodo_id': fields.many2one('unefa.conf.periodo_academico','Período Académico',required=True,states={'borrador': [('readonly', True)],'ejecucion': [('readonly', True)],'aprobado': [('readonly', True)]}),
        'observaciones': fields.text('Observaciones',states={'aprobado': [('readonly', True)]}),
        'pensum_ids':fields.one2many('unefa.pensum_oferta_academica','oferta_id', 'Pensum', required=True,states={'aprobado': [('readonly', True)]}),
        'state': fields.selection([
            ('borrador', 'Borrador'),
            ('ejecucion', 'En Ejecución'),
            ('aprobado', 'Aprobado'),
            ],'Estado', readonly=True, copy=False, help="Este es es estado actual de la oferta académica.", select=True),
    }
    
    _defaults = {
        'create_date': fields.datetime.now,
        'carrera_id': default_carrera,
        'turno': default_regimen,
        'regimen': 'semestre',
    }
    
    _sql_constraints = [
        ('oferta_uniq', 'unique(carrera_id,turno,periodo_id)', 'Ya existe una oferta academica registrada para esta carrera y período académico.')
        ]
    
    _order = 'create_date desc, id desc'
    
    def descargar_oferta_academica(self,cr,uid,ids,context=None):
        url='/descargar/oferta_academica/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
    def filtrar_coordinacion_oferta_academica(self,cr,uid,ids,context=None):
        objeto_users=self.pool.get('res.users')
        id_users=objeto_users.search(cr,uid,[('id','=',uid)])
        data_users=objeto_users.browse(cr,uid,id_users)
        coordinacion = data_users['coordinacion_id']
        value={}
        value={
            'coordinacion_id':coordinacion,
            }
        return {'value':value}
    
    def aprobar_oferta_academica(self, cr, uid, ids, context=None):
        vals_gestion={}
        list_pensum=[]
        list_asignatura=[]
        cronograma_recuperacion_obj=self.pool.get('unefa.cronogramas_recuperacion')
        user_obj=self.pool.get('res.users')
        user_ids=user_obj.search(cr,uid,[('id','=',uid)])
        user_data=user_obj.browse(cr,uid,user_ids)
        piso_id=user_data['coordinacion_id'].coordinaciones_ids.id
        pensum_oferta_academica_obj=self.pool.get('unefa.pensum_oferta_academica')
        oferta_academica_semestre_obj=self.pool.get('unefa.oferta_academica_semestre')
        oferta_academica_seccion_obj=self.pool.get('unefa.oferta_academica_seccion')
        oferta_academica_asignatura_obj=self.pool.get('unefa.oferta_academica_asignatura')
        gestion_semeste_obj=self.pool.get('unefa.gestion_semestre')
        mail_message_obj=self.pool.get('mail.message')
        usuarios_obj=self.pool.get('res.users')
        for record in self.browse(cr,uid,ids):
            periodo=record.periodo_id.periodo_academico
            usuarios_ids=usuarios_obj.search(cr,uid,[('carrera_id','=',record.carrera_id.id),('regimen','=',record.turno)])
            usuarios_data=usuarios_obj.browse(cr,uid,usuarios_ids)
            for id_pensum in record.pensum_ids:
                pensum_oferta_academica_obj.write(cr,uid,id_pensum.id,{'state':'aprobado'})
                for id_semestre in id_pensum.semestres_ids:
                    oferta_academica_semestre_obj.write(cr,uid,id_semestre.id,{'state':'aprobado'})
                    for seccion in id_semestre.secciones_ids:
                        oferta_academica_seccion_obj.write(cr,uid,seccion.id,{'state':'aprobado'})
                        for id_asignatura in seccion.asignaturas_ids:
                            
                            if id_asignatura.asignatura_id.reparacion==False:
                                list_asignatura.append([0,False,{'semestre_id':id_semestre.semestre_id.id,
                                                        'seccion_id':seccion.id,
                                                        'asignatura_id':id_asignatura.asignatura_id.id,
                                                        'profesor_id':id_asignatura.profesor_id.id,
                                                         }])
                            vals_gestion={'asignatura_id':id_asignatura.asignatura_id.id,'seccion_id':seccion.id,
                                        'periodo_id':record.periodo_id.id,'pensum_id':id_pensum.pensum_id.id,
                                        'carrera_id':record.carrera_id.id,'turno':record.turno,'state':'borrador','profesor_id':id_asignatura.profesor_id.id}
                            gestion_semeste_obj.create(cr,SUPERUSER_ID,vals_gestion)
                            oferta_academica_asignatura_obj.write(cr,SUPERUSER_ID,id_asignatura.id,{'state':'aprobado'})
                            
                            
                list_pensum.append([0,False,{'pensum_id':id_pensum.pensum_id.id,'cronograma_line_ids':list_asignatura }])
                list_asignatura=[]
            vals_cronograma={
                'carrera_id':record.carrera_id.id,
                'turno':record.turno,
                'periodo_id':record.periodo_id.id,
                'pensum_ids':list_pensum,
                    }
            cronograma_recuperacion_obj.create(cr,SUPERUSER_ID,vals_cronograma)
        list_partners=[]
        
        for usuario in usuarios_data:
            list_partners.append(usuario.partner_id.id)
       
        values={
            'body': 'Ha sido aprobada la oferta académica para el período '+periodo+'.', 
            'model': 'unefa.planificacion_semestre', 
            'res_id': ids[0], 
            'parent_id': False, 
            'subtype_id': False, 
            'author_id': uid, 
            'type': 'notification', 
            'notified_partner_ids': [[6, False, list_partners]], 
            'subject': False}
            
        mail_message_obj.create(cr,SUPERUSER_ID,values)        
        return self.write(cr,uid,ids,{'state':'aprobado'},context=context)
        
  
    
    def ejecucion_oferta_academica(self, cr, uid, ids, context=None):
        pensum_oferta_academica_obj=self.pool.get('unefa.pensum_oferta_academica')
        oferta_academica_semestre_obj=self.pool.get('unefa.oferta_academica_semestre')
        oferta_academica_seccion_obj=self.pool.get('unefa.oferta_academica_seccion')
        oferta_academica_asignatura_obj=self.pool.get('unefa.oferta_academica_asignatura')
        mail_message_obj=self.pool.get('mail.message')
        usuarios_obj=self.pool.get('res.users')
        for record in self.browse(cr,uid,ids):
            periodo=record.periodo_id.periodo_academico
            usuarios_ids=usuarios_obj.search(cr,uid,[('carrera_id','=',record.carrera_id.id),('regimen','=',record.turno)])
            usuarios_data=usuarios_obj.browse(cr,uid,usuarios_ids)
            for id_pensum in record.pensum_ids:
                pensum_oferta_academica_obj.write(cr,uid,id_pensum.id,{'state':'ejecucion'})
                for id_semestre in id_pensum.semestres_ids:
                    oferta_academica_semestre_obj.write(cr,uid,id_semestre.id,{'state':'ejecucion'})
                    for seccion in id_semestre.secciones_ids:
                        oferta_academica_seccion_obj.write(cr,uid,seccion.id,{'state':'ejecucion'})
                        for id_asignatura in seccion.asignaturas_ids:
                            oferta_academica_asignatura_obj.write(cr,uid,id_asignatura.id,{'state':'ejecucion'})
        
        list_partners=[]
        
        for usuario in usuarios_data:
            list_partners.append(usuario.partner_id.id)
       
        values={
            'body': 'Ha sido puesta en ejecución la oferta académica para el período '+periodo+'.', 
            'model': 'unefa.planificacion_semestre', 
            'res_id': ids[0], 
            'parent_id': False, 
            'subtype_id': False, 
            'author_id': uid, 
            'type': 'notification', 
            'notified_partner_ids': [[6, False, list_partners]], 
            'subject': False}
            
        mail_message_obj.create(cr,SUPERUSER_ID,values)
        
        
        
        return self.write(cr,uid,ids,{'state':'ejecucion'},context=context)
    
    def validar_registro_one2many_oferta_create(self,cr,uid,ids,pensum_ids,context=None):
        list_pensum_ids = []
        list_semestre_ids = []
        list_seccion = []
        list_asignatura = []
        for pensum in pensum_ids:
            list_pensum_ids.append(pensum[2]['pensum_id'])
            for semestre in pensum[2]['semestres_ids']:
                list_semestre_ids.append(semestre[2]['semestre_id'])
                for seccion in semestre[2]['secciones_ids']:
                    list_seccion.append(seccion[2]['seccion'])
                    for asignatura in seccion[2]['asignaturas_ids']:
                        list_asignatura.append(asignatura[2]['asignatura_id'])
                    list_asignatura_filtrada = list(set(list_asignatura))
                    if len(list_asignatura_filtrada)!=len(list_asignatura):
                        raise osv.except_osv(
                            ('Error!'),
                            (u'Usted ha seleccionado 2 veces una Asignatura para la misma Sección.'))  
                    list_asignatura=[]
                list_seccion_filtrada = list(set(list_seccion))
                if len(list_seccion_filtrada)!=len(list_seccion):
                    raise osv.except_osv(
                        ('Error!'),
                        (u'Usted ha seleccionado 2 veces una Sección para un mismo Semestre.'))  
                list_seccion=[]
            list_semestre_ids_filtrada = list(set(list_semestre_ids))
            if len(list_semestre_ids_filtrada)!=len(list_semestre_ids):
                raise osv.except_osv(
                    ('Error!'),
                    (u'Usted ha seleccionado 2 veces un Semestre para un mismo Pensum.'))  
            list_semestre_ids=[]
        list_pensum_ids_filtrado = list(set(list_pensum_ids))
        if len(list_pensum_ids_filtrado)!=len(list_pensum_ids):
            raise osv.except_osv(
                ('Error!'),
                (u'Usted ha seleccionado 2 veces un Pensum para una misma Oferta Académica.'))  
        list_pensum_ids=[]
        return True
    
    def validar_registro_one2many_vacio_oferta_create(self,cr,uid,ids,pensum_ids,context=None):
        if pensum_ids==[]:
            raise osv.except_osv(
                ('Aviso!'),
                (u'Debe seleccionar al menos un Pensum.'))
        for pensum in pensum_ids:
            if pensum[2]['semestres_ids']==[]:
                raise osv.except_osv(
                    ('Aviso!'),
                    (u'Debe seleccionar al menos un Semestre para cada Pensum.'))
            for semestre in pensum[2]['semestres_ids']:
                if 'secciones_ids' in semestre[2].keys():
                    if semestre[2]['secciones_ids']==[]:
                        raise osv.except_osv(
                            ('Aviso!'),
                            (u'Debe seleccionar al menos una Sección para cada Semestre.'))
                    for seccion in semestre[2]['secciones_ids']:
                        if seccion[2]['asignaturas_ids']==[]:
                            raise osv.except_osv(
                            ('Aviso!'),
                            (u'Debe seleccionar al menos una Asignatura para cada Sección.'))
                else:
                    raise osv.except_osv(
                        ('Aviso!'),
                        (u'Debe seleccionar al menos una Sección para cada Semestre.'))
        return True
    
    def create(self, cr, uid, vals, context=None):
        filtrar_coordinacion=self.filtrar_coordinacion_oferta_academica(cr,uid,[])
        vals.update({
            'state':'borrador',
            'coordinacion_id':filtrar_coordinacion['value']['coordinacion_id'].id,
            })
        self.validar_registro_one2many_vacio_oferta_create(cr,uid,[],vals['pensum_ids'])
        self.validar_registro_one2many_oferta_create(cr,uid,[],vals['pensum_ids'])
        return super(unefa_oferta_academica,self).create(cr,uid,vals,context=context)
        
    
    def validar_registro_one2many_vacio_oferta_write(self,cr,uid,ids,pensum_ids,context=None):
        list_pensum=[]
        list_semestre=[]
        list_seccion=[]
        list_asignatura=[]
        for pensum in pensum_ids:
            if pensum[0]!=2:
                if pensum[0]==0 or pensum[0]==1:
                    for semestre in pensum[2]['semestres_ids']:
                        if semestre[0]!=2:
                            if semestre[0]==0 or semestre[0]==1:
                                for seccion in semestre[2]['secciones_ids']:
                                    if seccion[0]!=2:
                                         if seccion[0]==0 or seccion[0]==1:
                                            if 'asignaturas_ids' in seccion[2].keys():
                                                for asignatura in seccion[2]['asignaturas_ids']:
                                                    if asignatura[0]!=2:
                                                        print True
                                                    else:
                                                        list_asignatura.append(asignatura)
                                                if len(list_asignatura)==len(seccion[2]['asignaturas_ids']):
                                                    raise osv.except_osv(
                                                        ('Aviso!'),
                                                        (u'Debe seleccionar al menos una Asignatura para cada Sección.'))
                                                list_asignatura=[]
                                    else:
                                        list_seccion.append(seccion)
                                if len(list_seccion)==len(semestre[2]['secciones_ids']):
                                    raise osv.except_osv(
                                        ('Aviso!'),
                                        (u'Debe seleccionar al menos una Sección para cada Semestre.'))
                                list_seccion=[]
                        else:
                            list_semestre.append(semestre)
                    if len(list_semestre)==len(pensum[2]['semestres_ids']):
                        raise osv.except_osv(
                        ('Aviso!'),
                        (u'Debe seleccionar al menos un Semestre para cada Pensum.'))
                    list_semestre=[]
            else:
                list_pensum.append(pensum)
        if len(list_pensum)==len(pensum_ids):
            raise osv.except_osv(
                ('Aviso!'),
                (u'Debe seleccionar al menos un Pensum.'))
        return True
    
    def validar_registro_one2many_oferta_write(self,cr,uid,ids,pensum_ids,context=None):
        list_pensum_ids = []
        list_semestre_ids = []
        list_seccion = []
        list_asignatura = []
        pensum_obj=self.pool.get('unefa.pensum_oferta_academica')
        semestre_obj=self.pool.get('unefa.oferta_academica_semestre')
        seccion_obj=self.pool.get('unefa.oferta_academica_seccion')
        asignatura_obj=self.pool.get('unefa.oferta_academica_asignatura')
        for pensum in pensum_ids:
            if pensum[0]==4:
               pensum_data=pensum_obj.browse(cr,uid,pensum[1]).pensum_id.id
               list_pensum_ids.append(pensum_data)
            if pensum[0]==0:
                list_pensum_ids.append(pensum[2]['pensum_id'])
            if pensum[0]==0 or pensum[0]==1:
                for semestre in pensum[2]['semestres_ids']:
                    if semestre[0]==4:
                       semestre_data=semestre_obj.browse(cr,uid,semestre[1]).semestre_id.id
                       list_semestre_ids.append(semestre_data)
                    if semestre[0]==0:
                        list_semestre_ids.append(semestre[2]['semestre_id'])
                    if semestre[0]==0 or semestre[0]==1:
                        for seccion in semestre[2]['secciones_ids']:
                            if seccion[0]==4:
                               seccion_data=seccion_obj.browse(cr,uid,seccion[1])
                               list_seccion.append(seccion_data['seccion'])
                            if seccion[0]==0:
                                list_seccion.append(seccion[2]['seccion'].upper())
                            if seccion[0]==1:
                                if 'seccion' in seccion[2].keys():
                                    list_seccion.append(seccion[2]['seccion'].upper())
                            if seccion[0]==0 or seccion[0]==1:
                                if 'asignaturas_ids' in seccion[2].keys():
                                    for asignatura in seccion[2]['asignaturas_ids']:
                                        if asignatura[0]==4:
                                           asignatura_data=asignatura_obj.browse(cr,uid,asignatura[1])
                                           list_asignatura.append(asignatura_data['asignatura_id'].id)
                                        if asignatura[0]==0:
                                            list_asignatura.append(asignatura[2]['asignatura_id'])
                                        if asignatura[0]==1:
                                            if 'asignatura_id' in asignatura[2].keys():
                                                list_asignatura.append(asignatura[2]['asignatura_id'])
                                    list_asignatura_filtrada = list(set(list_asignatura))
                                    if len(list_asignatura_filtrada)!=len(list_asignatura):
                                        raise osv.except_osv(
                                            ('Error!'),
                                            (u'Usted ha seleccionado 2 veces una Asignatura para la misma Sección.'))  
                                        list_asignatura=[]
                        list_seccion_filtrada = list(set(list_seccion))
                        if len(list_seccion_filtrada)!=len(list_seccion):
                            raise osv.except_osv(
                                ('Error!'),
                                (u'Usted ha seleccionado 2 veces una Sección para un mismo Semestre.'))  
                        list_seccion=[]
                list_semestre_ids_filtrada = list(set(list_semestre_ids))
                if len(list_semestre_ids_filtrada)!=len(list_semestre_ids):
                    raise osv.except_osv(
                        ('Error!'),
                        (u'Usted ha seleccionado 2 veces un Semestre para un mismo Pensum.'))  
                list_semestre_ids=[]
        list_pensum_ids_filtrado = list(set(list_pensum_ids))
        if len(list_pensum_ids_filtrado)!=len(list_pensum_ids):
            raise osv.except_osv(
                ('Error!'),
                (u'Usted ha seleccionado 2 veces un Pensum para una misma Oferta Académica.'))  
        list_pensum_ids=[]
        return True
    
    def write(self, cr, uid, ids, vals, context=None):
        if 'pensum_ids' in vals.keys():
            self.validar_registro_one2many_vacio_oferta_write(cr,uid,[],vals['pensum_ids'])
            self.validar_registro_one2many_oferta_write(cr,uid,[],vals['pensum_ids'])
        return super(unefa_oferta_academica, self).write(cr, uid, ids, vals, context=context)

class unefa_pensum_oferta_academica(osv.osv):
    _name = 'unefa.pensum_oferta_academica'
    
    _columns = {
        'oferta_id': fields.many2one('unefa.oferta_academica', 'Oferta Academica',readonly=False,ondelete='cascade',),
        'pensum_id': fields.many2one('unefa.pensum', 'Pensum',readonly=False, required=True,states={'borrador': [('readonly', True)],'ejecucion': [('readonly', True)],'aprobado': [('readonly', True)]}),
        'semestres_ids': fields.one2many('unefa.oferta_academica_semestre','pensum_oferta_id','Semestres',readonly=False, required=True,states={'aprobado': [('readonly', True)]}),
        'state': fields.selection([
            ('borrador', 'Borrador'),
            ('ejecucion', 'En Ejecución'),
            ('aprobado', 'Aprobado'),
            ],'Estado', readonly=True, copy=False, help="Este es es estado actual de la oferta académica.", select=True),
        }
    
    _defaults={
        'state':'',
        }
    
    def cargar_semestre(self, cr, uid, ids, pensum_id, context=None):
        list_semestre = []
        list_asignatura = []
        res = {}
        if pensum_id:
            objeto_pensum=self.pool.get('unefa.pensum')
            ids_pensum=objeto_pensum.search(cr,uid,[('id','=',pensum_id)])
            data_pensum=objeto_pensum.browse(cr,uid,ids_pensum)
            for pensum in data_pensum:
                for semestre in pensum.semestre_ids:
                    for asignatura in semestre.asignaturas_ids:
                        list_asignatura.append([0,False,{'asignatura_id' : asignatura.id,}])
                    semestre = semestre.id
                    list_semestre.append([0,False,{'semestre_id' : semestre}])
            res={
                'semestres_ids':list_semestre,
                }
        return {'value':res}
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'state':'borrador',
            })
        return super(unefa_pensum_oferta_academica, self).create(cr, uid, vals, context=context)
    
class unefa_oferta_academica_semestre(osv.osv):
    _name = 'unefa.oferta_academica_semestre'
    
    _columns = {
        'pensum_oferta_id': fields.many2one('unefa.pensum_oferta_academica', 'Semestres Ofertados',ondelete='cascade',readonly=False),
        'semestre_id': fields.many2one('unefa.semestre', 'Semestre',readonly=False, required=True,states={'borrador': [('readonly', True)],'ejecucion': [('readonly', True)],'aprobado': [('readonly', True)]}),
        'secciones_ids': fields.one2many('unefa.oferta_academica_seccion', 'oferta_semestre_id', 'Secciones',states={'aprobado': [('readonly', True)]}),
        'tipo_estudiante_id':fields.many2one('unefa.tipo_estudiante', 'Tipo de Estudiante',readonly=False, required=True,states={'ejecucion': [('readonly', True)],'aprobado': [('readonly', True)]}),
        'state': fields.selection([
            ('borrador', 'Borrador'),
            ('ejecucion', 'En Ejecución'),
            ('aprobado', 'Aprobado'),
            ],'Estado', readonly=True, copy=False, help="Este es es estado actual de la oferta académica.", select=True),
        }
    
    _defaults={
        'state':'',
        }
    
    def validar_existencia_pensum(self,cr,uid,ids,pensum,semestre_id,context=None):
        mensaje={}
        res={}
        if semestre_id:
            if not pensum:
                mensaje={
                    'title':('Error'),
                    'message':('Debe seleccionar un Pensum de Estudio'),
                    }
                res={'semestre_id':''}
        return {
            'warning':mensaje,
            'value':res
                }
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'state':'borrador',
            })
        return super(unefa_oferta_academica_semestre, self).create(cr, uid, vals, context=context)


class unefa_oferta_academica_seccion(osv.osv):
    _name = 'unefa.oferta_academica_seccion'
    _rec_name = 'seccion'
    
    _columns = {
        'oferta_semestre_id': fields.many2one('unefa.oferta_academica_semestre', 'Semestres Ofertados',ondelete='cascade',readonly=False),
        'seccion':fields.char('Sección',size=80,required=True, help='Aquí se coloca el nombre de la sección',states={'ejecucion': [('readonly', True)],'aprobado': [('readonly', True)]}),
        'asignaturas_ids': fields.one2many('unefa.oferta_academica_asignatura', 'oferta_asignatura_id', 'Asignaturas',states={'aprobado': [('readonly', True)]}),
        'state': fields.selection([
            ('borrador', 'Borrador'),
            ('ejecucion', 'En Ejecución'),
            ('aprobado', 'Aprobado'),
            ],'Estado', readonly=True, copy=False, help="Este es es estado actual de la oferta académica.", select=True),
        }
    
    _defaults={
        'state':'',
        }
        
    def asinatura_default(self,cr,uid,ids,semestre_id,context=None):
        list_asignatura=[]
        semestre_obj=self.pool.get('unefa.semestre')
        semestre_ids=semestre_obj.search(cr,uid,[('id','=',int(semestre_id))])
        for asignatura in semestre_obj.browse(cr,uid,semestre_ids)['asignaturas_ids']:
            list_asignatura.append([0,False,{'asignatura_id' : asignatura.id}])
        res={
            'asignaturas_ids':list_asignatura,
            }
        return {'value':res}
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'seccion':vals['seccion'].upper(),
            'state':'borrador'
            })
        return super(unefa_oferta_academica_seccion, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if 'seccion' in vals.keys():
            vals.update({
            'seccion':vals['seccion'].upper(),
            })
        return super(unefa_oferta_academica_seccion, self).write(cr, uid, ids, vals, context=context)
        
        
class unefa_oferta_academica_asignatura(osv.osv):
    _name = 'unefa.oferta_academica_asignatura'
    
    _columns = {
        'oferta_asignatura_id': fields.many2one('unefa.oferta_academica_seccion', 'Asignaturas Ofertadas',readonly=False,ondelete='cascade',states={'aprobado': [('readonly', True)]}),
        'asignatura_id': fields.many2one('unefa.asignatura', 'Asignatura',readonly=False, required=True,states={'ejecucion': [('readonly', True)],'aprobado': [('readonly', True)]}),
        'matricula':fields.integer('Matrícula Estudiantil',required=True,states={'ejecucion': [('readonly', True)],'aprobado': [('readonly', True)]},help=''),
        'profesor_id':fields.many2one('res.users', 'Profesor',readonly=False, required=True,states={'ejecucion': [('readonly', True)],'aprobado': [('readonly', True)]}),
        'state': fields.selection([
            ('borrador', 'Borrador'),
            ('ejecucion', 'En Ejecución'),
            ('aprobado', 'Aprobado'),
            ],'Estado', readonly=True, copy=False, help="Este es es estado actual de la oferta académica.", select=True),
        }
    
    _defaults={
        'state':'',
        }
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'state':'borrador',
            })
        return super(unefa_oferta_academica_asignatura, self).create(cr, uid, vals, context=context)

    
    
class unefa_oferta_modalidad(osv.osv):
    _name = 'unefa.modalidad'
    _rec_name = 'modalidad'
    
    _columns = {
        'modalidad':fields.char('Modalidad',size=80,required=True, help='Aquí se coloca el nombre de la modalidad'),
        
        }
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'modalidad':vals['modalidad'].upper(),
            })
        return super(unefa_oferta_modalidad, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'modalidad' in vals.keys():
            vals.update({'modalidad':vals['modalidad'].upper(),})
        return super(unefa_oferta_modalidad, self).write(cr, uid, ids, vals, context=context)
    

class unefa_tipo_estudiante(osv.osv):
    _name = 'unefa.tipo_estudiante'
    _rec_name = 'tipo_estudiante'
    
    _columns = {
        'tipo_estudiante':fields.char('Tipo de estudiante',size=80,required=True, help='Aquí se coloca el tipo de estudiante'),
        }
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'tipo_estudiante':vals['tipo_estudiante'].upper(),
            })
        return super(unefa_tipo_estudiante, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'tipo_estudiante' in vals.keys():
            vals.update({'tipo_estudiante':vals['tipo_estudiante'].upper(),})
        return super(unefa_tipo_estudiante, self).write(cr, uid, ids, vals, context=context)
    
