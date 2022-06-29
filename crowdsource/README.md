## Crowdsource Human Evaluation Data in Plot Writing From Pre-Trained Language Models

The [paper](https://arxiv.org/abs/2206.03021) proposes a method to generate coherent and contentful story plots using off-the-shelf pre-trained language models. The crowdsource platform [Toloka](https://toloka.ai/) was used to conduct the human evaluation on the generated stories.

## Fine-grained Aspects Evaluation

We evaluate the generated stories from various baselines on the following aspects (More details and the annotation guidelines can be found in Appendix D.1 of the paper): 

- Naturalness
- Interestingness
- Cohesiveness

We sample 50 generated stories from each baseline and lauched separate evaluation tasks on each aspect. The stories are shuffled so that annotators are not aware which system generated each story. The raw data is `general-new.tsv`.

The data is contained in the folders `naturalness/`, `interestingness/`, and `coherence/` respectively. 

### Story Ending Evaluation

We randomly sampled 50 pairs of selected (story, ending) pairs selected using different algorithms (`nsp`, `perplexity`, and `random`) and asked crowdsource evaluators to conduct pair-wise evaluation. The result is contained in the `ending/` folder.

### Acknowledgement

The crowdsource human evaluation was funded by [Toloka Research Grant](https://toloka.ai/grants/). We appreciate their generosity and support for the research community.