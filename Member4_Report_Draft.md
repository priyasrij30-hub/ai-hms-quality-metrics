# Member 4 Report Draft — QuickMed Software Quality and Reliability Assessment

> **Before submission:** This is a draft template. Replace bracketed items and preliminary numbers with verified team results. Do not report TBD fields as findings.

## Performance and quality metrics

The team evaluated the QuickMed hospital management system using a combination of test reliability, code coverage, defect density, AI-model quality, maintainability, security, and usability measures. The measurements were intended to provide a repeatable view of software quality before AI integration, with AI functionality enabled, and after fixes where comparison data were available.

### Preliminary correctness/reliability observations

The preliminary figures shared by the team indicate a test pass rate of 88.2% before the relevant changes and 91.2% in the later measurement. Test failure rate changed from 11.8% to 8.8%. Defect density was reported as 23.0, 21.8, and 17.5 defects/KLOC across the recorded stages. Test flakiness was reported as 0%. Code coverage was reported as 99% before AI integration and 84.9% with AI integration. These values are preliminary and must be confirmed against the final pipeline output before submission.

Coverage can fall after adding AI-related code if the newly added paths are not exercised by the existing tests. This does not by itself prove the software became less reliable; coverage should be interpreted alongside test results, the amount of code added, and the types of paths tested.

### AI model quality

The AI feature should be assessed using accuracy, precision, recall, and F1 score from Member 2's verified evaluation. Insert the final values, the test dataset size, and the evaluation method here. For a healthcare prediction feature, explain the trade-off between false positives and false negatives and avoid claiming clinical suitability from software metrics alone.

**Final AI results:** [Insert verified accuracy, precision, recall, F1 score, test-set details, and limitations.]

### Maintainability and security

Member 2's maintainability measurements include cyclomatic complexity, maintainability index, code duplication, and comment density. Member 3's security checks include Bandit findings, vulnerable/risky dependency results from pip-audit, and the hardcoded-secret finding. Report counts by severity, the status of each fix, and evidence from the final scan. Do not include any actual secret values in the report.

**Final maintainability results:** [Insert verified values and agreed thresholds.]

**Final security results:** [Insert final scan date, tool versions if known, severity counts, dependency findings, and fixes.]

### Usability

Lighthouse was planned for the login, home, register-patient, and risk-prediction pages. Record Performance and Accessibility scores for each page under consistent test conditions. The System Usability Scale (SUS) survey should use the standard ten questions and actual responses from 8–10 classmates, after a short task-based trial of the app.

For each respondent, score odd-numbered items as response minus 1 and even-numbered items as 5 minus response. Sum the ten adjusted values and multiply by 2.5 to obtain a SUS score from 0 to 100. Report the mean of the respondent scores and the number of respondents. A score of 68 is a commonly used reference point, not a universal pass/fail rule.

**Lighthouse results:** [Insert scores for all four pages.]

**SUS result:** [Insert respondent count, average score, and key qualitative feedback.]

## Conclusion

This project establishes a metrics-based workflow for evaluating software quality and reliability in QuickMed as AI functionality is integrated. The dashboard brings selected measurements into one view and supports comparison across development stages. Preliminary test results suggest that the later run had a higher test pass rate and lower test failure rate than the earlier run, while defect density also decreased across the reported stages. These observations must be validated using the team's final evidence.

No single metric is sufficient to establish overall quality. Test results should be interpreted together with coverage, AI-model evaluation, maintainability, security scans, and usability evidence. Because QuickMed includes a healthcare-related prediction feature, its output should not be treated as a clinical diagnosis and the project should clearly document dataset limitations and the need for appropriate validation.

## Future work

1. Replace all preliminary and TBD values with final measurements and preserve links or screenshots to the evidence.
2. Automate dashboard updates from the CI pipeline so that each run refreshes the test, coverage, defect, and security metrics.
3. Add time-series tracking and trend charts to detect regressions across commits.
4. Add severity-aware security reporting and dependency monitoring.
5. Expand tests for AI input validation, edge cases, model performance, and failure handling.
6. Collect usability feedback from a larger and more representative user group and repeat testing after UI improvements.
7. Document data provenance, privacy safeguards, model limitations, and human oversight for the AI prediction feature.
