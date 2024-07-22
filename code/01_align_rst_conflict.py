''' Creates table with RST annotations and flat RST labels "main_conflicts_sm_aligned.csv".
Input: folder with rst files /data/07_rst, conflicts table ../data/main_conflicts.csv
Output: aligned conflicts-rst table'''
import lxml.etree
from configparser import ConfigParser
from pathlib import Path
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_lg')
xmlp = lxml.etree.XMLParser(strip_cdata=False, resolve_entities=False, encoding='utf-8', remove_comments=True)


def get_root_path(node, tree, path):
    if 'parent' in node.attrib:
        parent_id = node.get('parent')
        parent_node = [x for x in tree.getroot().find('.//body') if x.get('id') == parent_id]

        assert len(parent_node) == 1
        path.append(parent_node[0])
        get_root_path(parent_node[0], tree, path)

    return path


def align(csvf, rst_dir):
    df = pd.read_csv(csvf, index_col=0)
    df = df.sort_values(["filename", "speech_edu_id"])
    path = Path(rst_dir)
    listi = [i for i in path.glob('**/*.rs3')]
    listi.sort()
    big_list_id = []
    big_list_relation = []
    big_list_id_chain = []
    big_list_relation_chain = []

    # get files that are not annotated with rst but conflicts, and filter those from df, create "_selected" corpus
    list_fileids_confl = df["fileid"].drop_duplicates().to_list()
    list_fileids_rst = [i.name[:26] for i in path.glob('**/*.rs3')]
    temp = [x for x in list_fileids_confl if x not in list_fileids_rst]
    df_f = df[~df['fileid'].isin(temp)]

    for rstf in listi:
        list_rootpath = []
        name = rstf.name[:26]
        # get rows in df for file
        df_file = df_f[df_f.fileid == name]

        rstree = lxml.etree.parse(str(rstf), parser=xmlp)
        debug_list = []
        debug_list1 = []
        debug_list2 = []
        debug_list3 = []
        count_rst_segements = len(rstree.getroot().findall('.//segment'))

        #debug
        if df_file.shape[0] != count_rst_segements:
            print(name, "conflict edus:", df_file[0], "rst edus:", count_rst_segements )
        assert df_file.shape[0] == count_rst_segements
        #print(df_file.shape[0])
        #print(count_rst_segements)

        for segment in rstree.getroot().findall('.//segment'):

            rootpath = get_root_path(segment, rstree, [segment])

            id_chain = [x.get('id') for x in rootpath]
            id_rel = id_chain[0]
            relation_chain = [x.get('relname') for x in rootpath]
            relation = relation_chain[0]
            assert len(id_chain) == len(relation_chain)

            big_list_id_chain.append(id_chain)
            big_list_id.append(id_rel)
            big_list_relation_chain.append(relation_chain)
            big_list_relation.append(relation)

            debug_list.append(id_chain)
            debug_list1.append(id_rel)
            debug_list2.append(relation_chain)
            debug_list3.append(relation)
        #if len(debug_list3) != df_file.shape[0]:
        #    print("Error: ", len(debug_list3), df_file.shape[0], name)

    # df_files = df[(df.fileid == 'UNSC_2014_SPV.7138_spch002') | (df.fileid == 'UNSC_2014_SPV.7138_spch004') | (df.fileid == 'UNSC_2014_SPV.7138_spch005')]
    assert len(big_list_id) == len(big_list_id_chain) == len(big_list_relation_chain)

    df_f['rstree_nodeid'] = big_list_id
    df_f['rstree_nodeid_chain'] = big_list_id_chain
    df_f['rstree_relation_leave'] = big_list_relation
    df_f['rstree_relation_chain'] = big_list_relation_chain
    df_f = df_f.reset_index(drop=True)

    df_f['paragraph_id'] = df_f['paragraph_id'].astype("Int64")
    df_f['speech_sentence_id'] = df_f['speech_sentence_id'].astype("Int64")
    return df_f

def get_tokens(df_aligned):
    # tokenize edus
    list_edutexts = df_aligned['text_edu'].tolist()
    big_tokenized_list = []
    big_len_tok_list = []
    for text in list_edutexts:
        processed_text = nlp(text)
        tokenized_list = [i.text for i in processed_text]
        len_tok_list = len(tokenized_list)
        big_tokenized_list.append(tokenized_list)
        big_len_tok_list.append(len_tok_list)
    df_aligned['tokenized_edus'] = big_tokenized_list
    df_aligned['len_tokens_edus'] = big_len_tok_list
    return df_aligned

def main():
    config = ConfigParser()
    config.read("config.ini") # adjust path
    rst_dir = '../data/07_rst_selected' # adjust path
    csvf = '../data/main_conflicts.csv'
    output_file = "../data/main_conflicts_aligned.csv"
    df_aligned = align(csvf, rst_dir)
    df = get_tokens(df_aligned)
    df.to_csv(output_file)


if __name__ == '__main__':
    main()
