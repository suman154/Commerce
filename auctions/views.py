from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import User, Category, Listing, Comment, Bid



def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner
    })


def listings_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    listings = category.listings.filter(is_active=True)
    return render(request, 'auctions/categories.html', {'category': category, 'listings': listings})


def category_list(request):
    categories = Category.objects.all()
    print(categories)  # Debugging line
    return render(request, "auctions/categories.html", {'categories': categories})


def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isOwner = request.user.username == listingData.owner.username
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "update": True,
        "message": "Conguralation! your auction is closed."
    })




def addComment(request, id):
    if request.method == 'POST':
        currentUser = request.user
        listingData = Listing.objects.get(pk=id)
        message = request.POST.get('newComment', '')

        newComment = Comment(
            author=currentUser,
            listing=listingData,
            message=message
        )
        newComment.save()
        messages.success(request, 'Comment added successfully!')
        return HttpResponseRedirect(reverse('listing', args=(id, )))


def addBid(request, id):
    listingData = get_object_or_404(Listing, pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user == listingData.owner

    if request.method == "POST":
        newBid = request.POST.get('newBid')
        if newBid:
            newBid = int(newBid)
            if newBid > listingData.price:
                listingData.price = newBid
                listingData.save()
                return render(request, "auctions/listing.html", {
                    "listing": listingData,
                    "message": "Bid was updated successfully",
                    "isListingInWatchlist": isListingInWatchlist,
                    "allComments": allComments,
                    "update": True,
                    "isOwner": isOwner
                })
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listingData,
                    "message": "Bid must be higher than the current price.",
                    "isListingInWatchlist": isListingInWatchlist,
                    "allComments": allComments,
                    "update": False,
                    "isOwner": isOwner
                })

    
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner
    })



def removeWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, ))) 



def addWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def displayWatchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })





def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "Listings": activeListings,
        "categories": allCategories
    })


def displayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListings = Listing.objects.filter(isActive=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "Listings": activeListings,
            "categories": allCategories
        })



def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else: 
        # Get the data from form 
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        # User
        currentUser = request.user
        # All content from the particular category
        categoryData = Category.objects.get(categoryName=category)
        # Create a new bid
        bid = Bid(bid=int(price), user=currentUser)
        bid.save()

        # Create new listing
        newListing = Listing(
            title=title,
            description=description,
            imageUrl=imageurl,
            price=float(price),
            category=categoryData,
            owner=currentUser
        )
       
        # Insert the object in database
        newListing.save()
        # Redirect to index page
        return HttpResponseRedirect(reverse(index))
 



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


