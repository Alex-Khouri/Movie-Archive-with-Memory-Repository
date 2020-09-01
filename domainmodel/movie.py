from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director

class Movie:
	def __init__(self, titleArg=None, yearArg=None):
		self.movie_title = None
		if (isinstance(titleArg, str) and len(titleArg) > 0):
			self.movie_title = titleArg.strip()
		self.movie_year = None
		if (isinstance(yearArg, int) and yearArg >= 1900):
			self.movie_year = yearArg
		self.movie_description = None
		self.movie_director = None
		self.movie_actors = []
		self.movie_genres = []
		self.movie_runtime_minutes = None
	
	def __repr__(self):
		return f"<Movie {self.movie_title}, {self.movie_year}>"
	
	def __eq__(self, other):
		return (self.__class__ == other.__class__ and self.movie_title == other.movie_title and self.movie_year == other.movie_year)
	
	def __lt__(self, other):
		if self.movie_title == other.movie_title:
			return (self.movie_year < other.movie_year)
		else:
			return (self.movie_title < other.movie_title)
	
	def __hash__(self):
		return hash(self.movie_title + str(self.movie_year))
		
	@property
	def title(self):
		return self.movie_title
	
	@property
	def description(self):
		return self.movie_description
		
	@property
	def director(self):
		return self.movie_director
		
	@property
	def actors(self):
		return self.movie_actors
		
	@property
	def genres(self):
		return self.movie_genres
		
	@property
	def runtime_minutes(self):
		return self.movie_runtime_minutes
		
	@title.setter
	def title(self, newTitle):
		if (isinstance(newTitle, str) and len(newTitle) > 0):
			self.movie_title = newTitle.strip()
	
	@description.setter
	def description(self, newDescrip):
		if (isinstance(newDescrip, str) and len(newDescrip) > 0):
			self.movie_description = newDescrip.strip()
	
	@director.setter
	def director(self, newDirector):
		if (isinstance(newDirector, Director)):
			self.movie_director = newDirector
			
	@actors.setter
	def actors(self, newActors):
		if (isinstance(newActors, list)):
			self.movie_actors = newActors
			
	@genres.setter
	def genres(self, newGenres):
		if (isinstance(newGenres, list)):
			self.movie_genres = newGenres
			
	@runtime_minutes.setter
	def runtime_minutes(self, newRuntime):
		if (isinstance(newRuntime, int)):
			if (newRuntime >= 0):
				self.movie_runtime_minutes = newRuntime
			else:
				raise ValueError('ValueError: Negative runtime value!')
			
	def add_actor(self, newActor):
		if (isinstance(newActor, Actor) and not newActor in self.movie_actors):
			self.movie_actors.append(newActor)
			
	def add_genre(self, newGenre):
		if (isinstance(newGenre, Genre) and not newGenre in self.movie_genres):
			self.movie_genres.append(newGenre)
			
	def remove_actor(self, remActor):
		if (isinstance(remActor, Actor) and remActor in self.movie_actors):
			self.movie_actors.remove(remActor)
		elif (isinstance(remActor, str)):
			for actor in self.movie_actors:
				if actor.actor_full_name == remActor:
					self.movie_actors.remove(actor)
					break
			
	def remove_genre(self, remGenre):
		if (isinstance(remGenre, Genre) and remGenre in self.movie_genres):
			self.movie_genres.remove(remGenre)
		elif (isinstance(remGenre, str)):
			for genre in self.movie_genres:
				if genre.genre_name == remGenre:
					self.movie_genres.remove(genre)
					break