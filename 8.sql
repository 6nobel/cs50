SELECT name FROM stars
    INNER JOIN movies
    ON stars.movie_id = movies.id
    INNER JOIN people
    on stars.person_id = people.id
    WHERE title = 'Toy Story';