-- Table: public.inciweb

-- DROP TABLE public.inciweb;

CREATE TABLE public.inciweb
(
    inc_id integer NOT NULL DEFAULT nextval('inciweb_inc_id_seq'::regclass),
    inc_name text COLLATE pg_catalog."default",
    inc_type text COLLATE pg_catalog."default",
    inc_summary text COLLATE pg_catalog."default",
    inc_state text COLLATE pg_catalog."default",
    inc_updated text COLLATE pg_catalog."default",
    geom geometry(Point,4326),
    inc_size text COLLATE pg_catalog."default",
    inc_url text COLLATE pg_catalog."default",
    inc_contained text COLLATE pg_catalog."default",
    feed_id text COLLATE pg_catalog."default",
    CONSTRAINT wildfire_pkey PRIMARY KEY (inc_id)
)

TABLESPACE pg_default;

ALTER TABLE public.inciweb
    OWNER to postgres;