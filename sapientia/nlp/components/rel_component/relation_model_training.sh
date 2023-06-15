#!/bin/bash
rm -rf data
mkdir data
rm -rf training
mkdir training
python3 -m spacy project assets
python3 -m spacy project run data
python3 -m spacy project run train_joint_cpu