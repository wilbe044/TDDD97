

drop table if exists users;
create table users (
  email text primary key not null,
  password text not null,
--   firstname text not null,
--   familyname text not null,
--   gender text not null,
--   city text not null,
--   country text not null
);