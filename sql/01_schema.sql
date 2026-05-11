-- ARTIST Table
CREATE TABLE ARTIST (
    ArtistID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    FormationYear YEAR,
    Bio TEXT
);

-- ALBUM Table
CREATE TABLE ALBUM (
    AlbumID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(150) NOT NULL,
    ReleaseDate DATE,
    Genre VARCHAR(50)
);

-- TRACK Table
CREATE TABLE TRACK (
    TrackID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(150) NOT NULL,
    Duration TIME, -- to keep time like '03:45:00'
    TrackNumber INT NOT NULL
);

-- ALBUM_VARIANT Table (physical items)
CREATE TABLE ALBUM_VARIANT (
    VariantID INT AUTO_INCREMENT PRIMARY KEY,
    Format VARCHAR(50) NOT NULL, -- like 'Vinyl', 'CD', 'Cassette'
    Price DECIMAL(10,2) NOT NULL,
    StockQuantity INT DEFAULT 0,
    CHECK (StockQuantity >= 0) -- business rule: stock cannot be less than zero
);

-- CUSTOMER Table
CREATE TABLE CUSTOMER (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE, -- business rule: emails must be unique
    Address TEXT
);

-- CUSTOMER_ORDER Table
CREATE TABLE CUSTOMER_ORDER (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10,2) DEFAULT 0.00,
    Status VARCHAR(20) DEFAULT 'Pending'
);
-- STEP 4: Mapping 1:N Relationships

-- One Album has many Tracks 
-- We add AlbumID to TRACK table
ALTER TABLE TRACK 
ADD COLUMN AlbumID INT,
ADD CONSTRAINT fk_album_track 
FOREIGN KEY (AlbumID) REFERENCES ALBUM(AlbumID);

-- One Album can have many Formats like Vinyl or CD 
-- We add AlbumID to ALBUM_VARIANT table
ALTER TABLE ALBUM_VARIANT 
ADD COLUMN AlbumID INT,
ADD CONSTRAINT fk_album_variant 
FOREIGN KEY (AlbumID) REFERENCES ALBUM(AlbumID);

-- One Customer can make many Orders 
-- We add CustomerID to CUSTOMER_ORDER table
ALTER TABLE CUSTOMER_ORDER 
ADD COLUMN CustomerID INT,
ADD CONSTRAINT fk_customer_order 
FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID);

-- STEP 5: Mapping M:N Relationships

-- Table for ARTIST and ALBUM relationship (M:N)
-- Many Artists can create Many Albums
CREATE TABLE ARTIST_ALBUM (
    ArtistID INT,
    AlbumID INT,
    PRIMARY KEY (ArtistID, AlbumID),
    FOREIGN KEY (ArtistID) REFERENCES ARTIST(ArtistID),
    FOREIGN KEY (AlbumID) REFERENCES ALBUM(AlbumID)
);

-- Table for ORDER and ALBUM_VARIANT relationship (M:N)
-- An Order includes many items, and an item can be in many orders
CREATE TABLE ORDER_ITEM (
    OrderID INT,
    VariantID INT,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL, -- business rule: save price during the sale
    PRIMARY KEY (OrderID, VariantID),
    FOREIGN KEY (OrderID) REFERENCES CUSTOMER_ORDER(OrderID),
    FOREIGN KEY (VariantID) REFERENCES ALBUM_VARIANT(VariantID),
    CHECK (Quantity > 0)
);