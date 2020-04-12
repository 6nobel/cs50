SELECT title FROM stars
    INNER JOIN movies
    ON stars.movie_id = movies.id
    INNER JOIN people
    on stars.person_id = people.id
    INNER JOIN ratings
    on stars.movie_id = ratings.movie_id
    WHERE name = 'Chadwick Boseman'
    ORDER BY rating DESC
    LIMIT 5;