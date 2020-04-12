SELECT DISTINCT name FROM stars
    INNER JOIN movies
    ON stars.movie_id = movies.id
    INNER JOIN people
    on stars.person_id = people.id
    where year = 2004
    ORDER BY birth;