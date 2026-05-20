 Drop the Constants It is very possible for O(N) code to run faster than 0( 1) code for specific inputs. Big O just describes the rate of increase. For this reason, we drop the constants in runtime. An algorithm that one might have described as 0(2N) is actuallyO(N). Many people resist doing this. They will see code that has two (non-nested) for loops and continue this 0 ( 2N). They think they're being more "precise:'They're not. Consider the below code: 
 ![[Pasted image 20251103143822.png]]
  Which one is faster?The first one does one for loop and the other one does two for loops. But then, the first solution has two lines of code per for loop rather than one. If you're going to count the number of instructions, then you'd have to go to the assembly level and take into account that multiplication requires more instructions than addition, how the compiler would opti mize something, and all sorts of other details. This would be horrendously complicated, so don't even start going down this road. Big O allows us to express how the runtime scales. We just need to accept that it doesn't mean that O(N) is always better than O(N2).

# Drop the Non-Dominant Terms 
What do you do about an expression such as O ( N2 + N)? That second N isn't exactly a constant. But it's not especially important. We already said that we drop constants. Therefore, 0( N2 + N2) would be O ( N2). If we don't care about that latter N2 term, why would we care about N? We don't. You should drop the non-dominant terms. O(N2 + N) becomesO(N2). • O(N + log N) becomesO(N). 0(5*2N + 1000N100) becomes0(2N). We might still have a sum in a runtime. For example, the expression0(82 + A) cannot be reduced (without some special knowledge of A and B). The following graph depicts the rate of increase for some of the common big O times .
![[Pasted image 20251103143959.png]]
As you can see, 0 ( x2) is much worse than O ( x), but it's not nearly as bad as O ( 2x) or O ( x ! ) . There are lots ofruntimes worse than 0( x ! ) too, such as O( xx) or 0( 2x * x ! ) .

# Multi-Part Algorithms:
Add vs. Multiply Suppose you have an algorithm that has two steps. When do you multiply the runtimes and when do you add them? This is a common source of confusion for candidates.
![[Pasted image 20251103144215.png]]
In the example on the left, we do A chunks of work then B chunks of work. Therefore, the total amount of work is O(A + B ). 
In the example on the right, we do B chunks of work for each element in A. Therefore, the total amount of work isO(A * B).
# Amortized Time
An Array List, or a dynamically resizing array, allows you to have the benefits of an array while offering flexibility in size.
An Arraylist is implemented with an array. When the array hits capacity, the Arraylist class will create a new array with double the capacity and copy all the elements over to the new array.
The array could be full. If the array contains N elements, then inserting a new element will take O(N) time. You will have to create a new array of size 2N and then copy N elements over. This insertion will take O ( N) time. 
However, we also know that this doesn't happen very often. The vast majority of the time insertion will be inO(l) time.
We need a concept that takes both into account. This is what amortized time does. It allows us to describe that, yes, this worst case happens every once in a while. But once it happens, it won't happen again for so long that the cost is "amortized:' In this case, what is the amortized time? As we insert elements, we double the capacity when the size of the array is a power of 2. So after X elements, we double the capacity at array sizes 1, 2, 4, 8, 16, ... , X. That doubling takes, respectively, 1, 2, 4, 8, 16, 32, 64, ... , X copies. What is the sum of 1 + 2 + 4 + 8 + 16 + ... + X? If you read this sum left to right, it starts with 1 and doubles until it gets to X. If you read right to left, it starts with X and halves until it gets to 1. What then is the sum ofX + X + X + X + ... + 1 ?This is roughly 2X. Therefore, X insertions take 0( 2X) time. The amortized time for each insertion is 0( 1).
# � Log N Runtimes

We commonly see O(log N) in runtimes. Where does this come from? 

Let's look at binary search as an example. In binary search, we are looking for an example x in an N-element sorted array. We first compare x to the midpoint of the array. If x == middle, then we return. If x < middle, then we search on the left side of the array. If x > middle, then we search on the right side of the array.

We start off with an N-element array to search. Then, after a single step, we're down to Y i elements. One more step, and we're down to % elements. We stop when we either find the value or we're down to just one element.

The total runtime is then a matter of how many steps (dividing N by 2 each time) we can take until N becomes 1.

We could look at this in reverse (going from 1 to 16 instead of 16 to 1 ). How many times we can multiply 1 by 2 until we get N?

What is k in the expression 2k = N? This is exactly what log expresses.

This is a good takeaway for you to have. When you see a problem where the number of elements in the problem space gets halved each time, that will likely be a 0( log N) runtime.

This is the same reason why finding an element in a balanced binary search tree is O ( log N). With each comparison, we go either left or right. Half the nodes are on each side, so we cut the problem space in half each time.
# Recursive Runtimes
Here's a tricky one. What's the runtime of this code?
![[Pasted image 20251103145146.png]]
Rather than making assumptions, let's derive the runtime by walking through the code. Suppose we call f ( 4). This calls f ( 3) twice. Each of those calls to f ( 3) calls f ( 2), until we get down to f ( 1 ). f(4) A lot of people will, for some reason, see the two calls to f and jump to 0( N2). This is completely incorrect.

How many calls are in this tree? (Don't count!).

The tree will have depth N. Each node (i.e., function call) has two children. Therefore, each level will have twice as many calls as the one above it. The number of nodes on each level is:
![[Pasted image 20251103145408.png]]
Try to remember this pattern. When you have a recursive function that makes multiple calls, the runtime will often (but not always) look like O( branches^depth), where branches is the number of times each recursive call branches. In this case, this gives us O ( 2^N).

 As you may recall, the base of a log doesn't matter for big O since logs of different bases are only different by a constant factor. However, this does not apply to exponents. The base of an exponent does matter. Compare 2" and 8". If you expand 8", you get (23)", which equals 23", which equals 22" * 2". As you can see, 8" and 2° are different by a factor of 22". That is very much not a constant factor 

The space complexity of this algorithm will be O(N). Although we have 0(2^N) nodes in the tree total, only O(N) exist at any given time. Therefore, we would only need to have O(N) memory available