import torch
import torch.nn.functional as F
from tqdm import trange
import os
import sys
import json
import urllib.request
from transformers import PreTrainedTokenizerFast
from transformers import GPT2LMHeadModel


MODEL_NAME = "skt/kogpt2-base-v2"
MODEL_PATH = "./models/"
SEQ_LEN = 50
TOKENS_DICT = {
    "additional_special_tokens": ["<unused0>", "<unused1>"],
}

tokenizer = PreTrainedTokenizerFast.from_pretrained(MODEL_NAME)
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
tokenizer.add_special_tokens(TOKENS_DICT)

device = torch.device('cpu')
model.load_state_dict(torch.load("smithy/models/processed_slogan_final_5epoch_model.pth", map_location=device))
model.eval()

import torch
import torch.nn.functional as F
from tqdm import trange


def top_k_top_p_filtering(logits, top_k=0, top_p=0.0, filter_value=-float("Inf")):

    top_k = min(top_k, logits.size(-1))
    if top_k > 0:

        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value

    if top_p > 0.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        sorted_indices_to_remove = cumulative_probs > top_p


        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        # 정렬된 텐서를 원래 인덱싱에 분산
        indices_to_remove = sorted_indices_to_remove.scatter(
            dim=1, index=sorted_indices, src=sorted_indices_to_remove
        )
        logits[indices_to_remove] = filter_value
    return logits


def sample_sequence(
    model,
    length,
    context,
    segments_tokens=None,
    num_samples=1,
    temperature=1,
    top_k=0,
    top_p=0.0,
    repetition_penalty=1.0,
    device="cpu",
):
    context = torch.tensor(context, dtype=torch.long, device=device)
    context = context.unsqueeze(0).repeat(num_samples, 1)
    generated = context

    with torch.no_grad():
        for _ in trange(length):

            inputs = {"input_ids": generated}
            if segments_tokens != None:
                inputs["token_type_ids"] = (
                    torch.tensor(segments_tokens[: generated.shape[1]])
                    .unsqueeze(0)
                    .repeat(num_samples, 1)
                )

            outputs = model(**inputs)
            next_token_logits = outputs[0][:, -1, :] / (temperature if temperature > 0 else 1.0)

            for i in range(num_samples):
                for _ in set(generated[i].tolist()):
                    next_token_logits[i, _] /= repetition_penalty

            filtered_logits = top_k_top_p_filtering(next_token_logits, top_k=top_k, top_p=top_p)
            if temperature == 0:  # greedy sampling
                next_token = torch.argmax(filtered_logits, dim=-1).unsqueeze(-1)
            else:
                next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
            generated = torch.cat((generated, next_token), dim=1)
    return generated



# -------------------------------------------------------------------------------

def koslogan(info):  # 여기에 사용자 인풋값 받게끔

    context_tkn = tokenizer.additional_special_tokens_ids[0]
    slogan_tkn = tokenizer.additional_special_tokens_ids[1]

    input_ids = [context_tkn] + tokenizer.encode(info)

    segments = [slogan_tkn] * SEQ_LEN
    segments[: len(input_ids)] = [context_tkn] * len(input_ids)

    input_ids += [slogan_tkn]

    # device = torch.device('cpu')
    # model.load_state_dict(torch.load("smithy/models/processed_slogan_final_5epoch_model.pth", map_location=device))
    # model.eval()

    generated = sample_sequence(
        model,
        length=30,
        context=input_ids,
        segments_tokens=segments,
        temperature=0.9,
        top_k=50,
        top_p=0.95,
        num_samples=4,
    )

    slogans = []
    for g in generated:
        slogan = tokenizer.decode(g.squeeze().tolist())
        slogan = slogan.split('</s>')[0].split('<unused1>')[1]
        slogans.append(slogan)

    return slogans