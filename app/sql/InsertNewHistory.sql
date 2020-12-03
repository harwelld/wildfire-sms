-- PROCEDURE: public.insertnewhistory(integer, integer, numeric, text)

-- DROP PROCEDURE public.insertnewhistory(integer, integer, numeric, text);

CREATE OR REPLACE PROCEDURE public.insertnewhistory(
	_feed_id integer,
	_cust_id integer,
	_distance numeric,
	_msg_sid text)
LANGUAGE 'sql'
AS $BODY$
INSERT INTO sms_history(feed_id, cust_id, distance, msg_sid)
    VALUES(
		CAST (_feed_id AS int),
		CAST (_cust_id AS int),
		CAST (_distance AS numeric),
		CAST (_msg_sid AS text)
	);
$BODY$;
