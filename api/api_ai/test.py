
class Exp_Long_Term_Forecast(Exp_Basic):
    def __init__(self, args):
        super(Exp_Long_Term_Forecast, self).__init__(args)

    def _build_model(self):
        model = Model(self.args).float()

        if self.args.use_multi_gpu and self.args.use_gpu:
            model = nn.DataParallel(model, device_ids=self.args.device_ids)
        return model

    def _get_data(self, flag):
        data_set, data_loader = data_provider(self.args, flag)
        return data_set, data_loader

    def _select_optimizer(self):
        model_optim = optim.Adam(self.model.parameters(), lr=self.args.learning_rate)
        return model_optim

    def _select_criterion(self):
        criterion = nn.MSELoss()
        return criterion

    def vali(self, vali_data, vali_loader, criterion):
        total_loss = []
        self.model.eval()
        with torch.no_grad():
            for i, (batch_x, batch_y, batch_x_mark, batch_y_mark) in enumerate(vali_loader):
                batch_x = batch_x.float().to(self.device)
                batch_y = batch_y.float()

                if 'PEMS' in self.args.data or 'ECG' in self.args.data:
                    batch_x_mark = None
                    batch_y_mark = None
                else:
                    batch_x_mark = batch_x_mark.float().to(self.device)
                    batch_y_mark = batch_y_mark.float().to(self.device)

                # decoder input
                dec_inp = torch.zeros_like(batch_y[:, -self.args.pred_len:, :]).float()
                dec_inp = torch.cat([batch_y[:, :self.args.label_len, :], dec_inp], dim=1).float().to(self.device)
                # encoder - decoder
                if self.args.use_amp:
                    with torch.cuda.amp.autocast():
                        if self.args.output_attention:
                            outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)[0]
                        else:
                            outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
                else:
                    if self.args.output_attention:
                        outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)[0]
                    else:
                        outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
                f_dim = -1 if self.args.features == 'MS' else 0
                outputs = outputs[:, -self.args.pred_len:, f_dim:]
                batch_y = batch_y[:, -self.args.pred_len:, f_dim:].to(self.device)

                pred = outputs.detach().cpu()
                true = batch_y.detach().cpu()

                loss = criterion(pred, true)

                total_loss.append(loss)
        total_loss = np.average(total_loss)
        self.model.train()
        return total_loss

  def test(self, setting, test=0):
          test_data, test_loader = self._get_data(flag='test')
          if test:
              print('loading model')
              self.model.load_state_dict(torch.load(os.path.join('./checkpoints/' + setting, 'checkpoint.pth')))
  
          preds = []
          trues = []
          folder_path = './test_results/' + setting + '/'
          if not os.path.exists(folder_path):
              os.makedirs(folder_path)
  
          self.model.eval()
          with torch.no_grad():
              for i, (batch_x, batch_y, batch_x_mark, batch_y_mark) in enumerate(test_loader):
                  batch_x = batch_x.float().to(self.device)
                  batch_y = batch_y.float().to(self.device)
  
                  if 'PEMS' in self.args.data or 'Solar' in self.args.data:
                      batch_x_mark = None
                      batch_y_mark = None
                  else:
                      batch_x_mark = batch_x_mark.float().to(self.device)
                      batch_y_mark = batch_y_mark.float().to(self.device)
  
                  # decoder input
                  dec_inp = torch.zeros_like(batch_y[:, -self.args.pred_len:, :]).float()
                  dec_inp = torch.cat([batch_y[:, :self.args.label_len, :], dec_inp], dim=1).float().to(self.device)
                  # encoder - decoder
                  if self.args.use_amp:
                      with torch.cuda.amp.autocast():
                          if self.args.output_attention:
                              outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)[0]
                          else:
                              outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
                  else:
                      if self.args.output_attention:
                          outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)[0]
  
                      else:
                          outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
  
                  f_dim = -1 if self.args.features == 'MS' else 0
                  outputs = outputs[:, -self.args.pred_len:, f_dim:]
                  batch_y = batch_y[:, -self.args.pred_len:, f_dim:].to(self.device)
                  outputs = outputs.detach().cpu().numpy()
                  batch_y = batch_y.detach().cpu().numpy()
                  if test_data.scale and self.args.inverse:
                      shape = outputs.shape
                      outputs = test_data.inverse_transform(outputs.squeeze(0)).reshape(shape)
                      batch_y = test_data.inverse_transform(batch_y.squeeze(0)).reshape(shape)
  
                  pred = outputs
                  true = batch_y
  
                  preds.append(pred)
                  trues.append(true)
                  if i % 20 == 0:
                      input = batch_x.detach().cpu().numpy()
                      if test_data.scale and self.args.inverse:
                          shape = input.shape
                          input = test_data.inverse_transform(input.squeeze(0)).reshape(shape)
                      gt = np.concatenate((input[0, :, -1], true[0, :, -1]), axis=0)
                      pd = np.concatenate((input[0, :, -1], pred[0, :, -1]), axis=0)
                      visual(gt, pd, os.path.join(folder_path, str(i) + '.pdf'))
  
          preds = np.array(preds)
          trues = np.array(trues)
          print('test shape:', preds.shape, trues.shape)
          preds = preds.reshape(-1, preds.shape[-2], preds.shape[-1])
          trues = trues.reshape(-1, trues.shape[-2], trues.shape[-1])
          print('test shape:', preds.shape, trues.shape)
  
          # 결과 저장
          folder_path = './results/' + setting + '/'
          if not os.path.exists(folder_path):
              os.makedirs(folder_path)
  
          mae, mse, rmse, mape, mspe = metric(preds, trues)
          print('mse:{}, mae:{}'.format(mse, mae))
          f = open("result_long_term_forecast.txt", 'a')
          f.write(setting + "  \n")
          f.write('mse:{}, mae:{}'.format(mse, mae))
          f.write('\n')
          f.write('\n')
          f.close()
  
          np.save(folder_path + 'metrics.npy', np.array([mae, mse, rmse, mape, mspe]))
          np.save(folder_path + 'pred.npy', preds)
          np.save(folder_path + 'true.npy', trues)
  

Exp = Exp_Long_Term_Forecast
exp = Exp(args)
exp.test(setting)
