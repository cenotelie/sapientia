from spacy.cli.project.run import project_run
from spacy.cli.project.assets import project_assets
from pathlib import Path
import spacy
from scripts.rel_pipe import make_relation_extractor
import scripts.rel_model


def test_rel_project():
    root = Path(__file__).parent
    project_assets(root)
    project_run(root, "all", capture=True)

def test_load_model():
    #model = "en_core_web_sm"
    model = "training/model-best"
    text = "Apple is looking at buying U.K. startup for $1 billion."
    nlp = spacy.load(model)
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
    for rel in doc._.rel :
        print(rel)

if __name__ == '__main__':
    test_load_model()
