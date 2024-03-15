create table if not exists students(
	id serial primary key,
	name varchar(50) not null,
	surname varchar(50) not null,
	group_name varchar(50) not null,
	ticket varchar(50) unique not null
);

insert into students (name, surname, group_name, ticket)
values ('Tania', 'Ruzhman', 'KT-31', 356845);

select * from students;

delete from students where id = 1;