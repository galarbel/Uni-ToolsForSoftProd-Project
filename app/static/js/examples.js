var noDafExample = `# @noDafny
a = 5
print(a)
print(a+10)`


var example1 = `def MultipleReturns(x,y):
# @types: x: int
# @types: y: int
# @returns: more: int, less: int
# @requires: 0 < y
# @ensures: less < x < more
   more = x + y
   less = x - y
   return more,less`;
   
var example2 = `def Abs(x):
# @types: x: int
# @returns: y: int
# @ensures: y >= 0
    if (x < 0):
        return -x
    else:
        return x`
		
var example3 = `def Find(a, key):
# @types: a: array<int>
# @types: key: int
# @returns: index: int
# @requires: a != null
# @ensures: 0 <= index ==> index < a.Length && a[index] == key
# @ensures: index < 0 ==> forall k :: 0 <= k < a.Length ==> a[k] != key
	index = 0
	while index < a.Length:
		# @invariant: 0 <= index <= a.Length
		# @invariant: forall k :: 0 <= k < index ==> a[k] != key
		if a[index] == key:
			return
		index = index + 1
	index = -1
	return index`;
	
var example4 = `def Find(a, key):
# @types: a: array<int>
# @types: key: int
# @returns: index: int
# @requires: a != null
# @ensures: 0 <= index ==> index < a.Length && a[index] == key
# @ensures: index < 0 ==> forall k :: 0 <= k < a.Length ==> a[k] != key
	for index in range (a.Length):
		# @invariant: 0 <= index <= a.Length
		# @invariant: forall k :: 0 <= k < index ==> a[k] != key
		if a[index] == key:
			return		
	index = -1
	return index`;
	

	
	
/*-----------------------------
-----------HomeWork------------
-----------------------------*/

var hw1_8 = `def final_grade(exam, hw):
    # @types: exam: real
    # @types: hw: real
    # @returns: x: int
    # @ensures: x == (0.75 * exam + 0.25 * hw).Floor || x == (0.75 * exam + 0.25 * hw).Floor +1
	
	result = 0
	
	#add your code here
	
	return result`
	
var hw1_8sol =`def final_grade(exam, hw):
    # @types: exam: real
    # @types: hw: real
    # @returns: x: int
    # @ensures: x == (0.75 * exam + 0.25 * hw).Floor || x == (0.75 * exam + 0.25 * hw).Floor +1
    
	result = 0
	
    result = round(0.75 * exam + 0.25 * hw)

	return result`

var hw1_9 = `def max2(n1, n2):
    # @types: n1: int
    # @types: n2: int
    # @returns: x: int
    # @ensures n1 >= n2 ==> x == n1 && n2 > n1 ==> x == n2
    result = n2
    if n1 >= n2:
        result = n1
    return result
	
	`	
	
	
var hw2 = `def mystery(lst, j):
# @types: lst: array<int>
# @types: j: int
# @requires: lst != null && lst.Length > 0 && 0 < j <= lst.Length 
# @modifies: lst
# @ensures: forall l:: 0 <= l < j ==> lst[l] >= lst[j-1]   
	index=0
	tmp=lst[0]
	## Complete: As long as index is less than j-1:
	    # @invariant: 0 <= index <= j-1 && forall l:: 0 <= l <= index ==> lst[l] >= lst[index]
		## Complete: If the list value at index greater than the the list value at index+1 then:
            ## Complete: assign tmp variable to list value at index 
            ## Complete: assign the list value at index to list value at index+1
            ## Complete: assign the list value at index+1 to the value of tmp
        ## Complete: Increase index by 1


def mystery2(lst):
# @types: lst: array<int>
# @returns: res: int
# @requires: lst != null
# @requires: lst.Length > 0
# @modifies: lst
    ## Complete: assign listlen variable to lst length 
	## Complete: As long as listlen is greater than 0:
		mystery(lst,listlen)
		## Complete: decrease index by 1`
	
var hw2sol = `def mystery(lst, j):
# @types: lst: array<int>
# @types: j: int
# @requires: lst != null && lst.Length > 0 && 0 < j <= lst.Length 
# @modifies: lst
# @ensures: forall l:: 0 <= l < j ==> lst[l] >= lst[j-1]   
	index=0
	tmp=lst[0]
	while(index<j-1):
	    # @invariant: 0 <= index <= j-1 && forall l:: 0 <= l <= index ==> lst[l] >= lst[index]
		if ( lst[index] < lst [index+1]):
			tmp = lst[index]
			lst[index] = lst[index+1]
			lst[index+1]=tmp
		index = index + 1


def mystery2(lst):
# @types: lst: array<int>
# @returns: res: int
# @requires: lst != null
# @requires: lst.Length > 0
# @modifies: lst
	listlen = len(lst)
	while(listlen>0):
		mystery(lst,listlen)
		listlen = listlen-1`