1. 
-------
script = torch.jit.script(model)
sceipt.save('model.pt')

model =torch.jit.load(os.path.join(model_dir,'model.pt'))