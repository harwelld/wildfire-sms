-- PROCEDURE: public.registernewcustomer(text, text, integer, numeric, numeric)

-- DROP PROCEDURE public.registernewcustomer(text, text, integer, numeric, numeric);

CREATE OR REPLACE PROCEDURE public.registernewcustomer(
	_username text,
	_phone text,
	_distance integer,
	_lat numeric,
	_lon numeric)
LANGUAGE 'sql'
AS $BODY$
INSERT INTO customer(user_name, user_phone, user_distance, geom)
    VALUES(
		CAST (_username AS text),
		CAST (_phone AS text),
		CAST (_distance AS integer),
		ST_SetSRID(ST_MakePoint(_lon, _lat), 4326)
	);
$BODY$;
