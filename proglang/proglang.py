#Joseph Harrison 2019

#seperate tokens based on whitespace
tokenise = lambda expr: expr.split(' ')

class Lambda:

	def __init__(self, tokens):
		#get body of abstraction
		i = len(tokens) - 1
		#parens accounts for anon lambdas
		parens = 0
		while i > 0 and tokens[i] != '.' or parens != 0:
			if tokens[i] == ')':
				parens += 1
			elif tokens[i] == '(':
				parens -= 1
			i -= 1
		self.body = tokens[i + 1:]
		#get bound variables
		self.bound = []
		for j in range(i):
			if tokens[j] != 'λ' and tokens[j] != '.':
				self.bound.append(tokens[j])
		self.sig = tokens[:i + 1]

	@property
	def arity(self):
		return len(self.bound)
	
	#sub args into body, lambdas can be curried
	#by applying fewer args than the arity
	def sub(self, args):
		ret = list(self.body)
		for i in range(len(args)):
			for j in range(len(ret)):
				if ret[j] == self.bound[i]:
					ret[j] = args[i]
		return ret

	def __repr__(self):
		sig = ' '.join(self.sig)
		body = ' '.join(self.body)
		return sig + ' ' + body

def next_pairing_token(tokens, i, a, b):
	j = 0
	while tokens[i] != b or j != -1:
		i += 1
		if tokens[i] == a:
			j += 1
		elif tokens[i] == b:
			j -= 1
	return i

def eval_expr(tokens):
	stack = []
	i = 0
	while i < len(tokens):
		token = tokens[i]
		if token in atoms:
			atom, arity = atoms[token]
			#pop args from stack
			args = map(float, stack[-arity:])
			stack = stack[:-arity]
			#add result to stack
			stack.append(atom(*args))
		elif token in lambdas:
			lambda_abs = lambdas[token]
			#get args from stack
			args = stack[-lambda_abs.arity:]
			stack = stack[:-lambda_abs.arity]
			#sub args into lambda
			expr = lambda_abs.sub(args)
			#add result to stacks
			stack.append(eval_expr(expr))
		elif token in free_vars:
			stack.append(free_vars[token])
		#anonymous lambdas
		elif token == '(':
			#search for pairing bracket
			j = i
			parens = 0
			flag = True
			while flag:
				j += 1
				if tokens[j] == '(':
					parens += 1
				elif tokens[j] == ')' and parens == 0:
					flag = False
				elif tokens[j] == ')':
					parens -= 1
				elif j == len(tokens) - 1:
					flag = False
			expr = tokens[i + 1:j]
			#create lambda
			lambda_abs = Lambda(expr)
			#call with args
			args = stack[-lambda_abs.arity:]
			stack = stack[:-lambda_abs.arity]
			expr = lambda_abs.sub(args)
			stack.append(eval_expr(expr))
			i = j
		#for branch
		elif token == '?':
			result, i = eval_branch_expr(tokens, i)
			stack.append(result)
		else:
			stack.append(token)
		i += 1
	return stack[0]

def eval_branch_expr(tokens, i):
	#get condition expr
	j = i + 1
	i = next_pairing_token(tokens, i, '?', '->')
	condition = tokens[j:i]
	#get success expr
	j = i + 1
	i = next_pairing_token(tokens, i, '?', '!')
	success = tokens[j:i]
	#get the failure expr
	j = i + 1
	i = next_pairing_token(tokens, i, '?', ':')
	failure = tokens[j:i]
	#branch logic
	if float(eval_expr(condition)) > 0:
		return eval_expr(success), i
	else:
		return eval_expr(failure), i

def parse_stmt(tokens):
	tokens = [item for item in tokens if item != '']
	if tokens[1] == ':=':
		identifier = tokens[0]
		expr = tokens[2:]
		#this is lambda assigment
		if expr[0] == 'λ':
			lambdas[identifier] = Lambda(expr)
		else:
			free_vars[identifier] = eval_expr(expr)
	else:
		print(eval_expr(tokens))

#identifier maps to tuple of function and its arity
atoms = {'+' : (lambda x, y: x + y, 2),
		 '-' : (lambda x, y: x - y, 2),
		 '*' : (lambda x, y: x * y, 2),
		 '%' : (lambda x, y: x % y, 2),
		 '/' : (lambda x, y: x // y, 2)}

free_vars = {}

lambdas = {}
