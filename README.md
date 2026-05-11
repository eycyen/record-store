# Record Store Database System

This project involves the design and implementation of a relational database for a Record Store to manage its daily operations. It was developed for the COM2058 project at Ankara University, Computer Engineering Department.

## System Description

The system is designed to record and manage information regarding albums, artists, physical store items (such as vinyl records, CDs, and cassettes), customers, and customer orders. By using a relational database design, the system ensures data integrity and prevents the repetition of information.

## Database Entities

The database consists of the following main entities:

* ARTIST: Represents the singer or the music band.
* ALBUM: Represents the music release itself, independent of its physical format.
* TRACK: Represents the individual songs contained within an album.
* ALBUM_VARIANT (Physical Inventory): Represents the actual physical items available in the store (e.g., a specific vinyl or CD).
* CUSTOMER: Represents the individuals who purchase music from the store.
* CUSTOMER_ORDER: Represents the shopping receipt or the transaction record.

## Relationship Requirements

The entities are connected through the following relationships:

* Artist and Album (M:N): One artist can create many albums, and one album can feature multiple artists (e.g., a duet).
* Album and Track (1:N): One album contains many tracks, but a specific track belongs to only one album.
* Album and Physical Inventory (1:N): One album can be released in many formats, but a specific physical item is linked to only one album.
* Customer and Order (1:N): A customer can place many orders, but a single order is linked to exactly one customer.
* Order and Physical Product (M:N): An order can contain many physical items, and a physical item can be included in many different orders. This relationship also records the specific sale details, such as quantity and unit price.

## Business Rules and Constraints

The system enforces the following business rules to maintain data accuracy:

* Stock Validation: The stock quantity of any physical item in the store cannot be less than zero.
* Unique Customers: Customer email addresses must be unique. Two customers cannot register with the same email address.
* Price History Integrity: The system must save the specific unit price in the order details at the time of the sale. This ensures that past order totals do not change if the store updates the current price of an item later.