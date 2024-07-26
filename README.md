# RST-UNSC: Rhetorical Strategies in the UN Security Council

Dataset, Amendment for RST annotation guidelines and code for analysis experiments for the paper "How Diplomats Dispute: The UN Security Council Conflict Corpus" by Karolina Zaczynska, and Manfred Stede. To appear in Proceedings of the 25th Meeting of the Special Interest Group on Discourse and Dialogue (SIGDIAL 2024). Kyoto, Japan, 2024.

## Dataset

`\data` folder contains: 
* `\output` directory with computed Nuclearity Mass values per speech (`nuclearity_mass_speech.csv`) or paragraph (`nuclearity_mass_para.csv`) and per paragraph with paragraph-based RST-subtree values (`main_conflicts_aligned_paragraohid.csv`).
* `07_rst` with original RST annotations output from RSTweb tool in rs3-format
* `main_conflicts.csv` UNSC speechs with Conflicts annotations per EDU (taken from UNSCon: https://github.com/linatal/UNSCon)
* `main_conflicts_aligned.csv` UNSC speechs with Conflicts annotations with RST annotations per EDU aligned