# UNSC-RST: Rhetorical Strategies in the UN Security Council

Dataset, Amendment for RST annotation guidelines and code for experiments as described in the paper "[Rhetorical Strategies 
in the UN Security Council: Rhetorical Structure Theory and Conflicts](https://aclanthology.org/2024.sigdial-1.2/)" (Karolina Zaczynska, and Manfred Stede, Proceedings of the 25th Meeting of the Special Interest Group on Discourse and Dialogue (SIGDIAL 2024). Kyoto, Japan, 2024).

This git-repository includes a new dataset with RST annotations of 82 diplomatic speeches given in the UN Security Council (UNSC-RST). 
For the RST annotations we use a modified version of the [guidelines](https://www.sfu.ca/~mtaboada/docs/research/RST_Annotation_Guidelines.pdf) by Stede et al. 2014.
For the analysis of rhetorical strategies used by diplomats to express (verbal) Conflicts, we aligned the RST and existing Conflict annotations (see also our previous [paper](https://github.com/linatal/UNSCon/tree/main?tab=readme-ov-file) on Conflicts).
We look at both the RST-relation distribution and the RST tree structure in combination with Conflicts in the speeches. 
In preliminary analyses we already see patterns that are characteristic for particular topics and countries. 

## Dataset

`\data` folder contains: 
* `\output` directory with computed Nuclearity Mass values per speech (`nuclearity_mass_speech.csv`) or paragraph (`nuclearity_mass_para.csv`) and per paragraph with paragraph-based RST-subtree values (`main_conflicts_aligned_paragraohid.csv`).
* `07_rst` RST annotations (retrieved from RSTweb tool) in rs3-format
* `main_conflicts.csv` UNSC speechs with Conflicts annotations per EDU (taken from https://github.com/linatal/UNSCon)
* `main_conflicts_aligned.csv` UNSC speechs with Conflicts annotations with RST annotations per EDU aligned