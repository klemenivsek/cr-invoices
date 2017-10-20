drop table if exists invoices;
create table invoices (
  id integer primary key autoincrement,
  customer text not null,
  total integer not null
);