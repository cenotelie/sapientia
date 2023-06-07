#!/bin/bash
python3 -m prodigy train ../ner_models/collins_en/ --ner collins_en --eval-split 0.1 --base-model en_core_web_sm --label-stats