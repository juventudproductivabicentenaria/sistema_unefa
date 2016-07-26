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

from openerp.osv import fields, osv
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import * 
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import re


    #~ metodo que filtra las carreras y regimen dependiendo 
    #~ de la coordinacion en la cual se inscribi el estudiante


def filtrar_carreras_regimen_general(self,cr,uid,ids,context=None):
    objeto_users=self.pool.get('res.users')
    id_users=objeto_users.search(cr,uid,[('id','=',uid)])
    data_users=objeto_users.browse(cr,uid,id_users)
    value={}
    value={
        'carrera_id':data_users['coordinacion_id'].carrera_id,
        'regimen':data_users['coordinacion_id'].regimen,
        }
    return {'value':value}

    #~ metodo para establecer por defecto el rol de un usuario dependiendo de su tipo

def rol_usuario_default_general (self,cr,uid,ids,tipo_usuario,group,context=None):
    objeto_res_groups=self.pool.get('res.groups')
    id_res_groups=objeto_res_groups.search(cr,uid,[('name','=',tipo_usuario)])
    data_res_groups=objeto_res_groups.browse(cr,uid,id_res_groups)
    group_usuario={}
    result=[]
    dataobj = self.pool.get('ir.model.data')
    dummy,group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'base', 'group_user')
    result.append(group_id)
    dummy,group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'base', 'group_partner_manager')
    result.append(group_id)
    if data_res_groups['name']==tipo_usuario:
        dummy,group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'unefa_configuracion', group)
        result.append(group_id)
        group_usuario={'groups_id':[[6, False, result]]}
        return {'value':group_usuario}


    #~ metodo general para el rec_name (nombre, segundo nombre, primer 
    #~ apellido y segundo apellido)de todos los tipos de usuario

def name_get_general(self, cr, uid, ids, context=None):
        res = []
        for records in self.browse(cr, uid, ids):
            if records.is_estudiante or records.is_profesor or records.is_coordinador or records.is_asistente: 
                if records.segundo_nombre!=False and records.segundo_apellido!=False:
                    res.append((records.id, records.primer_apellido + ' ' + records.segundo_apellido + ' ' + records.name + ' ' + records.segundo_nombre))
                else:
                    if records.segundo_nombre==False and records.segundo_apellido!=False:
                        res.append((records.id, records.primer_apellido + ' ' + records.segundo_apellido + ' ' + records.name))
                    elif records.segundo_nombre!=False and records.segundo_apellido==False:
                        res.append((records.id, records.primer_apellido + ' ' + records.name + ' ' + records.segundo_nombre))
                    else:
                        res.append((records.id, records.primer_apellido + ' ' + records.name))
            else:
                res.append((records.id, records.name))
        return res


        #~ metodo para validar que la fecha de nacimiento sea menor a la fecha de hoy


def validar_fecha_nacimiento_general(fecha_nacimiento):
        mensaje={}
        fechas = {}
        fecha_actual = date.today()
        if fecha_nacimiento:
            fecha_nacimiento=datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
            fecha_nacimiento =datetime.date(fecha_nacimiento)
            if cmp(fecha_nacimiento, fecha_actual) == 1 or cmp(fecha_nacimiento, fecha_actual) == 0:
                    mensaje={
                        'title':('Error de fecha'),
                        'message':('La fecha de nacimiento no puede ser mayor\
                                    o igual a la fecha de hoy.'),
                        }
                    fechas={
                        'fecha_nacimiento':'',
                        }
            
        return {
            'warning':mensaje,
            'value':fechas
                }

class unefa_usuarios(osv.osv):

    _name='res.users'
    _inherit = 'res.users'
    
    def name_get(self, cr, uid, ids, context=None):
        return name_get_general(self, cr, uid, ids) 
    
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)
    
    _columns = {
        'segundo_nombre':fields.char('Segundo Nombre', required=False, size=30),
        'primer_apellido':fields.char('Primer Apellido', required=True, size=30),
        'segundo_apellido':fields.char('Segundo Apellido', required=False, size=30),
        'is_estudiante':fields.boolean('Estudiante'),
        'is_profesor':fields.boolean('Profesor'),
        'is_coordinador':fields.boolean('Coordinador'),
        'is_asistente':fields.boolean('Asistente'),
        'nacionalidad':fields.selection([('extranjero','Extranjero'),('venezolano','Venezolano')],'Nacionalidad', required=True),
        'cedula':fields.char('Cédula', required=True, size=15),
        'telefono_local':fields.char('Teléfono Local', required=False),
        'telefono':fields.char('Teléfono Celular', required=True),
        'fecha_nacimiento':fields.date('Fecha de Nacimiento', required=True),
        'estado_civil':fields.selection([('soltero','Soltero'),('casado','Casado'),('divorciado','Divorciado'),('viudo','Viudo')],'Estado Civil', required=True),
        'sexo':fields.selection([('masculino','Masculino'),('femenino','Femenino')],'Sexo', required=True),
        'condicion':fields.selection([('civil','Civil'),('militar','Militar')],'Condición', required=True),
        'grado_id':fields.many2one('unefa.grado_militar','Grado Militar', required=False),
        'fuerza_id':fields.many2one('unefa.fuerza_militar','Fuerza', required=False),
        'carrera_id':fields.many2one('unefa.carrera','Carrera', required=True,),
        'regimen':fields.selection([('nocturno','Nocturno'),('diurno','Diurno')],'Turno', required=True,),
        'estado_id':fields.many2one('unefa.estados','Estado', required=True),
        'municipio_id':fields.many2one('unefa.municipios','Municipio', required=True),
        'parroquia_id':fields.many2one('unefa.parroquias','Parroquia', required=True),
        'sector':fields.char('Sector', required=True, size=80),
        'calle_avenida':fields.char('Calle/Avenida', required=True, size=80),
        'casa_apto':fields.char('Casa/Apto', required=True, size=80),
        'fecha_ingreso':fields.date('Fecha de Ingreso', required=True),
        'coordinacion_id':fields.many2one('unefa.coordinacion','Coordinación', required=True,),
        'condicion_id':fields.many2one('unefa.condicion_profesor','Condición', required=True),
        'dedicacion_id':fields.many2one('unefa.dedicacion_profesor','Dedicación', required=True),
        'categoria_id':fields.many2one('unefa.categoria_profesor','Categoría', required=True),
        'nombre_completo':fields.function(_name_get_fnc, 'Nombre Completo',type="char",),
        'materias_ids':fields.many2many('unefa.asignatura','unefa_profesor_materia', 'profesor_id','materia_id', 'Materias'),
        
        }
    
    _sql_constraints = [
        ('cedula_uniq', 'unique(cedula)', 'La Cédula Ingresada, ya se encuentra Registrada'),
        ]
    
    #~ _order = 'create_date desc, id desc'
        
    def validar_email(self, cr, uid, vals, context=None):
        login = vals['login'].strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", login):
                raise osv.except_osv(('Correo Incorrecto'),
            (u'''Formato de correo incorrecto.\n %s  ''' % (login)))
        return
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'name':vals['name'].upper(),
            'primer_apellido':vals['primer_apellido'].upper(),
            'sector':vals['sector'].upper(),
            'calle_avenida':vals['calle_avenida'].upper(),
            'casa_apto':vals['casa_apto'].upper(),
            })
        if vals['segundo_nombre'] != False:
            vals.update({
                'segundo_nombre':vals['segundo_nombre'].upper(),
                })
        if vals['segundo_apellido'] != False:
            vals.update({
                'segundo_apellido':vals['segundo_apellido'].upper(),
                })
        
        self.validar_email(cr,uid,vals,context)
        return super(unefa_usuarios, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'name' in vals.keys():
            vals.update({'name':vals['name'].upper(),})
        if 'segundo_nombre' in vals.keys():
            vals.update({'segundo_nombre':vals['segundo_nombre'].upper(),})
        if 'primer_apellido' in vals.keys():
            vals.update({'primer_apellido':vals['primer_apellido'].upper(),})
        if 'segundo_apellido' in vals.keys():
            vals.update({'segundo_apellido':vals['segundo_apellido'].upper(),})
        if 'sector' in vals.keys():
            vals.update({'sector':vals['sector'].upper(),})
        if 'calle_avenida' in vals.keys():
            vals.update({'calle_avenida':vals['calle_avenida'].upper(),})
        if 'casa_apto' in vals.keys():
            vals.update({'casa_apto':vals['casa_apto'].upper(),})
        if 'login' in vals.keys():
            self.validar_email(cr,uid,vals,context)
        return super(unefa_usuarios, self).write(cr, uid, ids, vals, context=context)
        
            
class unefa_usuarios_coordinador(osv.osv):
    
    _name='unefa.usuario_coordinador'
    _inherits = {'res.users':'user_id'}
        
    def name_get(self, cr, uid, ids, context=None):
        return name_get_general(self, cr, uid, ids, context=context)   
    
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)
    
    
    _columns = {
        'user_id': fields.many2one('res.users','Pensum', required=True),
        'nombre_completo':fields.function(_name_get_fnc, 'Nombre Completo',type="char",),
        }
    
    _defaults={
        'is_coordinador':True,
        }
    
    #~ _order = 'create_date desc, id desc'
    
    def validar_fecha_nacimiento(self,cr,uid,ids,fecha_nacimiento,context=None):
        return validar_fecha_nacimiento_general(fecha_nacimiento)
    
    def on_change_login(self, cr, uid, ids, login, context=None):
        if login:
            users_obj=self.pool.get('res.users')
            users_id=users_obj.on_change_login(cr,uid,ids,login,context)
            return users_id
    
    def rol_usuario_default (self,cr,uid,ids,tipo_usuario,context=None):
        return rol_usuario_default_general (self,cr,uid,ids,tipo_usuario,'group_unefa_coordinador')
    
    def cp_limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}
        
    def carrera_default(self,cr,uid,ids,coordinacion_id,context=None):
        coordinacion_obj=self.pool.get('unefa.coordinacion')
        coordinacion_ids=coordinacion_obj.search(cr,uid,[('id','=',coordinacion_id)])
        coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_ids)
        val={
            'carrera_id':coordinacion_data['carrera_id']
            }
        return{'value':val}
    
            
    def create(self,cr,uid,vals,context=None):
        objeto_users=self.pool.get('res.users')
        users_id=objeto_users.search(cr,uid,[('coordinacion_id','=',vals['coordinacion_id'])])
        data_users=objeto_users.browse(cr,uid,users_id)
        for coordinador in data_users:
            if coordinador.is_coordinador == True and coordinador.active == True:
                raise osv.except_osv(
                    ('Aviso!'),
                    (u'Ya existe un coordinador asignado a la coordinación seleccionada.')) 
        return super(unefa_usuarios_coordinador,self).create(cr,uid,vals,context=context)
    
        
        
class unefa_usuarios_asistente(osv.osv):

    _name='unefa.usuario_asistente'
    _inherits = {'res.users':'user_id'}
    
    def name_get(self, cr, uid, ids, context=None):
        return name_get_general(self, cr, uid, ids)   
        
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)
    
    _columns = {
        'user_id': fields.many2one('res.users','Pensum', required=True),
        'nombre_completo':fields.function(_name_get_fnc, 'Nombre Completo',type="char",),
        }
    
    _defaults={
        'is_asistente':True,
        }
    
    #~ _order = 'create_date desc, id desc'
        
    def validar_fecha_nacimiento(self,cr,uid,ids,fecha_nacimiento,context=None):
        return validar_fecha_nacimiento_general(fecha_nacimiento)
    
    def on_change_login(self, cr, uid, ids, login, context=None):
        users_obj=self.pool.get('res.users')
        users_id=users_obj.on_change_login(cr,uid,ids,login,context)
        return users_id
        
    def rol_usuario_default (self,cr,uid,ids,tipo_usuario,context=None):
        return rol_usuario_default_general (self,cr,uid,ids,tipo_usuario,'group_unefa_asistente')
        
    def coordinacion_default (self,cr,uid,ids,context=None):
        value={}
        usuario_obj=self.pool.get('res.users')
        usuario_data=usuario_obj.browse(cr,uid,uid)
        coordinacion_obj=self.pool.get('unefa.coordinacion')
        list_name=[]
        for u in usuario_data['groups_id']:
           list_name.append(u.name)
        if 'Coordinador' in list_name:
            coordinacion_ids=coordinacion_obj.search(cr,uid,[('id','=',usuario_data['coordinacion_id'].id)])
            coordinacion_data=coordinacion_obj.browse(cr,uid,coordinacion_ids)
            value={
                'coordinacion_id':usuario_data['coordinacion_id'],
                'carrera_id':coordinacion_data['carrera_id'],
                }
            return {'value':value}
    
    def filtrar_carreras_regimen(self,cr,uid,ids,context=None):
        return filtrar_carreras_regimen_general(self,cr,uid,ids)

    def cp_limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}
        
    def create(self,cr,uid,vals,context=None):
        filtro_carrera=self._get_default_presupuesto(cr,uid,[])
        
        vals.update({
            'coordinacion_id':filtro_carrera['value']['coordinacion_id'].id,
            })
        return super(unefa_usuarios_asistente,self).create(cr,uid,vals,context=context)
        
class unefa_usuarios_estudiante(osv.osv):

    _name='unefa.usuario_estudiante'
    _inherits = {'res.users':'user_id'}
    
    def name_get(self, cr, uid, ids, context=None):
        return name_get_general(self, cr, uid, ids)   
    
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)
    
    _columns = {
        'user_id': fields.many2one('res.users','Pensum', required=True),
        'pensum_id': fields.many2one('unefa.pensum','Pensum', required=True),
        'nombre_completo':fields.function(_name_get_fnc, 'Nombre Completo',type="char",),
        'is_comandante_curso':fields.boolean('Comandante de Curso'),
        }

    
    _defaults={
        'is_estudiante':True,
        'is_comandante_curso':False,
        }
    
    #~ _order = 'create_date desc, id desc'
    
    
    def descargar_historial_notas(self,cr,uid,ids,context=None):
        url='/descargar/historial_notas/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
    
    def validar_fecha_nacimiento(self,cr,uid,ids,fecha_nacimiento,context=None):
        return validar_fecha_nacimiento_general(fecha_nacimiento)
    
    def on_change_login(self, cr, uid, ids, login, context=None):
        users_obj=self.pool.get('res.users')
        users_id=users_obj.on_change_login(cr,uid,ids,login,context)
        return users_id
    
    def rol_usuario_default (self,cr,uid,ids,tipo_usuario,context=None):
        return rol_usuario_default_general (self,cr,uid,ids,tipo_usuario,'group_unefa_estudiantes')
    
    def filtrar_carreras_regimen(self,cr,uid,ids,context=None):
        return filtrar_carreras_regimen_general(self,cr,uid,ids)
    
    def cp_limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}
    
    def crear_ficha_estudiante(self,cr,uid,ids,context=None):
        url='/descargar/ficha_estudiante/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
    def create(self,cr,uid,vals,context=None):
        filtro_carrera=filtrar_carreras_regimen_general(self,cr,uid,[])
        vals.update({
            'carrera_id':filtro_carrera['value']['carrera_id'].id,
            'regimen':filtro_carrera['value']['regimen'],
            })
        return super(unefa_usuarios_estudiante,self).create(cr,uid,vals,context=context)
        

class unefa_usuarios_profesor(osv.osv):

    _name='unefa.usuario_profesor'
    _inherits = {'res.users':'user_id'}
    
    def name_get(self, cr, uid, ids, context=None):
        return name_get_general(self, cr, uid, ids)   
    
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)
    
    _columns = {
        'user_id':fields.many2one('res.users','Pensum', required=True),
        'nombre_completo':fields.function(_name_get_fnc, 'Nombre Completo',type="char",),
        }
    
    _defaults={
        'is_profesor':True,
        }
        
    #~ _order = 'create_date desc, id desc'
    
    def validar_fecha_nacimiento(self,cr,uid,ids,fecha_nacimiento,context=None):
        return validar_fecha_nacimiento_general(fecha_nacimiento)
    
    def on_change_login(self, cr, uid, ids, login, context=None):
        users_obj=self.pool.get('res.users')
        users_id=users_obj.on_change_login(cr,uid,ids,login,context)
        return users_id
    
    def rol_usuario_default (self,cr,uid,ids,tipo_usuario,context=None):
        return rol_usuario_default_general (self,cr,uid,ids,tipo_usuario,'group_unefa_profesores')
    
        
    def filtrar_carreras_regimen(self,cr,uid,ids,context=None):
        return filtrar_carreras_regimen_general(self,cr,uid,ids)

    def cp_limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}
    
    def crear_ficha_profesores(self,cr,uid,ids,context=None):
        url='/descargar/ficha_profesor/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
    
    def create(self,cr,uid,vals,context=None):
        filtro_carrera=filtrar_carreras_regimen_general(self,cr,uid,[])
        vals.update({
            'carrera_id':filtro_carrera['value']['carrera_id'].id,
            'regimen':filtro_carrera['value']['regimen'],
            })
        return super(unefa_usuarios_profesor,self).create(cr,uid,vals,context=context)
    
class unefa_condicion_profesor(osv.osv):
    _name='unefa.condicion_profesor'
    _rec_name = 'condicion'
    
    _columns = {
        'condicion':fields.char('Condición',size=80,required=True, help='Aquí se coloca la condición del Profesor'),
        }
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'condicion':vals['condicion'].upper(),
            })
        return super(unefa_condicion_profesor, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'condicion' in vals.keys():
            vals.update({'condicion':vals['condicion'].upper(),})
        return super(unefa_condicion_profesor, self).write(cr, uid, ids, vals, context=context)
    
class unefa_dedicacion_profesor(osv.osv):
    _name='unefa.dedicacion_profesor'
    _rec_name = 'dedicacion'
    
    _columns = {
        'dedicacion':fields.char('Dedicación',size=80,required=True, help='Aquí se coloca el tiempo de dedicación del Profesor'),
        'cant_horas':fields.integer('Cantidad de Horas',size=80,required=True, help='Aquí se coloca la cantidad de horas laborables del profesor'),
        }
    
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'dedicacion':vals['dedicacion'].upper(),
            })
        return super(unefa_dedicacion_profesor, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'dedicacion' in vals.keys():
            vals.update({'dedicacion':vals['dedicacion'].upper(),})
        return super(unefa_dedicacion_profesor, self).write(cr, uid, ids, vals, context=context)
    
class unefa_categoria_profesor(osv.osv):
    _name='unefa.categoria_profesor'
    _rec_name = 'categoria'
    
    _columns = {
        'categoria':fields.char('Categoría',size=80,required=True, help='Aquí se coloca el la categoría del Profesor'),
        }
    
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'categoria':vals['categoria'].upper(),
            })
        return super(unefa_categoria_profesor, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'categoria' in vals.keys():
            vals.update({'categoria':vals['categoria'].upper(),})
        return super(unefa_categoria_profesor, self).write(cr, uid, ids, vals, context=context)
    
