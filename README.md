# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation is the repeated application of task specific rules 
until a solution is found or no further progress can be made.

In case of the "naked twins" it means that 2 boxes from a set of peers have the 
same two solutions available. While it is unclear which digit goes into which box,
we know that no other (peer) boxes can obtain either of those two numbers.

The programmed solution looks first for pairs of boxes with the same two 
potential digits, then checks for units they both appear in and eliminate the locked
numbers from all peers.

An advanced explanation can be found [here](http://www.sudokuwiki.org/naked_candidates).

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In diagonal sudokus, the same rules that apply for rows, columns and squares, 
also applies to diagonals. This means the middle "X" can also contain numbers 
one through nine only once per line.

Due to the solution architecture, adding the diagonal peers to the general set 
of peers sufficiently satisfies the constraint.
An additional condition for the "naked twins" was implemented as well.

Attention: variable `DIAGONAL` has to be `True` to solve diagonal Sudokus and 
should be set to `False` if the Sudoku to solve is not diagonal in nature. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

