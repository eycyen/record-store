USE RECORD_STORE;

-- Insert sample artists
INSERT INTO ARTIST (Name, FormationYear, Bio) VALUES
('Harry Styles', 2010, 'English singer, songwriter, and actor.'),
('Billie Eilish', 2015, 'American singer and songwriter.'),
('Olivia Rodrigo', 2020, 'American singer-songwriter and actress.');

-- Insert sample albums
INSERT INTO ALBUM (Title, ReleaseDate, Genre) VALUES
('Harry''s House', '2022-05-20', 'Pop'),
('HIT ME HARD AND SOFT', '2024-05-17', 'Alternative Pop'),
('SOUR', '2021-05-21', 'Pop Punk');

-- Link artists and albums in the junction table
INSERT INTO ARTIST_ALBUM (ArtistID, AlbumID) VALUES
(1, 1),
(2, 2),
(3, 3);

-- Insert a few sample tracks
INSERT INTO TRACK (Title, Duration, TrackNumber, AlbumID) VALUES
('As It Was', '00:02:47', 4, 1),
('LUNCH', '00:02:59', 2, 2),
('good 4 u', '00:02:58', 3, 3);

-- Insert physical inventory items (Album Variants)
INSERT INTO ALBUM_VARIANT (Format, Price, StockQuantity, AlbumID) VALUES
('Vinyl', 35.99, 15, 1),
('CD', 14.99, 30, 1),
('Vinyl', 39.99, 10, 2),
('Vinyl', 32.99, 20, 3);

-- Insert a sample customer
INSERT INTO CUSTOMER (FirstName, LastName, Email, Address) VALUES
('Deniz', 'Kaya', 'deniz.kaya@email.com', 'Cankaya, Ankara');

-- Insert a sample customer order
INSERT INTO CUSTOMER_ORDER (OrderDate, TotalAmount, Status, CustomerID) VALUES
('2026-05-10 14:30:00', 75.98, 'Completed', 1);

-- Insert the items included in the order
INSERT INTO ORDER_ITEM (OrderID, VariantID, Quantity, UnitPrice) VALUES
(1, 1, 1, 35.99), -- Harry Styles Vinyl
(1, 3, 1, 39.99); -- Billie Eilish Vinyl