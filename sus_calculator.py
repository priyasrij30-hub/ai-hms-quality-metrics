"""Small SUS calculator for the standard 10-item System Usability Scale.

Usage:
    python sus_calculator.py
Enter one participant's responses, each from 1 to 5. Repeat for each participant.
"""
def score_responses(responses):
    if len(responses) != 10 or any(x not in range(1, 6) for x in responses):
        raise ValueError("Enter exactly 10 responses, each from 1 to 5.")
    adjusted = []
    for idx, response in enumerate(responses, start=1):
        adjusted.append(response - 1 if idx % 2 == 1 else 5 - response)
    return sum(adjusted) * 2.5

def main():
    scores = []
    print("SUS calculator — enter responses from 1 (Strongly disagree) to 5 (Strongly agree).")
    while True:
        raw = input(f"Participant {len(scores)+1}: enter 10 comma-separated responses, or press Enter to finish: ").strip()
        if not raw:
            break
        try:
            responses = [int(x.strip()) for x in raw.split(",")]
            score = score_responses(responses)
            scores.append(score)
            print(f"Participant SUS score: {score:.1f}/100")
        except Exception as exc:
            print(f"Invalid input: {exc}")
    if scores:
        print(f"Respondents: {len(scores)}")
        print(f"Average SUS score: {sum(scores)/len(scores):.1f}/100")
        print("Interpretation: compare cautiously; 68 is a commonly used reference point, not a universal pass/fail cutoff.")
    else:
        print("No responses entered; no score calculated.")

if __name__ == "__main__":
    main()
