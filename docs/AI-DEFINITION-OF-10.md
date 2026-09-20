# Definition of 10 — AI Product Quality Standard

Status: Reusable quality standard

A 10 is not perfection. A 10 is the highest practical quality state in which no material weakness remains relative to the intended purpose, audience, constraints, and release environment.

## The 20 Quality Dimensions

### 1. Purpose
The product solves the intended human problem.

### 2. North Star
Every major decision supports the intended outcome.

### 3. Clarity
A first-time user understands what this is, why it matters, and what to do next.

### 4. Content
The information is correct, useful, appropriately concise, and well sequenced.

### 5. Personalization
The experience reflects the user's real context when personalization is intended.

### 6. Information Architecture
The structure feels obvious and intentional.

### 7. Visual Design
Typography, layout, color, forms, spacing, imagery, depth, and hierarchy work together.

### 8. Emotional Impact
The experience creates the intended emotional response without manipulation or empty hype.

### 9. User Experience
Interactions and navigation feel natural and low-friction.

### 10. Interaction Quality
Buttons, controls, states, feedback, hover, focus, touch, loading, errors, and success states work as intended.

### 11. Data Integrity
Real data is used correctly. No invented production results.

### 12. Technical Reliability
The product remains stable during normal use and known failure conditions.

### 13. Regression Safety
Changes do not silently break proven capabilities.

### 14. Responsive Quality
The experience is intentionally good across target screen sizes.

### 15. Accessibility
People with different interaction and sensory needs can use the product meaningfully.

### 16. Performance
The product is fast and efficient enough for its intended audience and devices.

### 17. Maintainability
The implementation can be changed safely without repeatedly rebuilding the entire product.

### 18. Release Readiness
The intended publishing environment can actually run the product.

### 19. Trust
The product is truthful about what it does, what it knows, and what it has verified.

### 20. Pride Test
A thoughtful human would be proud to receive it, use it, recommend it, and put their name on it.

## Scoring

Use 0–10 for each dimension.

0 = absent or broken
5 = usable but materially weak
7 = good
8 = strong
9 = excellent
10 = exceptional and no material weakness remains

Do not average away critical failures.

A product cannot be considered 10 overall if any critical dimension is materially below 9.

## Evidence Rule

Each 9–10 claim should have evidence appropriate to the dimension:

- source inspection;
- automated test;
- browser behavior;
- screenshot/video review;
- real-data test;
- performance measurement;
- accessibility inspection;
- live deployment verification;
- human approval.

"Looks good" is not evidence for functionality.

"Tests pass" is not evidence for emotional impact.

"AI says 10" is not evidence.

## Highest-Value Gap Rule

When improving a product, identify the three biggest gaps by impact, not the three easiest fixes.

Fix the highest-impact gap first.

Then verify and regression-test.

## Completion Rule

A project is finished when:

- all critical requirements are complete;
- all material Change Ledger items are complete;
- no critical regressions remain;
- the intended release environment works;
- the human Director is satisfied.
