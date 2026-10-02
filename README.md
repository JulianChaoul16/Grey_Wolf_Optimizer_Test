# Binary Grey Wolf Optimizer

This Python implementation searches for a good combination of on/off parameters using an algorithm inspired by the hunting behavior of grey wolves. Each wolf represents a candidate solution with n binary values: 0 turns a parameter off, and 1 turns it on.

A fitness function scores each combination, with lower scores representing better solutions. The three best solutions found guide the wolves as they explore and refine their parameter choices over repeated iterations.

The algorithm returns the best combination found and its fitness score. It can be used for feature selection and other problems that involve choosing which options to enable.
