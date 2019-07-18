#Joseph Harrison 2019
import sys, timeit

#programming language that consists of variables,
#atoms (basic functions) and lambda abstractions

#currently only supports single character identifiers
#doesn't support anonymous lambda exprs

#stores the bound variables and
#expr associated with a lambda abstraction
class LambdaAbstraction:

	def __init__(self, expr):
		#get bound variables
		self.bound = []
		p, q = 0, 0
		while q < len(expr):
			if expr[q] == '.':
				var = expr[p + 1:q]
				var = var.replace(' ', '')
				var = var.replace('λ', '')
				self.bound.append(var)
				p = q
				q += 1
			q += 1
		#get expr
		self.expr = expr[p + 1:]

	@property
	def arity(self):
		return len(self.bound)

	def __repr__(self):
		return 'λ ... ' + self.expr

	#substitute args into the lambda expr
	#so that it may be evaluated
	def substitute(self, *args):
		expr = self.expr
		for i in range(len(args)):
			expr = expr.replace(self.bound[i], args[i])
		return expr

#stores values associated with variables
#to define constants place them here
var_dict = {}

#links identifiers to relevant lambda abstractions
lambda_abs_dict = {}

#all of our abstractions can be reduced to these atoms
#atoms can then act as terminals of substitutions
#to define new atoms place them here
atom_dict = {'+' : (lambda x, y: x + y, 2),
			 '-' : (lambda x, y: y - x, 2),
			 '*' : (lambda x, y: x * y, 2),
			 '/' : (lambda x, y: x // y, 2),
			 '%' : (lambda x, y: x % y, 2)}

DIGITS = '0123456789.'

def is_number(token):
	for char in token:
		if char not in DIGITS:
			return False
	return True

def tokenise_expr(expr):
	tokens = []
	flag = False
	for char in expr:
		if char == ' ':
			flag = False
		elif char in DIGITS:
			if flag:
				tokens[-1] += char
			else:
				tokens.append(char)
				flag = True
		else:
			tokens.append(char)
	return tokens

def eval_expr(tokens):
	stack = []
	for token in tokens:
		#for atoms
		if token in atom_dict:
			atom, arity = atom_dict[token]
			#collect args for atom
			args = []
			for i in range(arity):
				args.append(stack.pop())
			#append result of calling atom on args
			stack.append(atom(*args))
		#for lambda abstractions
		elif token in lambda_abs_dict:
			lambda_abs = lambda_abs_dict[token]
			#collect args for lambda abstraction
			args = []
			for i in range(lambda_abs.arity):
				args.append(str(stack.pop()))
			#reverse args for abstractions
			args = list(reversed(args))
			#substitute values into lambda abstraction
			expr = lambda_abs.substitute(*args)
			#evaluate this expression and append to stack
			stack.append(eval_expr(tokenise_expr(expr)))
		#for variables
		elif token in var_dict:
			stack.append(var_dict[token])
		else:
			stack.append(int(token))
	return stack[-1]

def anon_lambdas_non_nested(tokens):
	q, r = 0, 0
	parens = 0
	found = False
	stack = []
	for token in tokens:
		print(stack, tokens)
		#is this token the start of a lambda
		if token == '(' and found == False:
			q = r + 1
			found = True
			parens = 0
		elif token == '(' and found == True:
			parens += 1
		elif token == ')' and found == True and parens == 0:
			#create lambda abstraction
			lambda_abs = LambdaAbstraction(' '.join(tokens[q:r]))
			#collect args for lambda
			args = []
			for i in range(lambda_abs.arity):
				args.append(str(stack.pop()))
			#sub args into lambda and add result to stack
			sub_expr = lambda_abs.substitute(*args)
			stack.append(sub_expr)
			found = False
		elif token == ')' and found == True:
			parens -= 1
		elif found == False:
			stack.append(token)
		r += 1
	return ' '.join(stack)

def eval_stmt(stmt):
	#if this an assignment
	if ':=' in stmt:
		#print(f'\nassignment {stmt}')
		#positions of := op
		p = stmt.find(':=')
		identifier = stmt[:p].replace(' ', '')
		#print(f'identifier: {identifier}')
		expr = stmt[p + 3:]
		#for lambda abstraction assignment
		if expr[0] == 'λ':
			#print(f'λ assignment: {expr}')
			lambda_abs_dict[identifier] = LambdaAbstraction(expr)
		#for anon lambda assignments
		elif 'λ' in stmt:
			value = int(anon_lambdas_non_nested(tokenise_expr(expr)))
			var_dict[identifier] = value
		#for integer expression assignments
		else:
			#value of integer expr
			value = eval_expr(tokenise_expr(expr))
			#print(f'integer expression assignment: {value}')
			var_dict[identifier] = value
	#if this is an expression
	else:
		#print(f'\nexpr {stmt}')
		#for anonymous lambda abstractions
		if 'λ' in stmt:
			print(int(anon_lambdas_non_nested(tokenise_expr(stmt))))
		#for integer exprs
		else:
			print(eval_expr(tokenise_expr(stmt)))

if __name__ == '__main__':
	#try get filename as command line arg
	try:
		filename = sys.argv[1]
	except IndexError:
		print('missing filename arg')
		sys.exit()

	#try open file
	try:
		handle = open(filename, 'r')
	except FileNotFoundError:
		print('file not found')
		sys.exit()

	#read program
	prog = ''
	for line in handle.readlines():
		#ignore comments
		if line[:2] == '//':
			continue
		prog += line.replace('\n', '')

	handle.close()

	start = timeit.default_timer()

	#interpret program
	for stmt in prog.split(';')[:-1]:
		eval_stmt(stmt)

	end = timeit.default_timer()

	print(f'[finished in {end - start :0.4f}s]')


