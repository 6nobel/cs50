SELECT DISTINCT name FROM directors
    INNER JOIN movies
    ON directors.movie_id = movies.id
    INNER JOIN people
    on directors.person_id = people.id
    INNER JOIN ratings
    on directors.movie_id = ratings.movie_id
    WHERE rating >= 9.0;