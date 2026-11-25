# Homework 3: Optimization Duel

> Draft skeleton. Replace every TODO with the team's choices, evidence, and analysis. Maximum 2,500 words.

## Setup and methods

- **Problems and instances:** TODO: describe Rastrigin and Rosenbrock at 2, 10, and 30 dimensions; choose TSP (20, 30, 50 cities) or knapsack at three sizes. Record bounds, instance generation, and sources.
- **Algorithms:** TODO: name at least three from GA, simulated annealing, PSO, ACO, and ABC. Identify the algorithm written from scratch and explain representations and operators.
- **Baselines:** TODO: describe random search and the relevant problem-specific heuristics: hill climbing with restarts for continuous problems, nearest-neighbour plus 2-opt for TSP, or greedy ratio for knapsack.
- **Protocol:** TODO: state the week 11 `Budget` evaluation cap, counting rules, seeds (at least 10 per configuration), settings, hardware, and reproduction commands. Explain how each method uses the same number of objective evaluations.

## Duel Scorecard

TODO: specify which methods belong in each column, mark any inapplicable comparison explicitly, and link the supporting evidence. Use the same outcome criteria across methods.

| Axis | Classical | LLM | Hybrid | Evidence |
|---|---|---|---|---|
| Correctness | TODO | TODO | TODO | TODO: validity and quality criteria; results across instances |
| Guarantee | TODO | TODO | TODO | TODO: claims and conditions |
| Cost | TODO | TODO | TODO | TODO: evaluations, tokens and CPU time as applicable |
| Latency | TODO | TODO | TODO | TODO: median and p95 per instance |
| Reproducibility | TODO | TODO | TODO | TODO: distinct answers across five repeated runs |
| Scaling | TODO | TODO | TODO | TODO: curve across sizes and instances |
| Interpretability | TODO | TODO | TODO | TODO: explanation or checkable certificate |
| Failure mode | TODO | TODO | TODO | TODO: classify failures and link evidence |

The course scorecard asks for at least four sizes and ten instances per size. TODO: reconcile this with the homework's three prescribed sizes per problem class, and document any added sizes or limitations.

## Results and convergence

TODO: report the final objective values with mean ± standard deviation or median and IQR over seeds. Include the raw CSV files in `results/`. Show convergence against objective evaluations with error bands. Include at least four PNG figures in `fig/`. Report prominently if random search is competitive.

## Hyperparameter study

TODO: identify one algorithm, a grid over at least two parameters, and at least five seeds per setting. Include a results table and heatmap, and discuss which parameters mattered.

## LLM arm

TODO: choose and justify option A or B. Option C alone is not sufficient. Describe inputs, model, prompt, configuration and comparison protocol, and link cached artifacts.

TODO: report token and wall-clock costs, and assess interpretability. For option A, report compile/crash rate and define and defend equal budget against the GA comparison. For option B, compare LLM proposals against random and grid search using the same number of configurations.

## No Free Lunch

TODO: identify which methods suit which problem structures, supported by results. Discuss properties such as multimodality, separability, and discreteness.

## Where we may have been unfair

TODO: assess the equal-budget definition, differences in tuning effort, and whether baselines had a fair shot. Discuss differences in information, instance selection, and any other limitations.

## Conclusion: biological metaphors

TODO: use the results to assess whether the biological metaphors helped explain performance, rather than attributing results to metaphor alone.
