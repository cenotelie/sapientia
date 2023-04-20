#parse_data.py
import json
import random

import typer
from pathlib import Path

from spacy.tokens import Span, DocBin, Doc
from spacy.vocab import Vocab
from wasabi import Printer

msg = Printer()

SYMM_LABELS = ["COLLABORATION", "CONNECTION"]
MAP_LABELS = {
    "COLLABORATION": "Collaborates",
    "PROVIDE": "Provides", 
    "DEFINED_BY": "Defined by",
    "COMPLY_WITH": "Complies with", 
    "COMPOSED_BY": "Composed by", 
    "HAS_FEATURE": "Has feature", 
    "HAS_VALUE": "Has value", 
    "PERFORM": "Performs", 
    "SUBJECT": "Subject", 
    "COMMUNICATE": "Communicates", 
    "IN_CONDITION": "In condition", 
    "CONTROL": "Controls",
    "CONNECTION": "Connects",
}


def main(json_loc: Path, train_file: Path, dev_file: Path, test_file: Path):
    """Creating the corpus from the Prodigy annotations."""
    random.seed(0)
    Doc.set_extension("rel", default={})
    vocab = Vocab()

    docs = {"train": [], "dev": [], "test": []}
    ids = {"train": set(), "dev": set(), "test": set()}
    count_all = {"train": 0, "dev": 0, "test": 0}
    count_pos = {"train": 0, "dev": 0, "test": 0}

    with json_loc.open("r", encoding="utf8") as jsonfile:
        for line in jsonfile:
            example = json.loads(line)
            span_starts = set()
            if example["answer"] == "accept":
                neg = 0
                pos = 0
                # Parse the tokens
                words = [t["text"] for t in example["tokens"]]
                spaces = [t["ws"] for t in example["tokens"]]
                doc = Doc(vocab, words=words, spaces=spaces)

                # Parse the GGP entities
                spans = example["spans"]
                entities = []
                span_end_to_start = {}
                for span in spans:
                    entity = doc.char_span(
                        span["start"], span["end"], label=span["label"]
                    )
                    span_end_to_start[span["token_end"]] = span["token_start"]
                    entities.append(entity)
                    span_starts.add(span["token_start"])
                doc.ents = entities

                # Parse the relations
                rels = {}
                for x1 in span_starts:
                    for x2 in span_starts:
                        rels[(x1, x2)] = {}
                relations = example["relations"]
                for relation in relations:
                    # the 'head' and 'child' annotations refer to the end token in the span
                    # but we want the first token
                    start = span_end_to_start[relation["head"]]
                    end = span_end_to_start[relation["child"]]
                    label = relation["label"]
                    label = MAP_LABELS[label]
                    if label not in rels[(start, end)]:
                        rels[(start, end)][label] = 1.0
                        pos += 1
                    if label in SYMM_LABELS:
                        if label not in rels[(end, start)]:
                            rels[(end, start)][label] = 1.0
                            pos += 1

                # The annotation is complete, so fill in zero's where the data is missing
                for x1 in span_starts:
                    for x2 in span_starts:
                        for label in MAP_LABELS.values():
                            if label not in rels[(x1, x2)]:
                                neg += 1
                                rels[(x1, x2)][label] = 0.0
                doc._.rel = rels

                # only keeping documents with at least 1 positive case
                if pos > 0:
                    if random.random() < 0.2:
                        docs["test"].append(doc)
                        count_pos["test"] += pos
                        count_all["test"] += pos + neg
                    elif random.random() < 0.5:
                        docs["dev"].append(doc)
                        count_pos["dev"] += pos
                        count_all["dev"] += pos + neg
                    else:
                        docs["train"].append(doc)
                        count_pos["train"] += pos
                        count_all["train"] += pos + neg

    docbin = DocBin(docs=docs["train"], store_user_data=True)
    docbin.to_disk(train_file)
    msg.info(
        f"{len(docs['train'])} training sentences from {len(ids['train'])} articles, "
        f"{count_pos['train']}/{count_all['train']} pos instances."
    )

    docbin = DocBin(docs=docs["dev"], store_user_data=True)
    docbin.to_disk(dev_file)
    msg.info(
        f"{len(docs['dev'])} dev sentences from {len(ids['dev'])} articles, "
        f"{count_pos['dev']}/{count_all['dev']} pos instances."
    )

    docbin = DocBin(docs=docs["test"], store_user_data=True)
    docbin.to_disk(test_file)
    msg.info(
        f"{len(docs['test'])} test sentences from {len(ids['test'])} articles, "
        f"{count_pos['test']}/{count_all['test']} pos instances."
    )


if __name__ == "__main__":
    typer.run(main)

