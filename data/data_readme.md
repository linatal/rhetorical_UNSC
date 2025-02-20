# Description of Dataset Files
### [data/07_rst](07_rst)  
RST annotations folder containing rst-xml files. The files were extracted from the annotation tool we used, which is *RSTWeb*.
Input dir for [code/01_align_rst_conflict.py](..%2Fcode%2F01_align_rst_conflict.py) 

### [data/main_conflicts.csv](main_conflicts.csv)
Conflict annotations as csv table copied from [UNSCon](https://github.com/linatal/UNSCon/tree/main) project. The speeches are preprocessed and EDU-segmented. 
Input file for [code/01_align_rst_conflict.py](..%2Fcode%2F01_align_rst_conflict.py) 

Columns:
* **filename**: txt filename annotated with Conflicts
* **fileid**: Basename of file (without .txt) as given in the original UN Security Debates Corpus.
* **char_start_offset_edu** and **char_end_offset_edu**: Character offset start and end of EDU
* **speech_sentence_id**: Counter ID for sentence inside the speech
* **speech_edu_id**: Counter ID for EDU inside the speech
* **text_edu**: EDU string from speech
* **Conflict_Type**: Conflict labels: *Indirect_Negeval*, *Direct_NegEval*, *Challenge* or *Correction*
* **Conflict_Target**: Council Target Types (*Speaker or Speech*, *Country*, *Group of Countries*, *UNSC*, 
*Self-targeting*, *Underspecified*)
* **Conflict_Target_Intermediate**: Intermediate Target Types (*Policy or Law*, *Person*, *UN-Organization*, *NGO*, *Other*)
* **Target_Country_Name**: Name of Target Country
* **paragraph_id**: Counter ID for paragraph, consecutive but with gaps [0,2,4,6....] since double-linebreaks were originally also counted as paragraphs

### [data/main_conflicts_aligned.csv](main_conflicts_aligned.csv)
Csv table created in ``code/02_dataframe_preparation.py``. The table includes merged Conflict annotations: [data/main_conflicts.csv](main_conflicts.csv) and RST annotations: [data/07_rst](07_rst) 

RST annotations were extracted in [code/01_align_rst_conflict.py](..%2Fcode%2F01_align_rst_conflict.py) in reversed depth-first method: starting from leaf node, going up to the root node. 
Each RST chain per EDU is saved as list.

Same columns as in [data/main_conflicts.csv](main_conflicts.csv), additionally: 
* **rstree_nodeid**: ID of leaf node in EDU chain
* **rstree_nodeid_chain**: A list of node IDs extracted from rs3 files. The node IDs lists are organized starting from the leaf nodes and going up to the root node.
* **rstree_relation_chain:**: A list of relations extracted from rs3 files. The relations lists are organized starting from the leaf nodes and going up to the root node.
* **rstree_relation_leaf:** The leaf node relation for the EDU. For example, if the relation is 'Circumstance', the EDU is annotated as describing the circumstances related to the content of the EDU to which the relation points.
* **rstree_edges**: Number of edges starting from the leaf node, going up to the root node.
* **sat_value_rstree**: Number of Satelites starting from the leaf node, going up to the root node.

### [data/output/main_conflicts_prepared.csv](output%2Fmain_conflicts_prepared.csv)
Csv table created in [code/02_compute_nuclearity.py](..%2Fcode%2F02_compute_nuclearity.py), modified version of [main_conflicts_aligned.csv](main_conflicts_aligned.csv) including corrected paragraph-IDs.

The table has the same columns as [data/main_conflicts.csv](main_conflicts.csv), additional ones:  
* **'paragraph_id_consecutive'**: consecutive paragraph id inclreasing in +1 steps for full dataset, starting at 0
* **'paragraph_id_consecutive_per_file'**: adds consecutive paragraph id inclreasing in +1 steps per file, starting at 0

### [main_conflicts_aligned_paragraphid.csv](output%2Fmain_conflicts_aligned_paragraphid.csv)
Csv table created in [code/02_compute_nuclearity.py](..%2Fcode%2F02_compute_nuclearity.py)

Same columns as [data/output/main_conflicts_prepared.csv](output%2Fmain_conflicts_prepared.csv) but with paragraph subtree rst relation chains (startin from leaf node going up to the root of the paragraph):
* **rstree_nodeid_chain_subtree**, **rstree_relation_chain_subtree**, **rstree_edges_subtree**, **sat_value_subtree**