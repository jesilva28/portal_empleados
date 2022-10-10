from app import db 
from flask_login import UserMixin

class Roles(db.Model, UserMixin):
    __tablename__ = 'Roles'
    
    id = db.Column(db.Integer, primary_key=True)
    identificacion=db.Column(db.String(64), unique=True)
    perfil=db.Column(db.String(120))
    password= db.Column(db.String(500))
    is_active= db.Column(db.Boolean, default=True)
    first_login= db.Column(db.Boolean, default=True)

    def __init__(self, identificacion,perfil,password):
        self.identificacion= identificacion
        self.password = password
        self.perfil= perfil

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

class Users(db.Model, UserMixin):
    __tablename_ = 'Users'
    
    identificacion = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    tipo_documento = db.Column(db.String(64), nullable=False)
    apellidos = db.Column(db.String(64), nullable=False)
    nombres = db.Column(db.String(64), nullable=False)
    fecha_nacimiento = db.Column(db.String(64), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    estado_civil = db.Column(db.String(64), nullable=False)
    correo_electronico = db.Column(db.String(64), unique=True, nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    barrio = db.Column(db.String(64), nullable=False)
    estrato = db.Column(db.Integer, nullable=False)
    contacto_emergencia = db.Column(db.String(64), nullable=False)
    telefono_contacto_emergencia = db.Column(db.Integer, nullable=False)
    parentesco_contacto_emergencia = db.Column(db.String(64), nullable=False)
    dependencia = db.Column(db.String(64), nullable=False)
    cargo = db.Column(db.String(64), nullable = False)
    tipo_contrato = db.Column(db.String(64), nullable = False)
    salario = db.Column(db.Float, nullable=False)
    fecha_ingreso = db.Column(db.String(64), nullable=False)
    fecha_termino = db.Column(db.String(64))
    
    def __init__(self, identificacion,tipo_documento,apellidos,nombres,fecha_nacimiento,edad,estado_civil,correo_electronico,telefono,direccion,barrio,estrato,contacto_emergencia,telefono_contacto_emergencia,parentesco_contacto_emergencia,dependencia,cargo,tipo_contrato,salario,fecha_ingreso,fecha_termino):
        self.identificacion= identificacion
        self.tipo_documento = tipo_documento
        self.apellidos = apellidos
        self.nombres = nombres
        self.fecha_nacimiento = fecha_nacimiento
        self.edad = edad
        self.estado_civil = estado_civil
        self.correo_electronico = correo_electronico
        self.telefono = telefono
        self.direccion = direccion
        self.barrio = barrio
        self.estrato = estrato
        self.contacto_emergencia = contacto_emergencia
        self.telefono_contacto_emergencia = telefono_contacto_emergencia
        self.parentesco_contacto_emergencia = parentesco_contacto_emergencia
        self.dependencia = dependencia
        self.cargo = cargo
        self.tipo_contrato = tipo_contrato
        self.salario = salario
        self.fecha_ingreso = fecha_ingreso
        self.fecha_termino = fecha_termino
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self