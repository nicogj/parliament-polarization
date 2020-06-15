# US Senate
python3 scripts/reduction.py us senate 116 --vote_freq_cutoff 0.25 --ind_freq_cutoff 0.75
python3 scripts/visualizations.py us senate 116

# France Assemblee
python3 scripts/reduction.py fr assemblee 15 --vote_freq_cutoff 0.25 --ind_freq_cutoff 0.2
python3 scripts/visualizations.py fr assemblee 15
