### Commerce Project 2
This document provides an overview and setup instructions for the auction site application built using Django.
Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”


### Table of Contents
Introduction
Models
Features
Setup Instructions
Django Admin Interface
Running the Application

### Introduction
The auction site is a web application that allows users to create, view, and bid on auction listings. It includes features such as adding listings to a watchlist, commenting on listings, and viewing listings by categories.

Models
The application includes the following models in addition to the User model provided by Django:

Listing: Represents an auction listing.

Fields: title, description, starting bid, current price, image URL, category, created by, active status, and creation date.
Bid: Represents a bid placed on a listing.

Fields: listing, user, amount, and timestamp.
Comment: Represents a comment made on a listing.

Fields: listing, user, content, and timestamp.
Category: Represents a category for listings.

Fields: name.

### Features
Create Listing: Users can create new auction listings with a title, description, starting bid, image URL (optional), and category (optional).

Active Listings Page: Displays all currently active auction listings, showing the title, description, current price, and photo (if provided).

Listing Page: Displays details about a specific listing. Users can add the listing to their watchlist, place a bid, close the auction (if they created it), and add comments.

Watchlist: Allows users to view and manage their watchlisted items.

Categories: Users can browse listings by category.

Admin Interface: Administrators can view, add, edit, and delete listings, bids, and comments through the Django admin interface.



## Installation
To set up this project on your computer:

1. **Download this project**
   ```sh
   git clone https://github.com/suman154/Wiki.git
2. Install all necessary dependencies
   ```sh
   pip install -r requirements.txt
3. Make migrations
   ```sh
   python manage.py makemigrations
4. Migrate
   ```sh
   python manage.py migrate
5. Run the server
   ```sh
   python manage.py runserver

  ### Running Tests
  To run the tests, use Django's test framework:
  ```sh
  python manage.py test
  ```

  ### Deployment
  Configure environment variables for production:
  Set DEBUG to False.
  Update ALLOWED_HOSTS.
  Configure the database settings for production.

  ### Contributing
  Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or improvements.
