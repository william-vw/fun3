# Performance Experiments: Zika use case

## Setup
We implemented the [CDC testing guidelines](https://www.cdc.gov/zika/hc-providers/testing-guidance.html) using N3 rules. 
These rules determine whether a patient should be tested for Zika, based on factors such as pregnancy, symptoms, recent travel to Zika areas, or sexual contacts. 
We evaluated rules of different complexity:

### Data
We represent patient data using the [HL7 FHIR](https://www.hl7.org/index.cfm) vocabulary, an EHR interoperability standard that offers an RDF representation (Turtle syntax).
We use a simplified version of the FHIR vocabulary, which relies less on deeply structured data. 
We provide example snippets of the [original](snippets/orig/) and [reduced](snippets/red/) HL7 FHIR vocabularies, 
which clearly illustrate the differences between them.

 We randomly generated datasets of (a) patients of increasing sizes (100, 200, 500, 700, 1000, 2000, 5000 patients), and (b) cases matching rule conditions:
 - _Dataset 1\%_: patients have a 1\% chance of meeting a condition for Zika testing.
 - _Dataset 2\%_: patients have a 2\% chance of meeting a condition for Zika testing.
 
We show the detailed sizes of the datasets below (in number of triples):

| \# patients | dataset 1\% | dataset 2\% |
|---|---|---|
| 100         | 875         | 1749       |
| 200         | 1882        | 3312       |
| 500         | 4603        | 7734       |
| 700         | 6353        | 11873      |
| 1000        | 9435        | 16878      |
| 2000        | 18252        | 34945      |
| 5000        | 44916        | 83582      |

The datasets can be found in the [`data/`](data/) folder. For instance, [`gen500_pt1`](data/gen500_pt1.n3) represents a dataset with 200 patients who have a 1\% chance of matching the rule conditions (`pt1`).

### Rules

- _Ruleset 1_ ([`rules_red0.n3`](rules_red0.n3)): rules only check a single condition for Zika testing, namely whether the person is pregnant. Pregnancy is checked by a separate rule that finds active and confirmed conditions with the clinical code for pregnancy. Utility rules allow for easier navigation of the HL7 FHIR vocabulary.
  In total, there are 5 rules in this ruleset.

- _Ruleset 2_ ([`rules_red1.n3`](rules_red1.n3)): rules check three conditions for Zika testing, namely pregnancy, whether the person has a Zika symptom, and whether they had a possible Zika exposure, due to travel to a Zika area or sexual encounters with a possibly exposed person. In total, there are 16 rules in this ruleset.


## Run

Checkout the [`exp.ipynb`](exp.ipynb) notebook to run the experiments. 