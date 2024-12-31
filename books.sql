SELECT * FROM books_db.books;
use books_db
-- 1. Check Availability of eBooks vs Physical Books
SELECT 
    SUM(CASE WHEN isEbook = 1 THEN 1 ELSE 0 END) AS ebook_count,
    SUM(CASE WHEN isEbook = 0 THEN 1 ELSE 0 END) AS physical_book_count
FROM books;

-- 2. Find the Publisher with the Most Books Published
SELECT publisher, COUNT(*) AS books_published
FROM books
GROUP BY publisher
ORDER BY books_published DESC
LIMIT 1;

-- 3. Identify the Publisher with the Highest Average Rating
SELECT publisher, AVG(averageRating) AS avg_rating
FROM books
GROUP BY publisher
ORDER BY avg_rating DESC
LIMIT 1;

-- 4. Get the Top 5 Most Expensive Books by Retail Price
SELECT book_title, amount_retailPrice
FROM books
ORDER BY amount_retailPrice DESC
LIMIT 5;

-- 5. Find Books Published After 2010 with at Least 500 Pages
SELECT book_title, year, pageCount
FROM books
WHERE year > 2010 AND pageCount >= 500;

-- 6. List Books with Discounts Greater than 20%
SELECT book_title, amount_listPrice, amount_retailPrice,
       ((amount_listPrice - amount_retailPrice) / amount_listPrice) * 100 AS discount_percentage
FROM books
WHERE amount_listPrice > amount_retailPrice
HAVING discount_percentage > 20;

-- 7. Find the Average Page Count for eBooks vs Physical Books
SELECT 
    isEbook,
    AVG(pageCount) AS avg_page_count
FROM books
GROUP BY isEbook;

-- 8. Find the Top 3 Authors with the Most Books
SELECT book_authors, COUNT(*) AS books_count
FROM books
GROUP BY book_authors
ORDER BY books_count DESC
LIMIT 3;

-- 9. List Publishers with More than 10 Books
SELECT publisher, COUNT(*) AS books_count
FROM books
GROUP BY publisher
HAVING books_count > 10;

-- 10. Find the Average Page Count for Each Category
SELECT categories, AVG(pageCount) AS avg_page_count
FROM books
GROUP BY categories;

-- 11. Retrieve Books with More than 3 Authors
SELECT book_title, book_authors
FROM books
WHERE LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) > 2;

-- 12. Books with Ratings Count Greater Than the Average
SELECT book_title, ratingsCount
FROM books
WHERE ratingsCount > (SELECT AVG(ratingsCount) FROM books);

-- 13. Books with the Same Author Published in the Same Year
SELECT book_authors, year, COUNT(*) AS books_count
FROM books
GROUP BY book_authors, year
HAVING books_count > 1;

-- 14. Books with a Specific Keyword in the Title
SELECT book_title
FROM books
WHERE book_title LIKE '%Keyword%';  -- Replace 'Keyword' with the desired search term

-- 15. Year with the Highest Average Book Price
SELECT year, AVG(amount_retailPrice) AS avg_price
FROM books
GROUP BY year
ORDER BY avg_price DESC
LIMIT 1;

-- 16. Count Authors Who Published 3 Consecutive Years
SELECT book_authors, COUNT(DISTINCT year) AS unique_years
FROM books
GROUP BY book_authors
HAVING unique_years >= 3;

-- 17. Authors Who Published Books in the Same Year but Under Different Publishers
SELECT book_authors, year, COUNT(DISTINCT publisher) AS publisher_count
FROM books
GROUP BY book_authors, year
HAVING publisher_count > 1;

-- 18. Average Retail Price of eBooks vs Physical Books
SELECT 
    AVG(CASE WHEN isEbook = 1 THEN amount_retailPrice ELSE NULL END) AS avg_ebook_price,
    AVG(CASE WHEN isEbook = 0 THEN amount_retailPrice ELSE NULL END) AS avg_physical_price
FROM books;

-- 19. Books with an Average Rating More Than Two Standard Deviations Away from the Overall Average Rating
WITH rating_stats AS (
    SELECT AVG(averageRating) AS avg_rating, STDDEV(averageRating) AS stddev_rating
    FROM books
)
SELECT book_title, averageRating, ratingsCount
FROM books, rating_stats
WHERE ABS(averageRating - avg_rating) > 2 * stddev_rating;

-- 20. Publisher with the Highest Average Rating (More Than 10 Books)
SELECT publisher, AVG(averageRating) AS avg_rating, COUNT(*) AS books_count
FROM books
GROUP BY publisher
HAVING books_count > 10
ORDER BY avg_rating DESC
LIMIT 1;








