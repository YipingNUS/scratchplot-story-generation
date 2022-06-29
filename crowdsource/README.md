## Crowdsourced Human Evaluation Data in Plot Writing From Pre-Trained Language Models

The [paper](https://arxiv.org/abs/2206.03021) proposes generating coherent and contentful story plots using off-the-shelf pre-trained language models. The crowdsourcing platform [Toloka](https://toloka.ai/) was used to conduct the human evaluation of the generated stories.

## Fine-grained Aspects Evaluation

We evaluate the generated stories from various baselines on the following aspects (More details and the annotation guidelines can be found in Appendix D.1 of the paper): 

- Naturalness
- Interestingness
- Cohesiveness

We sampled 50 generated stories from each baseline and launched separate evaluation tasks on each aspect. The stories are shuffled so that annotators are unaware of which system generated each story. The raw data is `general-new.tsv`.

The data is contained in the folders `naturalness/`, `interestingness/`, and `coherence/`, respectively. 

### Story Ending Evaluation

We randomly sampled 50 pairs of selected (story, ending) pairs using different algorithms (`nsp`, `perplexity`, and `random`) and asked crowdsource evaluators to conduct a pair-wise evaluation. The result is contained in the `ending/` folder.

### Additional Notes

- In each folder, there is a `train.csv`. It contains a handful of demonstrative examples with their expected labels. It is not the conventional "training data" in ML.
- The `full-annotation-result-new.tsv` file contains the annotation results to produce the final version of the paper.
- The `OUTPUT:category` column is the human annotation. We solicited three annotators for each evaluation. We take the majority vote for the pair-wise evaluation and average the scores for the fine-grained evaluation (on a scale of 1-5). 

### Acknowledgement

The crowdsource human evaluation was funded by [Toloka Research Grant](https://toloka.ai/grants/). We appreciate their generosity and support for the research community.