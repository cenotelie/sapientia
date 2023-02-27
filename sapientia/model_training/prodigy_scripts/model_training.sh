#!/bin/bash
prodigy train ../model --ner ner_rels --eval-split 0.1 --base-model en_core_web_sm --label-stats
