import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
import seaborn as sns
from collections import Counter
import ast

def flatten_comprehension(matrix):
    return [item for row in matrix for item in row]
def devide_sum(row, devider):
    return
def conflicts_to_binary(df):
    df = df.replace("_", "No_Conflict")
    df = df.replace("Indirect_NegEval", "Conflict")
    df = df.replace("Direct_NegEval", "Conflict")
    df = df.replace("Challenge", "Conflict")
    df = df.replace("Correction", "Conflict")
    return df

def count_labels_flat_all_conflicttypes(df):
    #begin with leave nodes relation conflict versus non-conflict
    df = df.replace("_", "No_Conflict")
    crosstb = pd.crosstab(df['Conflict_Type'], df['rstree_relation_leave'])
    crosstb['sum'] = crosstb.sum(axis=1)
    #crosstb.to_csv("/Users/karolinazaczynska/Documents/Potsdam/code/UNSC_Sigdial/UNSC_RST/other/labelsdistr_flat_all.csv")
    # get proportion of labels distribution per conflict type
    crosstb_new = crosstb.loc[:, "antithesis":"unless"].div(crosstb["sum"], axis=0)
    crosstb_new_perc = crosstb_new *100
    crosstb_new_perc = crosstb_new_perc.transpose()
    #crosstb_new_perc_sm = crosstb_new_perc.loc[["antithesis", "attribution", "cause", "concession", "conjunction", "contrast", "e-elaboration", "elaboration", "evidence", "joint", "list", "preparation", "purpose"]]

    counts_new_perc = crosstb_new_perc.drop("span")
    counts_new_perc = counts_new_perc.drop("sameunit")
    #counts_new_perc = counts_new_perc.drop("summary")
    counts_new_perc = counts_new_perc.drop("textual-organization")
    counts_new_perc = counts_new_perc.drop("topic-comment")
    counts_new_perc = counts_new_perc.drop("unless")
    #counts_new_perc = counts_new_perc.drop("means")
    counts_new_perc = counts_new_perc.drop("otherwise")
    counts_new_perc = counts_new_perc.drop("solutionhood")

    counts_new_perc.loc['reason-N'] += counts_new_perc.loc['reason-S']
    counts_new_perc.loc['evaluation-N'] += counts_new_perc.loc['evaluation-S']
    counts_new_perc = counts_new_perc.drop('reason-S')
    counts_new_perc = counts_new_perc.drop('evaluation-S')
    counts_new_perc = counts_new_perc.rename({'reason-N': "reason", 'evaluation-N': "evaluation"})

    index_list = [ 'attribution',
                   'background', 'enablement', 'evaluation', 'evidence', 'motivation', 'reason',
                   'antithesis', 'concession', 'contrast',
                   'cause', 'circumstance', 'condition', 'e-elaboration', 'elaboration', 'interpretation',
                   'means', 'purpose', 'result',
                   'preparation', 'restatement', 'summary',
                   'list',  'conjunction',  'joint', 'sequence']
    counts_new_perc = counts_new_perc.reindex(index_list)
    plt.style.use('seaborn-v0_8-dark')
    plt.rc('font', size=14)
    plt.rc('xtick', labelsize=14)
    colors= {'Correction': "gold", 'Challenge': "goldenrod", 'Direct_NegEval': "cornflowerblue", 'Indirect_NegEval': "lightsteelblue", 'No_Conflict': "crimson"}

    #ax = counts_new_perc.plot.bar()
    ax = counts_new_perc.plot.bar(width = 0.7, color=colors)
    plt.axvline([0.5], color= "black", linestyle="dashed")
    plt.axvline([6.5], color= "black", linestyle="dashed")
    plt.axvline([9.5], color= "black", linestyle="dashed")
    plt.axvline([18.5], color= "black", linestyle="dashed")
    plt.axvline([21.5], color= "black", linestyle="dashed")


    ax.set_axisbelow(True)
    ax.grid()
    plt.xlabel("RST Label in Leave Node")
    plt.ylabel("Proportion (%) within Conflict Type")
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=12)
    plt.show()


def count_labels_flat_binary(df):
    df = conflicts_to_binary(df)
    crosstb = pd.crosstab(df['Conflict_Type'], df['rstree_relation_leave'])
    crosstb['sum'] = crosstb.sum(axis=1)
    # get proportion of labels distribution per conflict type
    crosstb_new = crosstb.loc[:, "antithesis":"unless"].div(crosstb["sum"], axis=0)
    crosstb_new_perc = crosstb_new *100
    crosstb_new_perc = crosstb_new_perc.transpose()
    #crosstb_new_perc = crosstb_new_perc.loc[
    #    ["antithesis", "attribution", "background", "cause", "circumstance", "concession", "condition", "conjunction", "contrast", "e-elaboration", "elaboration", "evaluation-S", "elaboration",
    #     "evidence", "list", "preparation", "purpose", "reason-S", "restatement", "result", "sequence"]]
    counts_new_perc = crosstb_new_perc.drop("span")
    counts_new_perc = counts_new_perc.drop("sameunit")
    #counts_new_perc = counts_new_perc.drop("summary")
    counts_new_perc = counts_new_perc.drop("textual-organization")
    counts_new_perc = counts_new_perc.drop("topic-comment")
    counts_new_perc = counts_new_perc.drop("unless")
    #counts_new_perc = counts_new_perc.drop("means")
    counts_new_perc = counts_new_perc.drop("otherwise")
    counts_new_perc = counts_new_perc.drop("solutionhood")

    counts_new_perc.loc['reason-N'] += counts_new_perc.loc['reason-S']
    counts_new_perc.loc['evaluation-N'] += counts_new_perc.loc['evaluation-S']
    counts_new_perc = counts_new_perc.drop('reason-S')
    counts_new_perc = counts_new_perc.drop('evaluation-S')
    counts_new_perc.rename({'reason-N': "reason", 'evaluation-N': "evaluation"})

    ax = counts_new_perc.plot.bar()
    ax.set_axisbelow(True)
    ax.grid()
    ax.set_ylim(ymin=0, ymax=18)
    plt.xlabel("RST Label in Leave Node")
    plt.ylabel("Proportion (%) labels Conflicts vs. No Conflicts")
    plt.show()




def count_labels_paragraph_ConflictType(df):
    # counts proportion of relations in paragraohs including at least one conflict-EDU vs no conflicts at all,
    # counting all relations in a paragraph
    df = conflicts_to_binary(df)
    # preparing coubts dataframe
    para_idxs = df['paragraph_id_consecutive'].drop_duplicates().tolist()
    confl_para_list_big = []
    noconfl_para_list_big = []
    for p_idx in para_idxs:
        df_para = df[df['paragraph_id_consecutive'] == p_idx]
        # Check if "Conflict" Exists in Column/paragraph
        if (df_para['Conflict_Type'].eq("Conflict")).any():
            for index, row in df_para.iterrows():
                # get df['rstree_nodeid_chain'] row from str to lists
                y_str = row['rstree_relation_chain_subtree']
                y = ast.literal_eval(y_str)
                confl_para_list_big.append(y)
        elif (df_para['Conflict_Type'].eq("No_Conflict")).any():
            for index, row in df_para.iterrows():
                # get df['rstree_nodeid_chain'] row from str to lists
                y_str = row['rstree_relation_chain_subtree']
                y = ast.literal_eval(y_str)
                noconfl_para_list_big.append(y)

    confl_para_list_big = flatten_comprehension(confl_para_list_big)
    noconfl_para_list_big = flatten_comprehension(noconfl_para_list_big)
    df_confl = pd.DataFrame(confl_para_list_big, columns=['Conflict_RST_labels'])
    df_noconfl = pd.DataFrame(noconfl_para_list_big, columns=['NoConflict_RST_labels'])
    counts_confl = df_confl['Conflict_RST_labels'].value_counts()
    counts_noconfl = df_noconfl['NoConflict_RST_labels'].value_counts()
    counts = pd.concat([counts_confl, counts_noconfl], axis=1)
    # replace NaN Value with zero
    counts = counts.fillna(0)
    counts['NoConflict_RST_labels'] = counts['NoConflict_RST_labels'].astype(int)
    counts = counts.rename(columns={"Conflict_RST_labels" : "Conflict", "NoConflict_RST_labels": "No_Conflict"})

    sum_series = counts.sum()
    sum_list = sum_series.tolist()
    counts = counts.sort_index()

    counts.loc[len(counts)] = sum_list
    counts = counts.rename({35: 'sum'})
    # get proportion of labels distribution per conflic vs no-conflict paragraoh
    counts_new = counts.loc["antithesis":"unless", :].div(counts.loc["sum"], axis=1)
    counts_new_perc = counts_new *100

    counts_new_perc = counts_new_perc.drop("span")
    counts_new_perc = counts_new_perc.drop("sameunit")
    counts_new_perc = counts_new_perc.drop("summary")
    counts_new_perc = counts_new_perc.drop("textual-organization")
    counts_new_perc = counts_new_perc.drop("topic-comment")
    counts_new_perc = counts_new_perc.drop("unless")
    counts_new_perc = counts_new_perc.drop("means")
    counts_new_perc = counts_new_perc.drop("otherwise")
    counts_new_perc = counts_new_perc.drop("solutionhood")

    counts_new_perc.loc['reason-N'] += counts_new_perc.loc['reason-S']
    counts_new_perc.loc['evaluation-N'] += counts_new_perc.loc['evaluation-S']
    counts_new_perc = counts_new_perc.drop('reason-S')
    counts_new_perc = counts_new_perc.drop('evaluation-S')
    counts_new_perc.rename({'reason-N': "reason", 'evaluation-N': "evaluation"})
    ax = counts_new_perc.plot.bar()
    ax.set_axisbelow(True)
    ax.grid()
    plt.xlabel("RST Label in Paragraph")
    plt.ylabel("Proportion (%) labels in Conflicts vs. No Conflicts")
    plt.show()
    print()


def count_labels_paragraph_all_conflicttypes(df):
    # counts proportion of relations in paragraohs including at least one conflict-EDU comparing all conflict types,
    # counting all relations in a paragraph
    # preparing coubts dataframe
    df = df.replace("_", "No_Conflict")
    para_idxs = df['paragraph_id_consecutive'].drop_duplicates().tolist()
    dconfl_para_list_big = []
    iconfl_para_list_big = []
    chalconfl_para_list_big = []
    corrconfl_para_list_big = []
    noconfl_para_list_big = []
    for p_idx in para_idxs:
        df_para = df[df['paragraph_id_consecutive'] == p_idx]
        # Check if "Conflict" Exists in Column/paragraph
        if (df_para['Conflict_Type'].eq("Direct_NegEval")).any():
            for index, row in df_para.iterrows():
                # get df['rstree_nodeid_chain'] row from str to lists
                y_str = row['rstree_relation_chain_subtree']
                y = ast.literal_eval(y_str)
                dconfl_para_list_big.append(y)
        elif (df_para['Conflict_Type'].eq("Indirect_NegEval")).any():
            for index, row in df_para.iterrows():
                # get df['rstree_nodeid_chain'] row from str to lists
                y_str = row['rstree_relation_chain_subtree']
                y = ast.literal_eval(y_str)
                iconfl_para_list_big.append(y)
        elif (df_para['Conflict_Type'].eq("Challenge")).any():
            for index, row in df_para.iterrows():
                # get df['rstree_nodeid_chain'] row from str to lists
                y_str = row['rstree_relation_chain_subtree']
                y = ast.literal_eval(y_str)
                chalconfl_para_list_big.append(y)
        elif (df_para['Conflict_Type'].eq("Correction")).any():
            for index, row in df_para.iterrows():
                # get df['rstree_nodeid_chain'] row from str to lists
                y_str = row['rstree_relation_chain_subtree']
                y = ast.literal_eval(y_str)
                corrconfl_para_list_big.append(y)
        elif (df_para['Conflict_Type'].eq("No_Conflict")).any():
            for index, row in df_para.iterrows():
                # get df['rstree_nodeid_chain'] row from str to lists
                y_str = row['rstree_relation_chain_subtree']
                y = ast.literal_eval(y_str)
                noconfl_para_list_big.append(y)

    dconfl_para_list_big = flatten_comprehension(dconfl_para_list_big)
    iconfl_para_list_big = flatten_comprehension(iconfl_para_list_big)
    chalconfl_para_list_big = flatten_comprehension(chalconfl_para_list_big)
    corrconfl_para_list_big = flatten_comprehension(corrconfl_para_list_big)
    noconfl_para_list_big = flatten_comprehension(noconfl_para_list_big)

    df_dconfl = pd.DataFrame(dconfl_para_list_big, columns=['Direct_NegEval'])
    df_iconfl = pd.DataFrame(iconfl_para_list_big, columns=['Indirect_NegEval'])
    df_chalconfl = pd.DataFrame(chalconfl_para_list_big, columns=['Challenge'])
    df_corrconfl = pd.DataFrame(corrconfl_para_list_big, columns=['Correction'])
    df_noconfl = pd.DataFrame(noconfl_para_list_big, columns=['No_Conflict'])

    counts_dconfl = df_dconfl['Direct_NegEval'].value_counts()
    counts_iconfl = df_iconfl['Indirect_NegEval'].value_counts()
    counts_chalconfl = df_chalconfl['Challenge'].value_counts()
    counts_corrconfl = df_corrconfl['Correction'].value_counts()
    counts_noconfl = df_noconfl['No_Conflict'].value_counts()

    counts = pd.concat([counts_chalconfl, counts_corrconfl, counts_dconfl, counts_iconfl, counts_noconfl], axis=1)
    # replace NaN Value with zero
    counts = counts.fillna(0)
    counts = counts.astype(int)

    sum_series = counts.sum()
    sum_list = sum_series.tolist()
    counts = counts.sort_index()

    counts.loc[len(counts)] = sum_list
    counts = counts.rename({35: 'sum'})
    # get proportion of labels distribution per conflic vs no-conflict paragraoh
    counts_new = counts.loc["antithesis":"unless", :].div(counts.loc["sum"], axis=1)
    counts_new_perc = counts_new *100

    counts_new_perc = counts_new_perc.drop("span")
    counts_new_perc = counts_new_perc.drop("sameunit")
    #counts_new_perc = counts_new_perc.drop("summary")
    counts_new_perc = counts_new_perc.drop("textual-organization")
    counts_new_perc = counts_new_perc.drop("topic-comment")
    counts_new_perc = counts_new_perc.drop("unless")
    #counts_new_perc = counts_new_perc.drop("means")
    counts_new_perc = counts_new_perc.drop("otherwise")
    counts_new_perc = counts_new_perc.drop("solutionhood")

    counts_new_perc.loc['reason-N'] += counts_new_perc.loc['reason-S']
    counts_new_perc.loc['evaluation-N'] += counts_new_perc.loc['evaluation-S']
    counts_new_perc = counts_new_perc.drop('reason-S')
    counts_new_perc = counts_new_perc.drop('evaluation-S')
    counts_new_perc = counts_new_perc.rename({'reason-N': "reason", 'evaluation-N': "evaluation"})

    # small table:
    counts_new_perc = counts_new_perc.loc[['attribution',
                   'background', 'enablement', 'evaluation', 'evidence', 'motivation', 'reason',
                   'antithesis', 'concession', 'contrast']]
    plt.style.use('seaborn-v0_8-dark')
    plt.rc('font', size=13)
    #plt.rc('xtick', labelsize=14)
    colors= {'Correction': "gold", 'Challenge': "goldenrod", 'Direct_NegEval': "cornflowerblue", 'Indirect_NegEval': "lightsteelblue", 'No_Conflict': "crimson"}

    #ax = counts_new_perc.plot.bar()
    ax = counts_new_perc.plot.bar(width = 0.7, color=colors)
    plt.yticks(np.arange(0, 19, 2.5))
    plt.axvline([0.5], color= "black", linestyle="dashed")
    plt.axvline([6.5], color= "black", linestyle="dashed")
    #plt.axvline([9.5], color= "black", linestyle="dashed")
    #plt.axvline([18.5], color= "black", linestyle="dashed")
    #plt.axvline([21.5], color= "black", linestyle="dashed")


    ax.set_axisbelow(True)
    ax.grid()
    ax.get_legend().remove()
    plt.xlabel("RST Label in Paragraph")
    plt.ylabel("Proportion (%) within Conflict Type")
    #plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=12)
    plt.show()


def main():
    csvf = "../data/main_conflicts_aligned.csv"
    df = pd.read_csv("../data/output/main_conflicts_aligned_pargraphid.csv", index_col=0)
    #count_labels_flat_all_conflicttypes(df)
    #count_labels_flat_grouped(df)#todo
    #count_labels_flat_binary(df)
    #count_labels_paragraph_ConflictType(df)
    count_labels_paragraph_all_conflicttypes(df)


if __name__ == "__main__":
    main()