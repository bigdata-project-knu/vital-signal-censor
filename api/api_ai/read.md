1. 
-------
script = torch.jit.script(model)

sceipt.save('model.pt')

model =torch.jit.load(os.path.join(model_dir,'model.pt'))

configs = {seqlen : 96,
pred len : 96,
output_attention : False,
use_norm : True,
d_model : 512,
embed : 'timeF',
freq : 'h',
dropout : 0.1
class_strategy :'projection'
d_state : 32,
d_ff : 2048,
activation : 'gelu',
e_layers : 4}


