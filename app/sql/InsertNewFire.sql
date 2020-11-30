-- PROCEDURE: public.insertnewfire(text, text, text, text, text, text, text, text, text, numeric, numeric)

-- DROP PROCEDURE public.insertnewfire(text, text, text, text, text, text, text, text, text, numeric, numeric);

CREATE OR REPLACE PROCEDURE public.insertnewfire(
	_inc_name text,
	_inc_type text,
	_inc_summary text,
	_inc_state text,
	_inc_updated text,
	_inc_size text,
	_inc_url text,
	_inc_contained text,
	_feed_id text,
	_lat numeric,
	_lon numeric)
LANGUAGE 'sql'
AS $BODY$
INSERT INTO inciweb(inc_name, inc_type, inc_summary, inc_state, inc_updated, geom, inc_size, inc_url, inc_contained, feed_id)
    VALUES(
		CAST (_inc_name AS text),
		CAST (_inc_type AS text),
		CAST (_inc_summary AS text),
		CAST (_inc_state AS text),
		CAST (_inc_updated AS text),
		ST_SetSRID(ST_MakePoint(_lon, _lat), 4326),
		CAST (_inc_size AS text),
		CAST (_inc_url AS text),
		CAST (_inc_contained AS text),
		CAST (_feed_id AS text)
	);
$BODY$;
