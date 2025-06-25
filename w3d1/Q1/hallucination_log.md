# Hallucination Log

## Case 1
**Prompt Type:** Zero-shot  
**Query:** “What is the area?”  
**Issue:** The model assumed a square and gave an answer without clarification.

## Case 2
**Prompt Type:** CoT  
**Query:** “Check: 2x + 4 = 10. I solved x = 3.”  
**Issue:** Model incorrectly validated wrong answer. Correct x = 3 is false.
