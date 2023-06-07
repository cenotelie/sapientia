#!/bin/bash
cd ../../../model_training/prodigy_scripts
./get_annotations.sh
cd ..
cp prodigy_annotations/collins_en/collins_en.jsonl ../nlp/components/rel_component/assets/annotations.jsonl