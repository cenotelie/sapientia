#!/bin/bash
prodigy train ../model --ner airbus_collins --eval-split 0.1 --base-model en_core_web_sm --label-stats
