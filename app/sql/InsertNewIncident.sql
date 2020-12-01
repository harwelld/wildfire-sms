-- PROCEDURE: public.insertnewincident(text, text, text, text, text, numeric, numeric, text, text, text, text)

-- DROP PROCEDURE public.insertnewincident(text, text, text, text, text, numeric, numeric, text, text, text, text);

CREATE OR REPLACE PROCEDURE public.insertnewincident(
	_name text,
	_type text,
	_summary text,
	_state text,
	_updated text,
	_lat numeric,
	_lon numeric,
	_size text,
	_url text,
	_feed_id text,
	_contained text)
LANGUAGE 'sql'
AS $BODY$
INSERT INTO inciweb(inc_name, inc_type, inc_summary, inc_state, inc_updated, inc_size, inc_url, inc_contained, feed_id, geom)
    VALUES(
		CAST (_name AS text),
		CAST (_type AS text),
		CAST (_summary AS text),
		CAST (_state AS text),
		CAST (_updated AS text),
		CAST (_size AS text),
		CAST (_url AS text),
		CAST (_contained AS text),
		CAST (_feed_id AS text),
		ST_SetSRID(ST_MakePoint(_lon, _lat), 4326)
	);
$BODY$;
