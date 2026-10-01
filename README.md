# Binary Grey Wolf Optimizer (Python)

Each wolf holds `n` integer bits: `0` means a parameter is off and `1` means on.
For example, `[1, 0, 1, 0]` enables the first and third parameters. `dimensions`
is the parameter count. Only Python's standard library is required.

```powershell
python gwo.py --parameters 10 --wolves 30 --iterations 100 --seed 42
```

`--dimensions` is also accepted. Output includes the best binary list, fitness,
and elapsed milliseconds. Iteration fitness is written to `results.txt`
(overwritten each run); use `--output` to choose another file.

## Custom objective

The objective receives only integer zeros and ones and returns a finite score;
smaller is better. The default minimizes the number of enabled parameters, so its
ideal answer is all zeros. Replace it with your actual scoring function.

```python
from gwo import run_gwo, print_results

def objective_function(parameters):
    target = [1, 0, 1, 1, 0]
    return sum(bit != wanted for bit, wanted in zip(parameters, target))

result = run_gwo(objective_function, dimensions=5, num_wolves=30,
                 max_iterations=100, seed=42, output_path=None)
print_results(result)
```

`output_path=None` disables file output. Results include `best_position` (the
binary list), `best_fitness`, fitness history, and elapsed time. Zero iterations
returns the best initialized wolf. Seeds make Python runs reproducible.

## Binary update

Initial bits independently have equal probability of zero or one. For each bit,
the original GWO equations generate proposals from alpha, beta, and delta. Their
average is clipped to [0, 1] and sampled as the probability of enabling that bit.
For example, 0.8 gives an 80% chance of one. Only sampled integer bits are stored
and evaluated. This is a binary adaptation of the continuous optimizer.

Leaders update after each wolf and retain independent snapshots of the three
best evaluations, including ties. The C++ out-of-bounds fitness write and missing
leader demotion are corrected. This heuristic does not guarantee the global
optimum; a bit that becomes zero in all wolves and leaders cannot turn on again
under this update rule.

The original ObjectiveFunction.hpp was not supplied. The default objective and
settings (2 parameters, 30 wolves, 100 iterations) are examples. gwo.cpp retains
the original continuous implementation.

Run checks with `python -m unittest -v`.
