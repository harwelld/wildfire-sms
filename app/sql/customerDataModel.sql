-- Table: public.customer

-- DROP TABLE public.customer;

CREATE TABLE public.customer
(
    user_id integer NOT NULL DEFAULT nextval('customer_user_id_seq'::regclass),
    user_name text COLLATE pg_catalog."default" NOT NULL,
    user_phone text COLLATE pg_catalog."default" NOT NULL,
    user_distance integer,
    geom geometry(Point,4326),
    modified timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT customer_pkey PRIMARY KEY (user_id),
    CONSTRAINT customer_user_name_key UNIQUE (user_name),
    CONSTRAINT customer_user_phone_key UNIQUE (user_phone)
)

TABLESPACE pg_default;

ALTER TABLE public.customer
    OWNER to postgres;