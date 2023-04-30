## Syntactic Parser for ELL457

This is a project that uses natural language processing to analyze text data. The project uses the `stanfordnlp` library for syntactic parsing.

## Dependencies

- Python 3.6
- `stanfordnlp` library
- `nltk` library

## Acknowledgments

This project uses the `stanfordnlp` library for syntactic parsing. I would like to acknowledge the developers of the `stanfordnlp` library for their contributions to the field of natural language processing.

## Installation

1. Clone the repository.
2. Then download the relevant package and the necessary CoreNLP packages
```
  pip3 install nltk
  cd ~
  wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip
  unzip stanford-corenlp-full-2018-02-27.zip
  cd stanford-corenlp-full-2018-02-27
```

## Usage
1. Still in the `stanford-corenlp-full-2018-02-27` directory, start the server
```
  java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
  -preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
  -status_port 9000 -port 9000 -timeout 15000 & 
```
2. Now run the main script with `python3 stanford.py`
