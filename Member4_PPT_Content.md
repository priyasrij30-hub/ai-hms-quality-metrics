# Member 4 — PPT Slide Content

## Slide 1: Software Quality Dashboard
- QuickMed: Continuous Software Quality and Reliability Assessment
- Dashboard consolidates correctness, AI quality, maintainability, security, and usability metrics.
- Displays values, thresholds, status, stage, and evidence source.
- Current dashboard is a working prototype; final verified data must be entered.

## Slide 2: Correctness and Reliability Metrics
- Test pass rate: preliminary 88.2% → 91.2%
- Test failure rate: preliminary 11.8% → 8.8%
- Defect density: preliminary 23.0 → 21.8 → 17.5 defects/KLOC
- Test flakiness: preliminary 0%
- Code coverage: preliminary 99% before AI and 84.9% with AI
- Explain that all values require confirmation against final CI reports.

## Slide 3: Usability Evaluation
- Lighthouse pages: Login, Home, Register Patient, Risk Prediction.
- Record Performance and Accessibility scores under consistent test conditions.
- SUS: 10 standard questions, 8–10 classmates targeted.
- SUS scoring: odd items response − 1; even items 5 − response; total × 2.5.
- Report average SUS score and number of respondents; 68 is a common reference point.

## Slide 4: Conclusion
- A combined set of metrics gives a more complete view than any single measure.
- Preliminary test pass rate improved and failure rate decreased in the reported later run.
- AI integration can change coverage and introduce additional reliability, security, and usability concerns.
- Final conclusions depend on verified team measurements.

## Slide 5: Future Work
- Automate metrics extraction from CI.
- Track quality trends across commits.
- Expand AI edge-case and input-validation tests.
- Continue security/dependency scans.
- Repeat usability evaluation after improvements.
- Document model limitations, privacy, and human oversight.
