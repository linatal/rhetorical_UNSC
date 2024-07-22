import pandas as pd
from collections import Counter
import ast
import numpy as np
import itertools



def prepare_dataframe(table_conflict_rst_aligned):
    # input: dataframe output from 01_align_rst_conflict.py
    # create a conflict column, correct values in paragraph and sentence id, keep only columns needed, sort dataframe,
    # return prepared dataframe
    df = pd.read_csv(table_conflict_rst_aligned, index_col=0)
    df['A0_Negative_Evaluation'] = df['A0_Negative_Evaluation'].replace("_", "")
    df['B1_ChallengeType'] = df['B1_ChallengeType'].replace("_", "")
    df["Conflict_Type"] = df['A0_Negative_Evaluation'] + df['B1_ChallengeType']
    df["Conflict_Type"] = df["Conflict_Type"].replace("Direct_NegEvalChallenge", "Challenge")
    df["Conflict_Type"] = df["Conflict_Type"].replace("Indirect_NegEvalChallenge", "Challenge")
    df["Conflict_Type"] = df["Conflict_Type"].replace("", "_")
    df['paragraph_id'] = df['paragraph_id'].astype("Int64")
    df['speech_sentence_id'] = df['speech_sentence_id'].astype("Int64")
    # slice dataframe, keep only columns needed
    df_sent_sm = df[['filename', 'fileid', 'text_edu', 'Conflict_Type', 'tokenized_edus', 'len_tokens_edus', 'speech_edu_id', 'speech_sentence_id', 'paragraph_id',
     'rstree_nodeid_chain', 'rstree_relation_leave', 'rstree_relation_chain']]
    df_sent_sm = df_sent_sm.sort_values(['filename', 'speech_sentence_id'], ascending=[True, True])
    #df_sent_sm.to_csv(output_table_conflict_sents_small)
    return df_sent_sm


def to_consecutive(df_notcon):
    paragraph_id_list = df_notcon['paragraph_id'].tolist()
    id_counter = -1
    new_paragraph_id_list = []
    for index, element in enumerate(paragraph_id_list):
        #new_paragraph_id_list.append(id_counter)
        # TODO muss gecheckt werden
        # TypeError: boolean value of NA is ambiguous
        # for speeches with only one paragraph
        # Problem gelöst, unklar weshalb manche rows keine paragraoh id haben im original

        if not isinstance(paragraph_id_list[index], (int, np.integer)):
            new_paragraph_id_list.append(id_counter+1)
        elif not isinstance(paragraph_id_list[index-1], (int, np.integer)):
            new_paragraph_id_list.append(id_counter+1)
        elif paragraph_id_list[index-1] == paragraph_id_list[index]:
            new_paragraph_id_list.append(id_counter)
        elif paragraph_id_list[index-1] != paragraph_id_list[index]:
            id_counter += 1
            new_paragraph_id_list.append(id_counter)

    #df_notcon['paragraph_id_consecutive'] = new_paragraph_id_list

    return new_paragraph_id_list


def find_common_path(listi):
    if len(listi) == 1:
        return listi[0]
    global_common = [0] * max([len(x) for x in listi])
    for li in listi:
        reverse_li = li[::-1]
        for lj in listi:
            reverse_lj = lj[::-1]
            assert reverse_li[0] == reverse_lj[0]
            local_common = []
            shortest_list = min(len(reverse_li), len(reverse_lj))
            for i in range(shortest_list):
                if reverse_li[i] == reverse_lj[i]:
                    local_common.append(reverse_li[i])
                else:
                    break
            if len(local_common) < len(global_common):
                global_common = local_common
    #if [0] * len(global_common) == global_common:
    #    print("Only one edu in paragraph, no subtree.")
    return global_common[::-1]


def get_truncated_paths(listi, p):
    truncated_paths = []
    for li in listi:
        assert li[len(li) - len(p):] == p
        truncated_path = li[:len(li) - len(p) + 1]
        truncated_paths.append(truncated_path)
    return truncated_paths


def flatten_comprehension(matrix):
    return [item for row in matrix for item in row]


def get_subtrees_per_paragraph(df):
    # input: prepared dataframe
    # update paragraph_ids, take nodeid_chain and relation_chain and shorten them to subtrees (per paragraph)
    # get sat value for speech and paragraph trees, will be used for NM
    # output: dataframe with subtrees and sat values
    paragraph_consec_list = []
    list_nodeid_subtree = []
    list_rstree_rel = []
    list_rstree_li = []
    list_paragraph_index_chain_big = []

    list_sat_value = []
    list_sat_value_subtree = []

    nucl_labels = ['span', None, 'sameunit', 'list', 'joint', 'coordination', 'contrast', 'sequence', 'textual-organization'] # 'None' is the root node

    # include columns for paragraph id
    new_paragraph_id_list = to_consecutive(df)
    df['paragraph_id_consecutive'] = new_paragraph_id_list
    filenames = df['filename'].drop_duplicates().tolist()
    new_paragraph_id_list_per_file = []
    for filename in filenames:
        df_fn = df[df['filename'] == filename]
        list_consecutive_fn = to_consecutive(df_fn)
        new_paragraph_id_list_per_file.append(list_consecutive_fn)
    new_paragraph_id_list_per_file = flatten_comprehension(new_paragraph_id_list_per_file)
    assert len(new_paragraph_id_list_per_file) == len(new_paragraph_id_list)
    df['paragraph_id_consecutive_per_file'] = new_paragraph_id_list_per_file


    # iterate over apragraphs and compute over list of relations
    paragraph_idxs = df['paragraph_id_consecutive'].drop_duplicates().tolist()
    for paragraph_index in paragraph_idxs:
        df_p = df[df['paragraph_id_consecutive'] == paragraph_index]
        list_paragraph_index_chain = []

        for index, row in df_p.iterrows():
            # get df['rstree_nodeid_chain'] row from str to lists
            y_str = row['rstree_nodeid_chain']
            y = ast.literal_eval(y_str)
            list_paragraph_index_chain.append(y)

            # get df['rstree_relation_chain'] row from str to lists
            z_str = row['rstree_relation_chain']
            z = ast.literal_eval(z_str)
            list_rstree_rel.append(z)
            sum_edges = len(z)
            list_rstree_li.append(sum_edges)  # get sum of edges from leave to root
            # get sat value which are all satelite relation from leave to root
            assert len(y) == sum_edges

            counter = Counter(z)
            sum_rstree_nucl_value = counter[None] + counter['span'] + counter['sameunit'] + counter['list'] + counter[
                'joint'] + counter['contrast'] + counter['sequence'] + counter['textual-organization']
            assert sum_edges == sum(counter.values())

            sat_value = sum_edges - sum_rstree_nucl_value
            list_sat_value.append(sat_value)

        list_paragraph_index_chain_big.append(list_paragraph_index_chain)

        assert len(list_rstree_li) == len(list_sat_value)

        common_path = find_common_path(list_paragraph_index_chain)
        para_lst = get_truncated_paths(list_paragraph_index_chain, common_path)
        assert df_p.shape[0] == len(para_lst)
        list_nodeid_subtree.append(para_lst)

    list_paragraph_index_chain_big = flatten_comprehension(list_paragraph_index_chain_big)
    list_nodeid_subtree = flatten_comprehension(list_nodeid_subtree)
    assert len(list_nodeid_subtree) == len(list_rstree_rel) == len(list_rstree_li) == len(list_paragraph_index_chain_big)

    # get len list for each list in list_nodeid_subtree,
    list_subtree_li = [len(x) for x in list_nodeid_subtree]
    # slice df['rstree_relation_chain'] lists to len(para_lst)
    lst_para_rel_subtree = []
    for i, r in enumerate(list_subtree_li):
        sublist = list_rstree_rel[i][:r]
        counter2 = Counter(sublist)
        lst_para_rel_subtree.append(sublist)
        sum_subtree_nucl_value = counter2[None] + counter2['span'] + counter2['sameunit'] + counter2['list'] + counter2[
            'joint'] + counter2['contrast'] + counter2['sequence'] + counter2['textual-organization']
        sat_value_subtree = len(sublist) - sum_subtree_nucl_value
        list_sat_value_subtree.append(sat_value_subtree)

    assert len(lst_para_rel_subtree) == len(list_nodeid_subtree) == len(list_sat_value_subtree)

    df['rstree_edges'] = list_rstree_li
    df['sat_value_rstree'] = list_sat_value

    df['rstree_nodeid_chain_subtree'] = list_nodeid_subtree
    df['rstree_relation_chain_subtree'] = lst_para_rel_subtree
    df['rstree_edges_subtree'] = list_subtree_li

    df['sat_value_subtree'] = list_sat_value_subtree

    return df


def get_nuclearity_mass(df):
    # gets num of conflicts NM1 and NM2 values for full rstrees and for paragraph-wise subtrees
    # input: df from get_subtrees_per_paragraph(), output: df with file-wise rows, with NM1 and NM2 values
    num_conflicts_para = []
    num_indirect_para = []
    num_direct_para = []
    num_correction_para = []
    propotion_conflicts_para = []
    propotion_indirect_para = []
    propotion_direct_para = []
    propotion_correction_para = []

    num_cdus_para_lst = []
    num_edus_para_lst = []
    nm1_para = []
    nm2_para = []

    num_cdus_speech_lst = []
    num_edus_speech_lst = []
    nm1_speech = []
    nm2_speech = []

    num_conflicts_speech = []
    num_indirect_speech = []
    num_direct_speech = []
    num_correction_speech = []
    propotion_conflicts_speech = []
    propotion_indirect_speech = []
    propotion_direct_speech = []
    propotion_correction_speech = []

    # values per paragraph
    #length_path_to_root_lst = []
    para_idxs = df['paragraph_id_consecutive'].drop_duplicates().tolist()
    for p_idx in para_idxs:
        df_para = df[df['paragraph_id_consecutive'] == p_idx]
        num_edus_para = df_para.shape[0]

        num_conflicts_p = (
                (df_para['Conflict_Type'] == 'Indirect_NegEval') | (df_para['Conflict_Type'] == 'Direct_NegEval')
                | (df_para['Conflict_Type'] == 'Challenge') | (df_para['Conflict_Type'] == 'Correction')).sum()
        num_indirect_p = (df_para['Conflict_Type'] == 'Indirect_NegEval').sum()
        num_direct_p = (df_para['Conflict_Type'] == 'Direct_NegEval').sum()
        num_challenge_p = ((df_para['Conflict_Type'] == 'Challenge') | (df_para['Conflict_Type'] == 'Correction')).sum()

        num_conflicts_para.append(num_conflicts_p)
        num_indirect_para.append(num_indirect_p)
        num_direct_para.append(num_direct_p)
        num_correction_para.append(num_challenge_p)

        propotion_conflicts_p = num_conflicts_p / num_edus_para
        propotion_indirect_p = num_indirect_p / num_edus_para
        propotion_direct_p = num_direct_p / num_edus_para
        propotion_challenge_p = num_challenge_p / num_edus_para

        propotion_conflicts_para.append(propotion_conflicts_p)
        propotion_indirect_para.append(propotion_indirect_p)
        propotion_direct_para.append(propotion_direct_p)
        propotion_correction_para.append(propotion_challenge_p)

        # 2. get NM1 per paragraph (proportion of leaf nodes with a sat value of 0 or 1 (i.e., ‘central’ units))
        num_cdu_para = ((df_para['sat_value_rstree'] == 0) | (df_para['sat_value_rstree'] == 1)).sum()
        prop_cdu_para = num_cdu_para / num_edus_para

        # lists to append as new row to df
        num_cdus_para_lst.append(num_cdu_para)
        num_edus_para_lst.append(num_edus_para)
        nm1_para.append(prop_cdu_para) # NM1

        # NM2 is the sum of those li where i has a sat value of 0 or 1, divided by the sum of li for all i of the tree.
        sum_li_para = df_para['rstree_edges_subtree'].sum()
        nm2 = num_cdu_para / sum_li_para
        nm2_para.append(nm2)

    # values per files/rstree
    filenames = df['filename'].drop_duplicates().tolist()
    for filename in filenames:
        df_fn = df[df['filename'] == filename]
        num_edus_spch = df_fn.shape[0]

        # 1. number of Conflicts per rstree
        num_conflicts_spch = ((df_fn['Conflict_Type'] == 'Indirect_NegEval') | (df_fn['Conflict_Type'] == 'Direct_NegEval')
                         | (df_fn['Conflict_Type'] == 'Challenge') | (df_fn['Conflict_Type'] == 'Correction')).sum()
        num_indirect_spch = (df_fn['Conflict_Type'] == 'Indirect_NegEval').sum()
        num_direct_spch = (df_fn['Conflict_Type'] == 'Direct_NegEval').sum()
        num_challenge_spch = ((df_fn['Conflict_Type'] == 'Challenge') | (df_fn['Conflict_Type'] == 'Correction')).sum()

        propotion_conflicts_spch = num_conflicts_spch / num_edus_spch
        propotion_indirect_spch = num_indirect_spch / num_edus_spch
        propotion_direct_spch = num_direct_spch / num_edus_spch
        propotion_challenge_spch = num_challenge_spch / num_edus_spch

        num_conflicts_speech.append(num_conflicts_spch)
        num_indirect_speech.append(num_indirect_spch)
        num_direct_speech.append(num_direct_spch)
        num_correction_speech.append(num_challenge_spch)

        propotion_conflicts_speech.append(propotion_conflicts_spch)
        propotion_indirect_speech.append(propotion_indirect_spch)
        propotion_direct_speech.append(propotion_direct_spch)
        propotion_correction_speech.append(propotion_challenge_spch)

        # 2. get NM1 per speech (proportion of leaf nodes with a sat value of 0 or 1 (i.e., ‘central’ units))
        num_cdu_spch = ((df_fn['sat_value_rstree'] == 0) | (df_fn['sat_value_rstree'] == 1)).sum()
        prop_cdu_spch = num_cdu_spch / num_edus_spch

        # lists to append as new row to df
        num_cdus_speech_lst.append(num_cdu_spch)
        num_edus_speech_lst.append(num_edus_spch)
        nm1_speech.append(prop_cdu_spch) # NM1

        # NM2 is the sum of those li where i has a sat value of 0 or 1, divided by the sum of li for all i of the tree.
        sum_li_speech = df_fn['rstree_edges'].sum()
        nm2 = num_cdu_spch / sum_li_speech
        nm2_speech.append(nm2)

    # compressed dataframe one paragraph per row
    df_parawise = df[['filename', 'paragraph_id_consecutive', 'paragraph_id_consecutive_per_file']].drop_duplicates()

    df_parawise['num_conflict_para'] = num_conflicts_para
    df_parawise['num_Iconflict_para'] = num_indirect_para
    df_parawise['num_Dconflict_para'] = num_direct_para
    df_parawise['num_Cconflict_para'] = num_correction_para
    # propotion of edus marked as conflicts versus num edus
    df_parawise['propotion_conflict_para'] = propotion_conflicts_para
    df_parawise['propotion_Iconflict_para'] = propotion_indirect_para
    df_parawise['propotion_Dconflict_para'] = propotion_direct_para
    df_parawise['propotion_Cconflict_para'] = propotion_correction_para

    df_parawise['num_cdus_para'] = num_cdus_para_lst
    df_parawise['num_edus_para'] = num_edus_para_lst
    df_parawise['NM1_para'] = nm1_para
    df_parawise['NM2_para'] = nm2_para

    # compressed dataframe one speech per row
    # set filenames, per filename, export new dataframe 1row==1file
    df_filewise = df['filename'].drop_duplicates()
    df_filewise = df_filewise.to_frame() # Series to Dataframe to enable appending columns

    df_filewise['num_conflict_speech'] = num_conflicts_speech
    df_filewise['num_Iconflict_speech'] = num_indirect_speech
    df_filewise['num_Dconflict_speech'] = num_direct_speech
    df_filewise['num_Cconflict_speech'] = num_correction_speech
    df_filewise['propotion_conflict_speech'] = propotion_conflicts_speech
    df_filewise['propotion_Iconflict_speech'] = propotion_indirect_speech
    df_filewise['propotion_Dconflict_speech'] = propotion_direct_speech
    df_filewise['propotion_Cconflict_speech'] = propotion_correction_speech

    df_filewise['num_cdus_speech'] = num_cdus_speech_lst
    df_filewise['num_edus_speech'] = num_edus_speech_lst
    df_filewise['NM1_speech'] = nm1_speech
    df_filewise['NM2_speech'] = nm2_speech
    # TODO: check num cdus in table with trees in rstweb

    # Problem with NM1 value is that the bigger a tree the smaller the value (per tree usually one or - with multilabel related CDUs - two CDUs per document)
    # We have a great variety of tree lengths (from 7 up to 194 edus) (looking at df_filewise['num_edus_speech']) --> see def standard_deviation(), measures variability in a distribution
    print("standard deviation of EDU length and number of CDUs per speech:\n", df_filewise[['num_edus_speech', 'num_cdus_speech']].std()) # num_edus_speech 42.670252, num_cdus_speech 6.973009
    print("standard deviation of EDU length and number of CDUs per paragraphs:\n", df_parawise[['num_edus_para', 'num_cdus_para']].std()) # num_edus_speech 42.670252, num_cdus_speech 6.973009
    # -> Looking at paragraphs might be more usefull, also since we want to compare it with conflict annotations

    return df_filewise, df_parawise

def main():
    csvf = "../data/main_conflicts_aligned.csv"
    df = prepare_dataframe(csvf)

    df_sub = get_subtrees_per_paragraph(df)
    df_sub.to_csv("../data/output/main_conflicts_aligned_pargraphid.csv")
    evaluation_table_speech, evaluation_table_para = get_nuclearity_mass(df_sub)
    evaluation_table_speech.to_csv("../data/output/nuclearity_mass_speech.csv")
    evaluation_table_para.to_csv("../data/output/nuclearity_mass_para.csv")


if __name__ == "__main__":
    main()
