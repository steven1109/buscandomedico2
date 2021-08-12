CREATE TABLE pais
( 
	id_pais              integer PRIMARY KEY AUTO_INCREMENT ,
	cod_pais             varchar(10)  NOT NULL ,
	des_pais             varchar(100)  NOT NULL ,
	fec_creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  default NULL 
);

CREATE TABLE departamento
( 
	id_departamento      integer PRIMARY KEY AUTO_INCREMENT ,
	cod_departamento     varchar(10)  NOT NULL ,
	des_departamento     varchar(100)  NOT NULL ,
	fec_creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  default NULL ,
	id_pais              integer  NOT NULL 
);

CREATE TABLE provincia
( 
	id_provincia         integer PRIMARY KEY AUTO_INCREMENT ,
	id_departamento      integer  NOT NULL ,
	cod_provincia        varchar(10)  NULL ,
	cod_departamento     varchar(10)  NOT NULL ,
	des_provincia        varchar(100)  NOT NULL ,
	fec_Creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  default NULL
);

CREATE TABLE distrito
( 
	id_distrito          integer PRIMARY KEY AUTO_INCREMENT ,
	id_provincia         integer  NOT NULL ,
	id_departamento      integer  NOT NULL ,
	cod_provincia        varchar(10)  NOT NULL ,
	cod_distrito         varchar(10)  NOT NULL ,
	cod_departamento     varchar(10)  NOT NULL ,
	des_distrito         varchar(100)  NOT NULL ,
	fec_creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  default NULL
);

CREATE TABLE especialidad
( 
	id_especialidad      INTEGER PRIMARY KEY AUTO_INCREMENT ,
	des_especialidad     varchar(250)  NOT NULL ,
	bol_activo			 boolean NOT NULL ,
	fec_creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  defaultault NULL
);

CREATE TABLE plan
( 
	id_plan              INTEGER PRIMARY KEY AUTO_INCREMENT ,
	desc_plan            varchar(50)  NOT NULL ,
	fec_Creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  default NULL 
);

CREATE TABLE tipo_documento
( 
	id_documento         integer PRIMARY KEY AUTO_INCREMENT ,
	des_tipodocumento    varchar(100)  NOT NULL ,
	fec_creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  default NULL 
);

CREATE TABLE prospecto
( 
	id_prospecto         integer PRIMARY KEY AUTO_INCREMENT ,
	nombres              varchar(100)  NOT NULL ,
	ape_paterno          varchar(100)  NOT NULL ,
	ape_materno          varchar(100)  NOT NULL ,
	fec_nacimiento       datetime  NOT NULL ,
	genero               integer  NOT NULL ,
	num_contacto         varchar(15)  NOT NULL ,
	email_contacto       varchar(100)  NOT NULL ,
	comentario_duda      varchar(500)  NOT NULL ,
	hora_comunicacion    varchar(100)  NOT NULL ,
	fec_creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  default NULL 
);

CREATE TABLE paciente
( 
	id_paciente          INTEGER PRIMARY KEY AUTO_INCREMENT ,
	paciente_dni         char(18)  NULL ,
	paciente_nombres     char(18)  NULL ,
	paciente_genero      char(18)  NULL ,
	paciente_edad        char(18)  NULL ,
	contacto_email       char(18)  NULL ,
	contacto_telefono    char(18)  NULL ,
	comentario_paciente  char(18)  NULL ,
	fec_creacion         datetime NOT  NULL ,
	fec_modificacion     datetime  default NULL
);

CREATE TABLE medico
( 
	id_medico					integer PRIMARY KEY AUTO_INCREMENT ,
	cod_distrito				varchar(10) NOT NULL ,
	cod_provincia				varchar(10) NOT NULL ,
	cod_departamento			varchar(10) NOT NULL ,
	id_prospecto				integer  NOT NULL ,
	nombres              		varchar(100)  NOT NULL ,
	ape_paterno          		varchar(100)  NOT NULL ,
	ape_materno          		varchar(100)  NOT NULL ,
	fec_nacimiento       		datetime  NOT NULL ,
	genero               		integer  NOT NULL ,
	codigo_cmp           		varchar(20)  NOT NULL ,
	flag_atiende_covid   		integer  NOT NULL ,
	flag_Atiende_vih     		integer  NOT NULL ,
	flag_atiende_videollamada	integer  NOT NULL ,
	comentario_personal			varchar(500)  NOT NULL ,
	facebook             		varchar(100)  DEFAULT NULL ,
	instagram            		varchar(100)  DEFAULT NULL ,
	twitter              		varchar(100)  DEFAULT NULL ,
	linkedin             		varchar(100)  DEFAULT NULL,
	bol_activo			 		boolean NOT NULL , --- campo nuevo agregado, falta aumentar en la db y hacer un insert
	fec_creacion         		datetime  NOT NULL ,
	fec_modificacion     		datetime DEFAULT NULL
);


CREATE TABLE comentarios
( 
	id_comentarios       INTEGER PRIMARY KEY AUTO_INCREMENT ,
	id_medico            integer  NOT NULL ,
	des_comentario       varchar(500)  NOT NULL ,
	fec_creacion         datetime  NOT NULL ,
	fec_modificacion     datetime DEFAULT NULL ,
	puntaje              integer  NOT NULL 
);


CREATE TABLE consultorio
( 
	id_consultorio       integer PRIMARY KEY AUTO_INCREMENT ,
	id_medico            integer  NOT NULL ,
	cod_distrito         varchar(10) NOT NULL ,
	cod_provincia        varchar(10) NOT NULL ,
	cod_departamento     varchar(10) NOT NULL ,
	des_direccion        varchar(100)  NULL ,
	fec_creacion         datetime NOT NULL ,
	fec_modificacion     datetime DEFAULT NULL ,
	horario_atencion     varchar(30)  NULL 
);

CREATE TABLE documento_venta
( 
	id_docventa          integer PRIMARY KEY AUTO_INCREMENT ,
	id_tipodocumento     integer  NOT NULL ,
	fec_emision          datetime  not NULL ,
	des_venta            varchar(150)  not NULL ,
	precio_bruto         decimal  not NULL ,
	precio_neto          decimal not NULL ,
	precio_igv           decimal not NULL ,
	fec_creacion         datetime not NULL ,
	fec_modificacion     datetime default NULL 
);

CREATE TABLE enfermedades_tratadas
( 
	id_enf_tratadas      integer PRIMARY KEY auto_increment ,
	id_medico            integer  NOT NULL ,
	des_enfermedades     varchar(500)  NOT NULL ,
	fec_creacion         datetime  NOT NULL ,
	fec_modificacion     datetime default NULL 
);

CREATE TABLE especialidad_medico
( 
	id_especialidad_medico   integer primary KEY auto_increment ,
	id_especialidad          integer not null ,
	id_medico                integer  NOT NULL ,
	codigo_rne               varchar(10)  NULL ,
	fec_creacion             datetime  NOT NULL ,
	fec_modificacion         datetime  default NULL 
);

CREATE TABLE especialista
( 
	id_especialista      integer primary key auto_increment ,
	id_medico            integer  NOT NULL ,
	des_especialista     varchar(250)  NOT NULL ,
	fec_creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  default NULL 
);

CREATE TABLE formacion
( 
	id_formacion         integer primary key auto_increment ,
	id_medico            integer  NOT NULL ,
	desc_formacion       varchar(250)  NOT NULL ,
	fec_anio_inicio      datetime  NOT NULL ,
	fec_anio_fin         datetime  NOT NULL ,
	fec_Creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  default NULL 
);

CREATE TABLE servicio
( 
	id_servicio          integer PRIMARY KEY auto_increment ,
	id_medico            integer  NOT NULL ,
	des_servicio         varchar(200)  NOT NULL ,
	num_precio           decimal(10,2)  NOT NULL ,
	fec_creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  default NULL 
);

CREATE TABLE suscripcion
( 
	id_suscripcion       integer primary key auto_increment ,
	id_medico            integer  NOT NULL ,
	id_plan              integer  NOT NULL ,
	id_docventa          integer  NOT NULL ,
	fec_inicio           datetime  NOT NULL ,
	fec_fin              datetime  NOT NULL ,
	flag_activo          boolean  NOT NULL ,
	fec_creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  default NULL 
);

CREATE TABLE telefono
( 
	id_telefono          integer PRIMARY key auto_increment  ,
	id_consultorio       integer  NOT NULL ,
	num_telefono         varchar(20)  NOT NULL ,
	flag_activo          boolean  NOT NULL ,
	fec_creacion         datetime  NOT NULL ,
	fec_modificacion     datetime  default NULL 
);

CREATE TABLE cita
( 
	id_cita              integer PRIMARY KEY auto_increment ,
	id_consultorio       integer  NOT NULL ,
	id_paciente          integer  NOT NULL ,
	dia_cita             datetime  NULL ,
	hora_cita            varchar(18)  NULL ,
	flag_activa          boolean  not NULL ,
	fec_creacion         datetime NOT NULL ,
	fec_modificacion     datetime DEFAULT NULL 
);

CREATE TABLE medio_pago
( 
	id_mediopago         INTEGER PRIMARY KEY auto_increment ,
	id_consultorio       integer  NOT NULL,
	desc_medio_pago	     varchar(50) not NULL ,
	fec_creacion         datetime not null ,
	fec_modificacion     datetime DEFAULT NULL
);

CREATE TABLE perfil_usuario
(
	id_perfil_usuario 	INT PRIMARY KEY auto_increment,
	des_perfil_usuario	varchar(20) not null,
	num_vigente			integer NOT NULL ,
	fec_creacion        datetime not null ,
	fec_modificacion    datetime DEFAULT NULL
);

CREATE TABLE usuario
(
    id_usuarios         integer PRIMARY KEY AUTO_INCREMENT,
    id_medico           integer NOT null,
	id_perfil_usuario	integer NOT NULL ,
    des_correo          varchar(50) not null,
    des_pass            varchar(255) not null,
    fec_creacion        datetime NOT  NULL ,
	fec_modificacion    datetime  default NULL
);