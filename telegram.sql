create table tg_user (
       peer_id INTEGER primary key,
       print_name text,
       first_name text,
       last_name text,
       username text
);

create table tg_chat (
       peer_id INTEGER primary key,
       print_name text,
       title text
);

create table tg_user_tg_chat (
       id INTEGER primary key,
       tg_user_peer_id	 INTEGER,
       tg_chat_peer_id	 INTEGER,
       foreign key (tg_user_peer_id) REFERENCES tg_user(peer_id),
       foreign key (tg_chat_peer_id) REFERENCES tg_chat(peer_id)
);
