-- FUNCTION: public.getdistancebetweenpoints(character varying, character varying, character varying, character varying)

-- DROP FUNCTION public.getdistancebetweenpoints(character varying, character varying, character varying, character varying);

CREATE OR REPLACE FUNCTION public.getdistancebetweenpoints(
	_lng1 character varying,
	_lat1 character varying,
	_lng2 character varying,
	_lat2 character varying)
    RETURNS numeric
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    
AS $BODY$
BEGIN
   RETURN (SELECT ST_Distance(gg1, gg2) As spheroid_dist
			FROM (SELECT CONCAT('SRID=4326;POINT(',_lng1,' ',_lat1,')')::geography as gg1,
				         CONCAT('SRID=4326;POINT(',_lng2,' ',_lat2,')')::geography as gg2) as foo
					);
END
$BODY$;

ALTER FUNCTION public.getdistancebetweenpoints(character varying, character varying, character varying, character varying)
    OWNER TO postgres;
