from apps import master

@master.route('/')
def index():
	return "Feeling all setteled in"