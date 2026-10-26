# QuickMed Member 4 Package

## Run the dashboard
1. Extract this folder.
2. Open the folder in VS Code.
3. In the VS Code terminal run:
   `python -m pip install -r requirements.txt`
4. Run:
   `python -m streamlit run app.py`

## Important data note
`metrics.csv` contains preliminary figures supplied in the project discussion and `TBD` placeholders. These are not final verified results. Confirm all preliminary values with the teammates and replace every TBD field with actual measurements. Confirm the team's official selected metric list and thresholds; the file includes a broad working inventory, not a claim that every row belongs to the final agreed metric set.

## CSV columns
- Metric: metric name
- Category: correctness, AI quality, maintainability, security, or usability
- Stage: Before AI / With AI / After fix
- Value: measured numeric value or TBD
- Unit: value unit
- Threshold: human-readable target
- Direction: higher or lower; leave as agreed/blank for metrics where direction isn't meaningful
- Target: numeric target for automatic status; TBD until agreed
- Source: evidence/report used
- Notes: interpretation and work still needed

The app computes Green/Amber/Red only when Value, Target, and Direction are valid. The Amber band is a simple dashboard convention (within 10% below a higher-is-better target or up to 20% above a lower-is-better target); replace this with your team's formally agreed rules if different.
