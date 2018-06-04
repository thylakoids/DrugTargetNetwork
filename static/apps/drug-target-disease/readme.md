# Target-Disease Network
**therapeutic targets database**

From **DrugBank** we get the drug(cas-number)-target(Uniprot) relationship, now we need to map connect the target to disease.
<!-- MarkdownTOC -->

1. [Databases and tools](#databases-and-tools)
    1. [parse drugbank.xml, and save it to mysql](#parse-drugbankxml-and-save-it-to-mysql)
    1. [map targetmol ID to drugbank ID to target to disease](#map-targetmol-id-to-drugbank-id-to-target-to-disease)
    1. [ICD identifiers](#icd-identifiers)
    1. [Biology database id mapping](#biology-database-id-mapping)
    1. [Connectivity Map](#connectivity-map)
    1. [Library of Integrated Network-Based Cellular Signatures\(LINCS\) project](#library-of-integrated-network-based-cellular-signatureslincs-project)
    1. [Gene expression Omnibus\(GEO\)](#gene-expression-omnibusgeo)
    1. [STRING database](#string-database)
1. [potential drugs](#potential-drugs)
    1. [PPI network construction](#ppi-network-construction)
    1. [find hub nodes](#find-hub-nodes)
    1. [find potential drugs](#find-potential-drugs)
1. [potential drug combinations](#potential-drug-combinations)
    1. [PPI network construction](#ppi-network-construction-1)
    1. [Synergy score for each drug combination](#synergy-score-for-each-drug-combination)

<!-- /MarkdownTOC -->
## Databases and tools
### parse drugbank.xml, and save it to mysql
``` python
import pymysql
from xml.etree import cElementTree as ET
```
total drugs:11033

FDA:2557

### map targetmol ID to drugbank ID to target to disease
targetmol:1818

targetmo-drugbank:**1421**

unique targets:1563

uniprot-TTD:709

TTD-disease:2892

drug-target:[druginbank.csv](out/druginbank.csv)

target-disease:[target-disease.csv](out/target-disease.csv)

### [ICD identifiers](http://apps.who.int/classifications/icd10/browse/2016/en)
**International Statistical Classification of Diseases and Related Health Problems 10th Revision**

| Chapter | Blocks  | Title                                                                                               |
| --      | --      | --                                                                                                  |
| I       | A00–B99 | Certain infectious and parasitic diseases                                                           |
| II      | C00–D48 | Neoplasms                                                                                           |
| III     | D50–D89 | Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism |
| IV      | E00–E90 | Endocrine, nutritional and metabolic diseases                                                       |
| V       | F00–F99 | Mental and behavioural disorders                                                                    |
| VI      | G00–G99 | Diseases of the nervous system                                                                      |
| VII     | H00–H59 | Diseases of the eye and adnexa                                                                      |
| VIII    | H60–H95 | Diseases of the ear and mastoid process                                                             |
| IX      | I00–I99 | Diseases of the circulatory system                                                                  |
| X       | J00–J99 | Diseases of the respiratory system                                                                  |
| XI      | K00–K93 | Diseases of the digestive system                                                                    |
| XII     | L00–L99 | Diseases of the skin and subcutaneous tissue                                                        |
| XIII    | M00–M99 | Diseases of the musculoskeletal system and connective tissue                                        |
| XIV     | N00–N99 | Diseases of the genitourinary system                                                                |
| XV      | O00–O99 | Pregnancy, childbirth and the puerperium                                                            |
| XVI     | P00–P96 | Certain conditions originating in the perinatal period                                              |
| XVII    | Q00–Q99 | Congenital malformations, deformations and chromosomal abnormalities                                |
| XVIII   | R00–R99 | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified             |
| XIX     | S00–T98 | Injury, poisoning and certain other consequences of external causes                                 |
| XX      | V01–Y98 | External causes of morbidity and mortality                                                          |
| XXI     | Z00–Z99 | Factors influencing health status and contact with health services                                  |
| XXII    | U00–U99 | Codes for special purposes                                                                          |

disease: C34-C34.9, Malignant neoplasm of bronchus and lung

targets: 144

drugs: 584

### [Biology database id mapping](https://wolfsonliu.github.io/archive/chang-yong-sheng-wu-xin-xi-id-ji-zhuan-huan-fang-fa.html)
### [Connectivity Map](http://www.broadinstitute.org/cmap/)
It consists of 6100 drug signatures that stem from five different cell types treated with 1309 bioactive molecules of various concentrations and experiment duration(perturbagens).
### [Library of Integrated Network-Based Cellular Signatures(LINCS) project](http://www.lincsproject.org/)
**L1000CDS2**

input : differentially(up/down) expressed gene set

output : most related drugs, drug combinations
### Gene expression Omnibus(GEO)
It is a transcriptional data repository.

### [STRING database](http://version10.string-db.org/help/database/#table-networkactions)

* is_directional - describes if the diractionality of the particular interaction is known.
wget https://string-db.org/download/protein.actions.v10.5/9606.protein.actions.v10.5.txt.gz # 05/29/2017 # A subset of directional interactions
Total number of interactions: 1,862,289

Column 1: "item_id_a", e.g., 9606.ENSP00000000233
Column 2: "item_id_b", e.g., 9606.ENSP00000005257
Column 3: "mode"
107288 activation
326100 binding
506918 catalysis
23488 expression
23454 inhibition
29080 ptmod
845960 reaction
Column 4: "action"
107296 activation
35026 inhibition
Colum 5: "is_directional"
1260194 t
Column 6: "a_is_acting"
1232191 f
630097 t
Column 7: "score", from 150 to 900. Median 900.




## potential drugs
### PPI network construction 
Find lung cancer related target using TTD, and build PPI using STRING.

lung_cancer related uniprot:125

convert to string id:121

next : build a PPI network
nodes:125
edges:870
### find hub nodes
degree, betweenness and closeness(assign a importance value to each node )
### find potential drugs
hub target nodes related drugs(assign a importance value to each drug)

observation:
* multi-target drugs are often low-affinity binders

## potential drug combinations
### PPI network construction
Find lung cancer related target using TTD, and build PPI using STRING.
### Synergy score for each drug combination
topology score



