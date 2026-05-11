-- Useful SELECT queries

-- 1. List all tracks in a specific album (Testing 1:N relationship)
-- This query shows the relationship between ALBUM and TRACK
SELECT a.Title AS Album_Title, t.TrackNumber, t.Title AS Song_Name, t.Duration
FROM ALBUM a
JOIN TRACK t ON a.AlbumID = t.AlbumID
WHERE a.Title = 'Harry\'s House';

-- 2. Find all albums made by a specific artist (Testing M:N relationship)
-- This query uses the ARTIST_ALBUM junction table
SELECT ar.Name AS Artist_Name, al.Title AS Album_Title, al.Genre
FROM ARTIST ar
JOIN ARTIST_ALBUM aa ON ar.ArtistID = aa.ArtistID
JOIN ALBUM al ON aa.AlbumID = al.AlbumID
WHERE ar.Name = 'Billie Eilish';

-- 3. Show stock levels and prices for each album (Testing 1:N relationship)
-- This helps us see the physical items in our inventory
SELECT a.Title, v.Format, v.Price, v.StockQuantity
FROM ALBUM a
JOIN ALBUM_VARIANT v ON a.AlbumID = v.AlbumID
ORDER BY v.StockQuantity ASC;

-- 4. Calculate total amount spent by each customer
-- This joins CUSTOMER, CUSTOMER_ORDER and shows aggregation
SELECT c.FirstName, c.LastName, SUM(co.TotalAmount) AS Total_Spent
FROM CUSTOMER c
JOIN CUSTOMER_ORDER co ON c.CustomerID = co.CustomerID
GROUP BY c.CustomerID;

-- 5. Comprehensive Order History (Implementation of M:N Relationships)
-- This query demonstrates the many-to-many relationship by joining CUSTOMER, CUSTOMER_ORDER, ORDER_ITEM, ALBUM_VARIANT, and ALBUM to show detailed order information
SELECT co.OrderID, c.FirstName, c.LastName AS Customer_Name, a.Title AS Album_Title, v.Format, oi.Quantity, oi.UnitPrice
FROM CUSTOMER_ORDER co
JOIN CUSTOMER c ON co.CustomerID = c.CustomerID
JOIN ORDER_ITEM oi ON co.OrderID = oi.OrderID
JOIN ALBUM_VARIANT v ON oi.VariantID = v.VariantID
JOIN ALBUM a on a.AlbumID = v.AlbumID
ORDER BY co.OrderDate;