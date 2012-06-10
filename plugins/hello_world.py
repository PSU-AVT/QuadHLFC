import llfc

def say_hello():
	print 'Hello, world!'
	evloop.add_timer(1, say_hello)

def on_load():
	say_hello()

print 'hello'
