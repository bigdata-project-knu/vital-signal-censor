# !pip install accelerate==0.27.0 -qq -U
# !pip install bitsandbytes # bitsandbytes version:  0.42.0
# !pip install peft==0.7.2 -qq -U
# pip install accelerate==0.27.0 bitsandbytes==0.42.0 peft==0.7.2 
from transformers import AutoProcessor, AutoModelForPreTraining

processor = AutoProcessor.from_pretrained("HuggingFaceM4/idefics-9b")
model = AutoModelForPreTraining.from_pretrained("Shashwath01/Idefic_medical_VQA_merged_4bit")
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"

def do_inference(model, processor, prompts, max_new_tokens=50):
    tokenizer = processor.tokenizer
    bad_words = ["<image>", "<fake_token_around_image>"]
    if len(bad_words) > 0:
        bad_words_ids = tokenizer(bad_words, add_special_tokens=False).input_ids
    eos_token = "</s>"
    eos_token_id = tokenizer.convert_tokens_to_ids(eos_token)

    while True:
        inputs = processor(prompts, return_tensors="pt").to(device)
        generated_ids = model.generate(
            **inputs,
            eos_token_id=[eos_token_id],
            bad_words_ids=bad_words_ids,
            max_new_tokens=max_new_tokens,
            early_stopping=True
        )
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(generated_text)

        user_input = input("Enter your query (or 'exit' to stop): ")
        if user_input.lower() == 'exit':
            break
        else:
            prompts = [prompts[0], "Question: " + user_input, "Answer:"]


img='/ecg.jpg'

prompts = [
    img,
    "Question: analyze the ecg signal",
    "Answer:"
]

do_inference(model, processor, prompts, max_new_tokens=100)

