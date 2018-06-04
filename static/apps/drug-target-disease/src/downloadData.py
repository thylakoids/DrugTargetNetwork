import sys

def downloadSTRINGdata():
    # download the STRING actions database
    os.system('wget https://stringdb-static.org/download/protein.actions.v10.5/9606.protein.actions.v10.5.txt.gz -O ../data/9606.protein.actions.v10.5.txt.gz')
    '''
    # keep only activation and inhibition lines
    # contiton 
    column 4 :'action' (inhibition|activation)
    column 5 :'is_directional' t
    column 6 :'a_is_acting' t
    column 7 :'score' >800
    '''
    os.system(
        "zcat ../data/9606.protein.actions.v10.5.txt.gz| awk '{if ($4~/(inhibition|activation)/ && $5 ~/t/ && $6~/t/ && $7>800 || NR==1 ) print $1,$2,$4,$5,$6,$7}' > ../out/ppi_actions_ensp.txt"
        )

    # download the STRING links.full database
    os.system('wget https://stringdb-static.org/download/protein.links.full.v10.5/9606.protein.links.full.v10.5.txt.gz -O ../data/9606.protein.links.full.v10.5.txt.gz')

    os.system(
        "zcat ../data/9606.protein.links.full.v10.5.txt.gz|awk '{gsub(/9606\./,"");if ($16>800 || NR==1) print $1,$2,$16}'>../out/ppi_ensp.txt"
        )
    os.system(
        "wget https://string-db.org/mapping_files/uniprot_mappings/9606_reviewed_uniprot_2_string.04_2015.tsv.gz -O ../data/9606_reviewed_uniprot_2_string.04_2015.tsv.gz"
        )