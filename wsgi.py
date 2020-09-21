from flask import Flask, request, render_template
from repository.memory_repo import MemoryRepo
from domainmodel.user import User

app = Flask(__name__)
repo = MemoryRepo('datafiles/Data1000Movies.csv')
titleChars = ["0-9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
servData = {
	"allMovies": repo.movies,
	"allDirectors": repo.directors,
	"allActors": repo.actors,
	"allGenres": repo.genres,
	"allUsers": repo.users,
	"currentUser": None,
	"currentWatchlist": None,
	"authMessage": "",
	"filteredMovies": repo.movies,
	"charLinks": [f'<a class="browse-link" href="/browse?BrowseCategory=TitleChar&BrowseQuery={char}">{char}</a>' for char in titleChars],
	"genreLinks": [f'<a class="browse-link" href="/browse?BrowseCategory=Genre&BrowseQuery={genre.name}">{genre.name}</a>' for genre in repo.genres],
	"directorLinks": [f'<a class="browse-link" href="/browse?BrowseCategory=Director&BrowseQuery={director.director_full_name}">{director.director_full_name}</a>' for director in repo.directors],
	"actorLinks": [f'<a class="browse-link" href="/browse?BrowseCategory=Actor&BrowseQuery={actor.actor_full_name}">{actor.actor_full_name}</a>' for actor in repo.actors]
}


@app.route('/')
def index():
	servData["filteredMovies"] = repo.movies
	return render_template('index.html', **servData)

@app.route('/login')
def login():
	servData["filteredMovies"] = repo.movies
	username = request.args.get('LoginUsername')
	password = request.args.get('LoginPassword')
	user = repo.get_user(username)
	if user is None:
		servData["authMessage"] = "Invalid username - please try again"
		return render_template('logging_in.html', **servData)  # COMPLETE THIS HTML FILE
	elif user.password != password:
		servData["authMessage"] = "Invalid password - please try again"
		return render_template('logging_in.html', **servData)  # COMPLETE THIS HTML FILE
	else:
		servData["authMessage"] = ""
		servData["currentUser"] = user
		servData["currentWatchlist"] = servData["currentUser"].watchlist
		return render_template('logged_in.html', **servData)  # COMPLETE THIS HTML FILE

@app.route('/register')
def register():
	servData["filteredMovies"] = repo.movies
	username = request.args.get('RegUsername').strip().lower()
	password1 = request.args.get('RegPassword1')
	password2 = request.args.get('RegPassword2')
	if password1 != password2:
		servData["authMessage"] = "Passwords don't match - please try again"
		return render_template('registering.html', **servData)  # COMPLETE THIS HTML FILE
	elif repo.get_user(username) is not None:
		servData["authMessage"] = "Username already taken - please try again"
		return render_template('registering.html', **servData)  # COMPLETE THIS HTML FILE
	else:
		servData["authMessage"] = ""
		servData["currentUser"] = User(username, password1)
		servData["currentWatchlist"] = servData["currentUser"].watchlist
		repo.add_user(servData["currentUser"])
		return render_template('logged_in.html', **servData) # COMPLETE THIS HTML FILE

@app.route('/logout')
def logout():
	servData["filteredMovies"] = repo.movies
	servData["currentUser"] = None
	servData["currentWatchlist"] = None
	return render_template('index.html', **servData)

@app.route('/browse')
def browse():
	category = request.args.get("BrowseCategory")  # i.e. TitleChar, Genre, Director, or Actor
	query = request.args.get("BrowseQuery").strip().lower()  # "0-9" if category == TitleChar
	if query == "":  # There are no known circumstances that can trigger this
		servData["filteredMovies"] = servData["allMovies"]
	else:
		servData["filteredMovies"] = list()
		for movie in servData["allMovies"]:
			if category == "TitleChar":
				first = movie.title.strip().lower()[0]
				if first.isalpha() and first == query or first.isdigit() and query == "0-9":
					servData["filteredMovies"].append(movie)
			elif category == "Genre":
				for genre in movie.genres:
					if genre.name.strip().lower() == query:
						servData["filteredMovies"].append(movie)
						break
			elif category == "Director":
				if movie.director.director_full_name.strip().lower() == query:
					servData["filteredMovies"].append(movie)
			elif category == "Actor":
				for actor in movie.actors:
					if query in actor.actor_full_name.strip().lower().split():
						servData["filteredMovies"].append(movie)
						break
			else:
				print("ERROR: Invalid browsing category passed from HTML")
	return render_template('index.html', **servData)

@app.route('/search')
def search():
	category = request.args.get("SearchCategory").strip().lower()  # i.e. title, genre, director, or actor
	query = request.args.get("SearchQuery").strip().lower()
	if query == "":
		servData["filteredMovies"] = servData["allMovies"]
	else:
		servData["filteredMovies"] = list()
		for movie in servData["allMovies"]:
			if category == "title":
				if movie.title.strip().lower() == query:
					servData["filteredMovies"].append(movie)
			elif category == "genre":
				for genre in movie.genres:
					if genre.name.strip().lower() == query:
						servData["filteredMovies"].append(movie)
						break
			elif category == "director":
				if movie.director.director_full_name.strip().lower() == query:
					servData["filteredMovies"].append(movie)
			elif category == "actor":
				for actor in movie.actors:
					if query in actor.actor_full_name.strip().lower().split():
						servData["filteredMovies"].append(movie)
						break
			else:
				print("ERROR: Invalid search category passed from HTML")
	return render_template('index.html', **servData)


if __name__ == "__main__":
	app.run(host='localhost', port=5000, debug=True)