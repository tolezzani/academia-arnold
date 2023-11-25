create table cadastro_aluno (
id int not null auto_increment,
nome varchar(50) not null,
datanasc  date not null,
sexo varchar(10) not null,
email varchar(40) not null unique,
primary key (id)
);

create table cadastro_prof (
id int not null auto_increment,
nome varchar(50) not null,
datanasc  date not null,
sexo varchar(10) not null,
email varchar(40) not null unique,
treino varchar(20) not null,
primary key (id)
);

create table cadastro_treino (
id int not null auto_increment,
treino varchar(50) not null,
dia_semana varchar(20) not null,
horario varchar(10) not null,
primary key (id)
);

create table marque_treino (
id int not null auto_increment,
matricula varchar (50) not null,
treino varchar (40) not null,
professor varchar (50) not null,
primary key (id)
);