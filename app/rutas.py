import os,logging 
from os import urandom
from flask import render_template, request,url_for,redirect, send_from_directory, session
from flask_login import login_user,logout_user, current_user, login_required
#from werkzeug.exceptions import HTTPException, NotFound,abort
from jinja2 import TemplateNotFound
from flask_session import Session
from app import app, lm, db, bc, nav
from app.modelos import Roles, Users
from app.forms import login_form


@lm.user_loader
def load_user(user_id):
    return Roles.query.get(int(user_id))

nav.Bar('superadmin', [
    nav.Item('Inicio', 'pagina_superadministrador'),
    nav.Item('Agregar usuario', 'pagina_superadministrador_addUser'),
    nav.Item('Editar usuario', 'pagina_superadministrador_searchUser'),
    nav.Item('Gestion de evaluaciones', 'pagina_superadministrador_manageAudits'),
])

nav.Bar('admin', [
    nav.Item('Inicio', 'pagina_administrador'),
    nav.Item('Agregar usuario', 'pagina_administrador_addUser'),
    nav.Item('Editar usuario', 'pagina_administrador_searchUser'),
    nav.Item('Gestion de evaluaciones', 'pagina_administrador_performance'),
])

nav.Bar('empleado', [
    nav.Item('Informacion general', 'pagina_empleado'),
    nav.Item('Historial de evaluaciones', 'pagina_empleado_audits'),
])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/", methods=['GET', 'POST'])
def login():
    form = login_form(request.form)
    message=None
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        session["final_user_id"] = user_id
        pwd = request.form.get('user_pwd')
        rol = Roles.query.filter_by(identificacion=user_id).first()
        if rol:
            if rol.is_active:
                if bc.check_password_hash(rol.password,pwd):
                    if not rol.first_login:
                        if rol.perfil == "superadministrador":
                            login_user(rol)
                            return redirect(url_for('pagina_superadministrador'))
                        elif rol.perfil == "administrador":
                            login_user(rol)
                            return redirect(url_for('pagina_administrador'))
                        elif rol.perfil == "empleado":
                            login_user(rol)
                            return redirect(url_for('pagina_empleado'))
                    else: 
                        return redirect(url_for("recover_password"))
                else: 
                    message= "Usuario o contraseña incorrecto"
    return render_template("login_1.html", form=form, message=message)

@app.route("/recuperar-password", methods=['GET', 'POST'])
def recover_password():
    if request.method=='POST':
        user_id = session["final_user_id"]
        pwd = request.form.get('pwd')
        rol = Roles.query.filter_by(identificacion=user_id).first()
        if rol:
            if rol.is_active:
                pwd_hash = bc.generate_password_hash(pwd)
                rol.password = pwd_hash
                rol.first_login = False
                rol.save()
                return redirect(url_for('login'))
    return render_template("establecer_password.html")
    
@app.route("/superadministrador")
@login_required
def pagina_superadministrador():
    superadmin = session["final_user_id"]
    user=Users.query.filter_by(identificacion=superadmin).first()
    nombre=user.nombres
    return render_template("superadmin_2.html",nombre=nombre)

@app.route('/',defaults={'path':'index'})
@app.route('/<path>')
def index(path):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

@app.route("/superadministrador/agregar-usuario", methods=['GET','POST'])
def pagina_superadministrador_addUser():
    if request.method =='POST':
        num_documento=request.form.get('inputNumDocumento')
        tipo_documento=request.form.get('inputTipoDocumento').lower()
        apellido=request.form.get('inputApellidos', type=str).lower()
        nombre=request.form.get('inputNombres', type=str).lower()
        fecha_nacimiento = request.form.get('inputFechaNacimiento')
        edad=request.form.get('inputEdad')
        estado_civil=request.form.get('inputEstadoCivil').lower()
        correo_electronico=request.form.get('inputCorreoElectronico').lower()
        telefono=request.form.get('inputTelefono')
        direccion=request.form.get('inputDireccion').lower()
        barrio=request.form.get('inputBarrio').lower()
        estrato=request.form.get('inputEstrato')
        contacto_emergencia=request.form.get('inputContactoEmergencia').lower()
        telefono_contacto_emergencia=request.form.get('inputTelefonoContactoEmergencia')
        parentesco_contacto_emergencia=request.form.get('inputParentesco').lower()
        dependencia=request.form.get('inputDependencia').lower()
        cargo=request.form.get('inputCargo').lower()
        tipo_contrato=request.form.get('inputTipoContrato').lower()
        salario=request.form.get('inputSalario')
        fecha_ingreso=request.form.get('inputFechaIngreso')
        fecha_termino=request.form.get('inputFechaTermino')
        
        perfil=request.form.get('inputPerfil').lower()
        pwd_hash = bc.generate_password_hash(num_documento)
        
        user = Users(num_documento,
                    tipo_documento,
                    apellido,
                    nombre,
                    fecha_nacimiento,
                    edad,
                    estado_civil,
                    correo_electronico,
                    telefono,
                    direccion,
                    barrio,
                    estrato,
                    contacto_emergencia,
                    telefono_contacto_emergencia,
                    parentesco_contacto_emergencia,
                    dependencia,
                    cargo,
                    tipo_contrato,
                    salario,
                    fecha_ingreso,
                    fecha_termino)
        user.save()
        rol = Roles(num_documento, perfil, pwd_hash)
        rol.save()
        
    return render_template("superadmin_addUser_3.html")

@app.route("/superadministrador/buscar-usuario", methods=['GET', 'POST'])
def pagina_superadministrador_searchUser():
    if request.method == 'POST':
        searchId = request.form.get('searchId')
        session["superadmin_search_id"] = searchId
        user=Users.query.filter_by(identificacion=searchId).first()
        if user:
            Id = user.identificacion
            nombre = user.nombres
            apellido = user.apellidos
        return render_template("superadmin_buscarUsuario_4.html", Id=Id, nombre= nombre, apellido=apellido)
    return render_template("superadmin_buscarUsuario_4.html")

@app.route("/superadministrador/editar-usuario", methods=['GET', 'POST'])
def pagina_superadministrador_editUser():
    if request.method == 'POST':
        num_documento=request.form.get('inputNumDocumento')
        tipo_documento=request.form.get('inputTipoDocumento')
        apellido=request.form.get('inputApellidos', type=str).lower()
        nombre=request.form.get('inputNombres', type=str).lower()
        fecha_nacimiento = request.form.get('inputFechaNacimiento')
        edad=request.form.get('inputEdad')
        estado_civil=request.form.get('inputEstadoCivil').lower()
        correo_electronico=request.form.get('inputCorreoElectronico').lower()
        telefono=request.form.get('inputTelefono')
        direccion=request.form.get('inputDireccion').lower()
        barrio=request.form.get('inputBarrio').lower()
        estrato=request.form.get('inputEstrato')
        contacto_emergencia=request.form.get('inputContactoEmergencia').lower()
        telefono_contacto_emergencia=request.form.get('inputTelefonoContactoEmergencia')
        parentesco_contacto_emergencia=request.form.get('inputParentesco').lower()
        dependencia=request.form.get('inputDependencia').lower()
        cargo=request.form.get('inputCargo').lower()
        tipo_contrato=request.form.get('inputTipoContrato').lower()
        salario=request.form.get('inputSalario')
        fecha_ingreso=request.form.get('inputFechaIngreso')
        fecha_termino=request.form.get('inputFechaTermino')
        
        desactivar_perfil=request.form.get('desactivarUsuario')
        user=Users.query.filter_by(identificacion=num_documento).first()
        rol=Roles.query.filter_by(identificacion=num_documento).first()
        
        user.apellidos = apellido
        user.nombres = nombre
        user.estado_civil = estado_civil
        user.correo_electronico = correo_electronico
        user.telefono = telefono
        user.direccion = direccion
        user.estrato = estrato
        user.contacto_emergencia = contacto_emergencia
        user.telefono_contacto_emergencia = telefono_contacto_emergencia
        user.parentesco_contacto_emergencia = parentesco_contacto_emergencia
        user.dependencia = dependencia
        user.cargo = cargo
        user.tipo_contrato = tipo_contrato
        user.salario = salario
        user.fecha_termino = fecha_termino
        
        user.save()
        if desactivar_perfil == 'on':
            rol.is_active = False
            rol.save()
        return render_template("superadmin_buscarUsuario_4.html")
    editId = session["superadmin_search_id"]
    user=Users.query.filter_by(identificacion=editId).first()
    Id = user.identificacion
    apellidos = user.apellidos
    nombres = user.nombres
    tipo_documento = user.tipo_documento
    fecha_nacimiento = user.fecha_nacimiento
    edad = user.edad
    estado_civil = user.estado_civil
    correo_electronico = user.correo_electronico
    telefono = user.telefono
    direccion = user.direccion
    barrio = user.barrio
    estrato = user.estrato
    contacto_emergencia = user.contacto_emergencia
    telefono_contacto_emergencia = user.telefono_contacto_emergencia
    parentesco_contacto_emergencia = user.parentesco_contacto_emergencia
    dependencia = user.dependencia
    cargo = user.cargo
    tipo_contrato = user.tipo_contrato
    salario = user.salario
    fecha_ingreso = user.fecha_ingreso
    fecha_termino = user.fecha_termino
    return render_template("superadmin_editUser_5.html",
                        Id=Id,
                        apellidos=apellidos,
                        nombres=nombres,
                        tipo_documento=tipo_documento,
                        fecha_nacimiento=fecha_nacimiento,
                        edad=edad,
                        estado_civil=estado_civil,
                        correo_electronico=correo_electronico,
                        telefono=telefono,
                        direccion=direccion,
                        barrio=barrio,
                        estrato=estrato,
                        contacto_emergencia=contacto_emergencia,
                        telefono_contacto_emergencia=telefono_contacto_emergencia,
                        parentesco_contacto_emergencia=parentesco_contacto_emergencia,
                        dependencia=dependencia,
                        cargo=cargo,
                        tipo_contrato=tipo_contrato,
                        salario=salario,
                        fecha_ingreso=fecha_ingreso,
                        fecha_termino=fecha_termino)

@app.route("/superadministrador/gestionar-evaluaciones")
def pagina_superadministrador_manageAudits():
    return render_template("superadmin_gestiónEvaluaciones_6.html")

@app.route("/administrador")
@login_required
def pagina_administrador():
    admin=session["final_user_id"]
    user=Users.query.filter_by(identificacion=admin).first()
    nombre=user.nombres
    return render_template("admin_7.html", nombre=nombre)

@app.route("/administrador/agregar-usuario", methods=['GET', 'POST'])
def pagina_administrador_addUser():
    if request.method =='POST':
        num_documento=request.form.get('inputNumDocumento')
        tipo_documento=request.form.get('inputTipoDocumento')
        apellido=request.form.get('inputApellidos', type=str).lower()
        nombre=request.form.get('inputNombres', type=str).lower()
        fecha_nacimiento = request.form.get('inputFechaNacimiento')
        edad=request.form.get('inputEdad')
        estado_civil=request.form.get('inputEstadoCivil').lower()
        correo_electronico=request.form.get('inputCorreoElectronico').lower()
        telefono=request.form.get('inputTelefono')
        direccion=request.form.get('inputDireccion').lower()
        barrio=request.form.get('inputBarrio').lower()
        estrato=request.form.get('inputEstrato')
        contacto_emergencia=request.form.get('inputContactoEmergencia').lower()
        telefono_contacto_emergencia=request.form.get('inputTelefonoContactoEmergencia')
        parentesco_contacto_emergencia=request.form.get('inputParentesco').lower()
        dependencia=request.form.get('inputDependencia').lower()
        cargo=request.form.get('inputCargo').lower()
        tipo_contrato=request.form.get('inputTipoContrato').lower()
        salario=request.form.get('inputSalario')
        fecha_ingreso=request.form.get('inputFechaIngreso')
        fecha_termino=request.form.get('inputFechaTermino')
        
        perfil=request.form.get('inputPerfil')
        pwd_hash = bc.generate_password_hash(num_documento)
        
        user = Users(num_documento,
                    tipo_documento,
                    apellido,
                    nombre,
                    fecha_nacimiento,
                    edad,
                    estado_civil,
                    correo_electronico,
                    telefono,
                    direccion,
                    barrio,
                    estrato,
                    contacto_emergencia,
                    telefono_contacto_emergencia,
                    parentesco_contacto_emergencia,
                    dependencia,
                    cargo,
                    tipo_contrato,
                    salario,
                    fecha_ingreso,
                    fecha_termino)
        user.save()
        rol = Roles(num_documento, perfil, pwd_hash)
        rol.save()
    return render_template("admin_addUser_8.html")

@app.route("/administrador/buscar-usuario", methods=['GET', 'POST'])
def pagina_administrador_searchUser():
    if request.method == 'POST':
        searchId = request.form.get('searchId')
        session["admin_search_id"] = searchId
        user=Users.query.filter_by(identificacion=searchId).first()
        if user:
            Id = user.identificacion
            nombre = user.nombres
            apellido = user.apellidos
        return render_template("admin_buscarUsuario_9.html", Id=Id, nombre= nombre, apellido=apellido)
    return render_template("admin_buscarUsuario_9.html")

@app.route("/administrador/editar-usuario", methods=['GET', 'POST'])
def pagina_administrador_editUser():
    if request.method == 'POST':
        num_documento=request.form.get('inputNumDocumento')
        tipo_documento=request.form.get('inputTipoDocumento')
        apellido=request.form.get('inputApellidos', type=str).lower()
        nombre=request.form.get('inputNombres', type=str).lower()
        fecha_nacimiento = request.form.get('inputFechaNacimiento')
        edad=request.form.get('inputEdad')
        estado_civil=request.form.get('inputEstadoCivil').lower()
        correo_electronico=request.form.get('inputCorreoElectronico').lower()
        telefono=request.form.get('inputTelefono')
        direccion=request.form.get('inputDireccion').lower()
        barrio=request.form.get('inputBarrio').lower()
        estrato=request.form.get('inputEstrato')
        contacto_emergencia=request.form.get('inputContactoEmergencia').lower()
        telefono_contacto_emergencia=request.form.get('inputTelefonoContactoEmergencia')
        parentesco_contacto_emergencia=request.form.get('inputParentesco').lower()
        dependencia=request.form.get('inputDependencia').lower()
        cargo=request.form.get('inputCargo').lower()
        tipo_contrato=request.form.get('inputTipoContrato').lower()
        salario=request.form.get('inputSalario')
        fecha_ingreso=request.form.get('inputFechaIngreso')
        fecha_termino=request.form.get('inputFechaTermino')
        
        user=Users.query.filter_by(identificacion=num_documento).first()
        
        user.apellidos = apellido
        user.nombres = nombre
        user.estado_civil = estado_civil
        user.correo_electronico = correo_electronico
        user.telefono = telefono
        user.direccion = direccion
        user.estrato = estrato
        user.contacto_emergencia = contacto_emergencia
        user.telefono_contacto_emergencia = telefono_contacto_emergencia
        user.parentesco_contacto_emergencia = parentesco_contacto_emergencia
        user.dependencia = dependencia
        user.cargo = cargo
        user.tipo_contrato = tipo_contrato
        user.salario = salario
        user.fecha_termino = fecha_termino
        
        user.save()
        return render_template("admin_buscarUsuario_9.html")
    editId = session["admin_search_id"]
    user=Users.query.filter_by(identificacion=editId).first()
    Id = user.identificacion
    apellidos = user.apellidos
    nombres = user.nombres
    tipo_documento = user.tipo_documento
    fecha_nacimiento = user.fecha_nacimiento
    edad = user.edad
    estado_civil = user.estado_civil
    correo_electronico = user.correo_electronico
    telefono = user.telefono
    direccion = user.direccion
    barrio = user.barrio
    estrato = user.estrato
    contacto_emergencia = user.contacto_emergencia
    telefono_contacto_emergencia = user.telefono_contacto_emergencia
    parentesco_contacto_emergencia = user.parentesco_contacto_emergencia
    dependencia = user.dependencia
    cargo = user.cargo
    tipo_contrato = user.tipo_contrato
    salario = user.salario
    fecha_ingreso = user.fecha_ingreso
    fecha_termino = user.fecha_termino
    return render_template("admin_editUser_10.html",
                        Id=Id,
                        apellidos=apellidos,
                        nombres=nombres,
                        tipo_documento=tipo_documento,
                        fecha_nacimiento=fecha_nacimiento,
                        edad=edad,
                        estado_civil=estado_civil,
                        correo_electronico=correo_electronico,
                        telefono=telefono,
                        direccion=direccion,
                        barrio=barrio,
                        estrato=estrato,
                        contacto_emergencia=contacto_emergencia,
                        telefono_contacto_emergencia=telefono_contacto_emergencia,
                        parentesco_contacto_emergencia=parentesco_contacto_emergencia,
                        dependencia=dependencia,
                        cargo=cargo,
                        tipo_contrato=tipo_contrato,
                        salario=salario,
                        fecha_ingreso=fecha_ingreso,
                        fecha_termino=fecha_termino)

@app.route("/administrador/performance")
def pagina_administrador_performance():
    return render_template("admin_desempeñoEmpleados_11.html")

@app.route("/administrador/cargar-evaluaciones")
def pagina_administrador_loadAudits():
    return render_template("admin_loadAudit_15.html")

@app.route("/administrador/evaluar-empleado")
def pagina_administrador_assessEmployee():
    return render_template("admin_assessEmployee_16.html")

@app.route("/empleado/informacion")
@login_required
def pagina_empleado():
    final_user_id = session["final_user_id"]
    user=Users.query.filter_by(identificacion=final_user_id).first()
    Id = user.identificacion
    apellidos = user.apellidos
    nombres = user.nombres
    tipo_documento = user.tipo_documento
    fecha_nacimiento = user.fecha_nacimiento
    edad = user.edad
    estado_civil = user.estado_civil
    correo_electronico = user.correo_electronico
    telefono = user.telefono
    direccion = user.direccion
    barrio = user.barrio
    estrato = user.estrato
    contacto_emergencia = user.contacto_emergencia
    telefono_contacto_emergencia = user.telefono_contacto_emergencia
    parentesco_contacto_emergencia = user.parentesco_contacto_emergencia
    dependencia = user.dependencia
    cargo = user.cargo
    tipo_contrato = user.tipo_contrato
    salario = user.salario
    fecha_ingreso = user.fecha_ingreso
    fecha_termino = user.fecha_termino
    return render_template("finalUser_12.html",
                        Id=Id,
                        apellidos=apellidos,
                        nombres=nombres,
                        tipo_documento=tipo_documento,
                        fecha_nacimiento=fecha_nacimiento,
                        edad=edad,
                        estado_civil=estado_civil,
                        correo_electronico=correo_electronico,
                        telefono=telefono,
                        direccion=direccion,
                        barrio=barrio,
                        estrato=estrato,
                        contacto_emergencia=contacto_emergencia,
                        telefono_contacto_emergencia=telefono_contacto_emergencia,
                        parentesco_contacto_emergencia=parentesco_contacto_emergencia,
                        dependencia=dependencia,
                        cargo=cargo,
                        tipo_contrato=tipo_contrato,
                        salario=salario,
                        fecha_ingreso=fecha_ingreso,
                        fecha_termino=fecha_termino)

@app.route("/empleado/evaluaciones")
def pagina_empleado_audits():
    return render_template("finalUser_evaluacion_13.html")