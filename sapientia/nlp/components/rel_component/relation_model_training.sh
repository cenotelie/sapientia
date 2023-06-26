#!/bin/bash
python3 -m spacy project assets
python3 -m spacy project run data
python3 -m spacy project run train_joint_cpu