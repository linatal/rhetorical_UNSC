from analysis_labelsdistribution import count_relations_per_paragraph
from pathlib import Path
import pandas as pd
import scipy.stats as stats

# TODO: Bonferroni Correction
# TODO: Exclude span and root relations
# TODO: Do one visualization
# TODO: include all in Text

def chi_each_relation(Conflicts,No_Conflicts, all_relations, total_conflicts, total_no_conflicts):
    # Perform Chi-square test for each relation seperately, comparing how often it appears in Conflicts vs No_Conflicts
    # possible downside: Multiple comparisons increase the risk of Type I errors (false positives).
    results = []
    for relation in all_relations:
        conflict_count = Conflicts.get(relation, 0)
        no_conflict_count = No_Conflicts.get(relation, 0)

        # Build a 2x2 contingency table
        #Row 1: Counts for this relation in Conflicts and No_Conflicts
        #Row 2: Remaining occurrences in Conflicts and No_Conflicts
        table = [[conflict_count, no_conflict_count],
                 [total_conflicts - conflict_count, total_no_conflicts - no_conflict_count]]

        # Perform Chi-square test
        chi2, p, _, _ = stats.chi2_contingency(table)

        results.append({"Relation": relation, "Chi2": chi2, "p-value": p})

    # Convert results to DataFrame and sort by p-value
    df_results = pd.DataFrame(results).sort_values("p-value")

    # Print significant results for threshold (p < 0.05) (only significant results)
    print(df_results[df_results["p-value"] < 0.05])
    # Print significant results for threshold (p >= 0.05) (only insignificant results)
    print(df_results[df_results["p-value"] >= 0.05])

def chi_all_relations(Conflicts,No_Conflicts, all_relations, total_conflicts, total_no_conflicts):
    # Build a contingency table (relations as rows, categories as columns)
    all_relations =sorted(all_relations)
    data = []
    for relation in all_relations:
        data.append([Conflicts.get(relation, 0), No_Conflicts.get(relation, 0)])

    # Convert to DataFrame
    df_contingency = pd.DataFrame(data, index=all_relations, columns=["Conflicts", "No_Conflicts"])

    # Perform a single Chi-square test for the whole distribution
    chi2, p, _, _ = stats.chi2_contingency(df_contingency)

    print(f"Global Chi2: {chi2:.2f}, p-value: {p:.5f}")

    if p < 0.05:
        print("Significant overall difference in relation distributions between Conflicts and No_Conflicts (using chi sqared test).")
    else:
        print("No significant overall difference in relation distributions (using chi sqared test).")

def chi_test(Conflicts,No_Conflicts):
    # total occurrences in each category
    total_conflicts = sum(Conflicts.values())
    total_no_conflicts = sum(No_Conflicts.values())

    # Get all unique relations
    all_relations = set(Conflicts.keys()).union(set(No_Conflicts.keys()))
    chi_each_relation(Conflicts,No_Conflicts, all_relations, total_conflicts, total_no_conflicts)
    chi_all_relations(Conflicts,No_Conflicts, all_relations, total_conflicts, total_no_conflicts)


def main():
    csvf_aligned = Path("../data/main_conflicts_aligned.csv")
    #csvf_aligned_parasubtrees = Path("../data/main_conflicts_aligned_paragraphid.csv")
    csvf_aligned = Path("../data/main_conflicts_aligned.csv")
    #df = pd.read_csv(csvf_aligned_parasubtrees, index_col=0)
    df['Conflict_Type'] = df['Conflict_Type'].replace("_", "No_Conflict")

    Count_Conflicts, Count_NoConflicts = count_relations_per_paragraph(df)
    chi_test(Count_Conflicts, Count_NoConflicts)

if __name__ == "__main__":
    main()