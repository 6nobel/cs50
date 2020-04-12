SELECT title FROM stars
    INNER JOIN movies
    ON stars.movie_id = movies.id
    INNER JOIN people
    on stars.person_id = people.id
    WHERE name = 'Helena Bonham Carter'
INTERSECT
SELECT title FROM stars
    INNER JOIN movies
    ON stars.movie_id = movies.id
    INNER JOIN people
    on stars.person_id = people.id
    WHERE name = 'Johnny Depp'
    ;