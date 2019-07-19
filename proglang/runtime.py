from proglang import *
import sys, timeit

#interpreter for programming language
#can interpret and run a file or open a repl

def repl():
	stmt = ''
	while stmt != 'q':
		stmt = input('λ ')
		if stmt != 'q':
			parse_stmt(tokenise(stmt))

if __name__ == '__main__':
	try:
		filename = sys.argv[1]
	except IndexError:
		print('entering repl (q to quit)')
		repl()
		sys.exit()

	try:
		handle = open(filename, 'r')
	except FileNotFoundError:
		print('no such file or directory')
		sys.exit()

	prog = ''
	for line in handle.readlines():
		#ignore comments
		if line[:2] != '//':
			line = line.replace('\n', '')
			line = line.replace('\t', '')
			prog += line
			
	handle.close()

	start = timeit.default_timer()

	for stmt in prog.split(';')[:-1]:

		parse_stmt(tokenise(stmt))

	end = timeit.default_timer()

	print(f'finished in {end - start :0.4f}s')
