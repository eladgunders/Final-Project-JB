CREATE or replace function sp_get_airline_by_username
(_username text)
returns TABLE(id bigint, name text, country_id bigint, 
			 user_id bigint)
language plpgsql AS
	$$
		BEGIN
			return QUERY
			select a.id, a.name, a.country_id, 
			a.user_id from airline_companies a
			join users u on a.user_id = u.id
			where u.username = _username;
		end;
	$$;
