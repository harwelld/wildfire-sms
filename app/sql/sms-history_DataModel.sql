-- Table: public.sms_history

-- DROP TABLE public.sms_history;

CREATE TABLE public.sms_history
(
    cust_id integer NOT NULL,
    distance numeric,
    hist_id bigint NOT NULL DEFAULT nextval('sms_history_hist_id_seq'::regclass),
    feed_id integer NOT NULL,
    msg_sid text COLLATE pg_catalog."default",
    modified timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT sms_history_pkey PRIMARY KEY (hist_id)
)

TABLESPACE pg_default;

ALTER TABLE public.sms_history
    OWNER to postgres;