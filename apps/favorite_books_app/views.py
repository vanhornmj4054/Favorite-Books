from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
	request.session["user"] = None #<------ sets any logged in user to NONE to facilitate log out
	return render(request, "favorite_books_app/index.html")


def create(request):
	first_name = request.POST["first_name"]
	last_name = request.POST["last_name"]
	email = request.POST["email"]
	password = request.POST["password"]
	pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) #<------------- encodes and salts password

	errors = User.objects.user_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		request.session["id"] = None
		return redirect("/")
	else:
		user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
		request.session["id"] = user.id
		return redirect("/books")
	

def validate(request):
	
	if User.objects.get(email=request.POST['login_email']) != None:
		user = User.objects.get(email=request.POST['login_email'])
		password = request.POST['login_password']
		pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 
		
		if bcrypt.checkpw(password.encode(), user.password.encode()): #<------------ checks encoded entered password
			request.session["id"] = user.id #<------------------------------ if match, set user id into session
			return redirect("/books") #<------------------------------------ and send to books page
	else:
		return redirect("/") # <------------ if not a match, redirect back to login page


def books(request):
	if request.session["id"] == None: #<------------------- prevents unauthorized access
		return redirect('/')
	else:
		user = User.objects.get(id=request.session["id"])
		
		context = {
			"user" : user,
			"uploaded_books": Book.objects.all(),
		}

		return render(request, "favorite_books_app/books.html", context)


def add_book(request):
	title = request.POST["favorite_title"]
	description = request.POST["favorite_description"]
	user = User.objects.get(id=request.session["id"])

	if len(title) > 0:
		new_book = Book.objects.create(title=title, description=description, uploaded_by=user)
		new_book.users_who_like.add(user) #<------------ automatically likes a book when user uploads

	return redirect("/books")


def edit_book(request, id): #<-------------------------- displays edit book page
	user = User.objects.get(id=request.session["id"])
	book = Book.objects.get(id=id)
	
	context = {
		"user" : user,
		"book" : book,
	}
	return render(request, "favorite_books_app/edit_book.html", context)


def update_book(request):
	book_id = request.POST['book_id']
	new_title = request.POST["title_edit"]
	book = Book.objects.get(id=book_id)
	description_edit = request.POST["description_edit"] 
	
	if new_title != book.title:
		if len(new_title) > 0:    #<------------------ validations for updated title
			book.title = new_title  #<---------------- sets book title to the new title
			book.save()

	if description_edit != book.description:
		if len(description_edit) > 4:
			book.description = description_edit
			book.save()

	return redirect("/books")


def favorite(request, id):  #<------------------------- favorite from edit page
	user = User.objects.get(id=request.session["id"])
	book = Book.objects.get(id=id)
	book.users_who_like.add(user)

	return redirect(f"/edit_book/{book.id}")


def unfavorite(request, id):  #<------------------------ unfavorite from edit page
	user = User.objects.get(id=request.session["id"])
	book = Book.objects.get(id=id)
	book.users_who_like.remove(user)

	return redirect(f"/edit_book/{book.id}")


def favorite_page(request, id):  #<--------------------- favorite from books page
	user = User.objects.get(id=request.session["id"])
	book = Book.objects.get(id=id)
	book.users_who_like.add(user)

	return redirect("/books")


def unfavorite_page(request, id):  #<-------------------- unfavorite from books page
	user = User.objects.get(id=request.session["id"])
	book = Book.objects.get(id=id)
	book.users_who_like.remove(user)

	return redirect("/books")


def delete_book(request, id):
	user = User.objects.get(id=request.session["id"])
	book = Book.objects.get(id=id)
	book.delete()

	return redirect("/books")

	
	
    