import argparse
import json
from os import path

from nltk import sent_tokenize
import torch
from transformers import BertTokenizer, BertForNextSentencePrediction
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

def nsp_score(candidates, model_name, device, verbose=False):
    """ Calculate the (contrastive) NSP score
    :param candidates:
    :param model_name:
    :param device:
    :param verbose:
    :return:
    """
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForNextSentencePrediction.from_pretrained(model_name).to(device)
    nsp_scores = list()
    for datum in candidates:
        text_a = datum['text_a']
        sents = sent_tokenize(text_a)
        text_a = sents[-2] + " " + sents[-1]
        text_b = datum['text_b']
        inputs = tokenizer(text_a, text_b, return_tensors='pt').to(device)
        inputs_neg = tokenizer(text_b, text_a, return_tensors='pt').to(device)
        logits = model(**inputs).logits
        logits_neg = model(**inputs_neg).logits
        logits = logits - logits_neg
        contrastive_nsp_score = torch.softmax(logits, axis=-1)[0][0].tolist()
        nsp_scores.append(contrastive_nsp_score)
        if verbose:
            print(f"Last sentence of text_a:\t{text_a}")
            print(f"NSP score ({contrastive_nsp_score}):\t{datum}")
    return nsp_scores


def ppl_score(candidates, model_name, device, verbose=False):
    """ Calculate the negative log likelihood score.
    Since we care only about the rank, it's no difference from the perplexity
    :param candidates:
    :param model_name:
    :param device:
    :param verbose:
    :return:
    """
    model = GPT2LMHeadModel.from_pretrained(model_name).to(device)
    tokenizer = GPT2TokenizerFast.from_pretrained(model_name)
    nll_scores = list()
    for datum in candidates:
        evidence = datum['text_a']
        claim = datum['text_b']
        evidence_inp = tokenizer(evidence, return_tensors='pt')
        claim_inp = tokenizer(claim, return_tensors='pt')
        tgt_len = claim_inp.input_ids.size(1)
        input_ids = torch.cat([evidence_inp.input_ids, claim_inp.input_ids], axis=-1).to(device)
        target_ids = input_ids.clone()
        # mask the evidence so they're not considered when calculating the perplexity
        target_ids[:, :-tgt_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            nll = outputs[0] # TODO: confirm whether to multiply by * tgt_len
            nll_scores.append(nll)
            if verbose:
                print(f"NLL score ({nll}):\t{datum}")
    return nll_scores


def __get_rank(arr, reverse=False):
    return list(map(lambda i: sorted(arr, reverse=reverse).index(i)+1, arr))


def rerank(candidates, nsp_scores, ppl_scores):
    """ rerank the candidates based on different scores
    :param candidates:
    :param nsp_scores:
    :param ppl_scores:
    :return:
    """
    max_nsp_score, best_nsp = float('-inf'), None
    for score, candidate in zip(nsp_scores, candidates):
        if score > max_nsp_score:
            max_nsp_score = score
            best_nsp = candidate

    min_ppl_score, best_ppl = float('inf'), None
    for score, candidate in zip(ppl_scores, candidates):
        if score < min_ppl_score:
            min_ppl_score = score
            best_ppl = candidate

    nsp_rank = __get_rank(nsp_scores, reverse=True)
    ppl_rank = __get_rank(ppl_scores, reverse=False)
    mean_rank = [(nsp+ppl)/2 for nsp, ppl in zip(nsp_rank, ppl_rank)]

    min_rank, best_rank, max_rank, worst_rank = float('inf'), None, float('-inf'), None
    for rank, candidate in zip(mean_rank, candidates):
        if rank < min_rank:
            min_rank = rank
            best_rank = candidate
        if rank > max_rank:
            max_rank = rank
            worst_rank = candidate

    return {"best_nsp": best_nsp, "best_ppl": best_ppl, "best_rank": best_rank, "random": worst_rank}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, default="plot-scene-dataset.jsonl",
                        help="The file containing the previous scene.")
    parser.add_argument("--output_file", type=str, default="plot-scene-best",
                        help="The file containing the instruction.")
    parser.add_argument("--output_dir", type=str, default="movie_exp/scenes/",
                        help="The output directory where generated dataset is saved")
    parser.add_argument("--verbose", action='store_true',
                        help="Print the scores for each candidate.")
    parser.add_argument("--model_name", type=str, default='bert-base-uncased',
                        help="The hugging face model name. Must be a BERT model that has NSP pretraining.")
    parser.add_argument("--ppl_model_name", type=str, default='gpt2',
                        help="The hugging face model name. Must be a GPT-2 model.")
    parser.add_argument("--device", type=str, default='cuda',
                        help="The device to run inference.")
    args = parser.parse_args()

    candidates = list()
    with open(path.join(args.output_dir, args.input_file), "r") as input_file:
        for line in input_file.readlines():
            datum = json.loads(line.strip())
            candidates.append(datum)

    nsp_scores = nsp_score(candidates, args.model_name, verbose=args.verbose, device=args.device)
    ppl_scores = ppl_score(candidates, args.ppl_model_name, verbose=args.verbose, device=args.device)
    result = rerank(candidates, nsp_scores, ppl_scores)

    # writing the results
    with open(f"{path.join(args.output_dir, args.output_file)}-nsp.json", 'w+') as f:
        json.dump(result['best_nsp'], f)

    with open(f"{path.join(args.output_dir, args.output_file)}-ppl.json", 'w+') as f:
        json.dump(result['best_ppl'], f)

    with open(f"{path.join(args.output_dir, args.output_file)}-rank.json", 'w+') as f:
        json.dump(result['best_rank'], f)

    with open(f"{path.join(args.output_dir, args.output_file)}-random.json", 'w+') as f:
        json.dump(result['random'], f)