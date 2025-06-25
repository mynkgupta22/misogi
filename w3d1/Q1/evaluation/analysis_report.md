# Prompt Strategy Evaluation

## Metrics Used
- Accuracy (1 = correct, 0 = incorrect)
- Reasoning Clarity (Good / Average / Poor)
- Hallucination (0 = none, 1 = minor, 2 = major)
- Consistency (manual observation)

## Observations

| Prompt Type | Accuracy | Reasoning Clarity | Avg. Hallucination |
|-------------|----------|-------------------|--------------------|
| Zero-Shot   | 3/5      | Poor              | 1.2                |
| Few-Shot    | 4/5      | Good              | 0.5                |
| CoT         | 5/5      | Excellent         | 0.2                |
| Meta        | 4/5      | Good              | 0.2                |

## Conclusion
Chain-of-thought prompts gave the most reliable and explainable answers, while meta-prompts effectively handled ambiguous queries.
