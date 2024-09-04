import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
import pandas as pd
import numpy as np

# Define the RNN model
class SongRNN_1(nn.Module):
    def __init__(self, hidden_dim, output_dim, n_layers=2):
        super(SongRNN_1, self).__init__()
        self.rnn = nn.RNN(6, hidden_dim, n_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        output, hidden = self.rnn(x)
        output = self.fc(output)
        return output

class SongRNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, n_layers=2):
        super(SongRNN, self).__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        self.rnn = nn.RNN(input_dim, hidden_dim, n_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x, hidden=None):
        # If hidden state is not provided, initialize it
        if hidden is None:
            hidden = self.init_hidden(x.size(0))

        # Pass the input and hidden state through the RNN
        output, hidden = self.rnn(x, hidden)
        
        # Apply the fully connected layer to the RNN output
        output = self.fc(output)
        
        return output, hidden

    def init_hidden(self, batch_size):
        # Initialize hidden state with zeros
        return torch.zeros(self.n_layers, batch_size, self.hidden_dim)

# complex lstm rnn for song order
class LSTM(nn.Module):
    def __init__(self, n_hidden = 256):
        super(LSTM, self).__init__()
        self.n_hidden = n_hidden
        self.lstm1 = nn.LSTMCell(6,self.n_hidden)
        self.lstm2 = nn.LSTMCell(self.n_hidden,self.n_hidden)
        self.linear = nn.Linear(self.n_hidden,6)
    def forward(self,x,future = 0):
        # device = torch.device('cuda')
        outputs = []
        n_samples = x.size(0)
        h_t = torch.zeros(n_samples,self.n_hidden,dtype=torch.float32)
        c_t = torch.zeros(n_samples,self.n_hidden,dtype=torch.float32)
        h_t2 = torch.zeros(n_samples,self.n_hidden,dtype=torch.float32)
        c_t2 = torch.zeros(n_samples,self.n_hidden,dtype=torch.float32)
        for input_t in torch.split(x,6,dim=1):
            h_t,c_t = self.lstm1(input_t,(h_t,c_t))
            h_t2,c_t2 = self.lstm2(h_t,(h_t2,c_t2))
            output = self.linear(h_t2)
            outputs.append(output)
        for i in range(future):
            h_t,c_t = self.lstm1(input_t,(h_t,c_t))
            h_t2,c_t2 = self.lstm1(h_t,(h_t2,c_t2))
            output = self.linear(h_t2)
            outputs.append(output)
        outputs = torch.cat(outputs,dim=1)
        return outputs

class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size, dropout_p=0.1):
        super(EncoderRNN, self).__init__()
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(input_size, hidden_size).to(device)
        self.gru = nn.GRU(hidden_size, hidden_size, batch_first=True)
        self.dropout = nn.Dropout(dropout_p)

    def forward(self, input):
        embedded = self.dropout(self.embedding(input))
        output, hidden = self.gru(embedded)
        return output, hidden

class DecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size):
        super(DecoderRNN, self).__init__()
        self.embedding = nn.Embedding(output_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size, batch_first=True)
        self.out = nn.Linear(hidden_size, output_size)

    def forward(self, encoder_outputs, encoder_hidden, target_tensor=None):
        batch_size = encoder_outputs.size(0)
        decoder_input = torch.empty(batch_size, 1, dtype=torch.long, device=device)#.fill_(SOS_token)
        decoder_hidden = encoder_hidden
        decoder_outputs = []

        for i in range(6):
            decoder_output, decoder_hidden  = self.forward_step(decoder_input, decoder_hidden)
            decoder_outputs.append(decoder_output)

            if target_tensor is not None:
                # Teacher forcing: Feed the target as the next input
                decoder_input = target_tensor[:, i].unsqueeze(1) # Teacher forcing
            else:
                # Without teacher forcing: use its own predictions as the next input
                _, topi = decoder_output.topk(1)
                decoder_input = topi.squeeze(-1).detach()  # detach from history as input

        decoder_outputs = torch.cat(decoder_outputs, dim=1)
        decoder_outputs = F.log_softmax(decoder_outputs, dim=-1)
        return decoder_outputs, decoder_hidden, None # We return `None` for consistency in the training loop

    def forward_step(self, input, hidden):
        output = self.embedding(input)
        output = F.relu(output)
        output, hidden = self.gru(output, hidden)
        output = self.out(output)
        return output, hidden
    
# Procedures 
# 1. randomize set
# 2. begin padding with (-1, 0) or (-1, -1)
# 3. normalize data, then make copy and lebel it 'y'
# 4. train!


def sort_X_Data():
#               Data:
# 0      [('New', '104'), ('New', '16'), ('New', '18'),...
    datas = pd.read_json('songs.json').swapaxes("index", "columns").reset_index(drop=True)["songList"]
    listy = []
    for list_of_vals in datas:
        if not ('Old' in list_of_vals):
            listy.append(eval(list_of_vals))
    X = pd.DataFrame(listy)
    print(X.drop(X.columns[8:11],axis=1).to_pickle('x_training_data.pkl'))

def encoding_for_training():
    #sort_X_Data()
    X = pd.read_pickle('x_training_data.pkl')
    X = pd.DataFrame(X).drop(index=88).dropna(axis=1,how='all')

    def replace_and_extract(val):
        # if 'New' in val:
        #     return (1, val[1])
        # elif 'Old' in val:
        #     return (0, val[1])
        # else:
        #     return (-1, -1)
        if 'New' in val:
            return int(val[1]) * 0.0001
        else:
            return (-1)
        
    from sklearn.preprocessing import MinMaxScaler
    
    Y = X.copy().fillna(value='-1',axis=1).map(replace_and_extract) #(-1,-1)
    print("Before:\n",X)
    
    shuffled_list = []
    for info in X.iterrows():
        row = info[1]
        row = row.dropna().sample(frac=1, random_state=24)
        shuffled_list.append(row)

    colList = X.columns
    X = pd.DataFrame(shuffled_list)#.reset_index(drop=True, inplace=True)#.reindex_like(X)#.reset_index(drop = True)
    X.columns = colList
    X = X.fillna(value='-1',axis=1) #pos: Do -1,0 (-1,-1)
    X = X.map(replace_and_extract)
    print("After:\n",X)


    # # Separate the tuples into two columns: 'status' and 'value'
    # status_X = X.map(lambda x: x[0]) #New, Old, or None
    # value_X = X.map(lambda x: x[1]) #Songnums 
    # # print(status_X, value_X)
    # status_Y = Y.map(lambda x: x[0]) #New, Old, or None
    # value_Y = Y.map(lambda x: x[1]) #Songnums 

    # Normalize the 'value' column while ignoring -1 values
    # mask = (value_X != -1)
    scaler = MinMaxScaler()
    # value_X[mask] = scaler.fit_transform(value_X[mask].astype(float))

    # value_Y[mask] = scaler.fit_transform(value_Y[mask].astype(float))
    def shuffle_it(df:pd.DataFrame):
        for items in df.iterrows():
            return items[1].map(lambda y: y * 0.001)
    # mask = (X != -1)
    # result_X = X.apply(shuffle_it, axis=1)
    # mask = (Y != -1)
    # result_y = Y.apply(lambda y: int(y) * .001, axis=1)
    print(X)
    print(Y)
    
    # mask = (X != -1)
    # X[mask] = scaler.fit_transform(X[mask].astype(float))
    # mask = (Y != -1)
    # Y[mask] = scaler.fit_transform(Y[mask].astype(float))

    # # print(value_X, value_Y)
    # # Combine the 'status' and normalized 'value' DataFrames back into tuples
    # result_X = pd.DataFrame(index=X.index, columns=X.columns)
    
    # for row in result_X.index:
    #     for col in result_X.columns:
    #         result_X.at[row, col] = X.at[row, col]#(status_X.at[row, col], value_X.at[row, col])
            
    # # print(result_X)
    # #       data:
    # #       0                         1                            2                            3                         4                         5                          6                         7
    # # (1, 0.1328125)  (1, 0.01799485861182519)  (1, 1.3796092135172487e-05)   (1, 0.0001923337550609341)    (1, 0.230188679245283)  (1, 0.10105757931844887)                (-1, -1)                  (-1, -1)
    
    # result_Y = pd.DataFrame(index=Y.index, columns=Y.columns)
    
    # for row in result_Y.index:
    #     for col in result_Y.columns:
    #         result_Y.at[row, col] = Y.at[row, col]#(status_Y.at[row, col], value_Y.at[row, col])

    # result_Y = result_Y.apply(lambda y: y * .001, axis=1) #doing a std is not consistant, so just scaling it down should work?

    # Loading this doesn't work :( , nvm it does i just dumb
    # X = result_X.to_numpy()
    # y = result_Y.to_numpy()
    # np.save('X_train', X)
    # np.save('y_train', y)

    # result_X.to_pickle('X_train.pkl')
    # result_Y.to_pickle('y_train.pkl')
    X.to_pickle('X_train.pkl')
    Y.to_pickle('y_train.pkl')
    # print("X:\n",result_X,"\nY:\n",result_Y)
    #FINALLY DONE!

encoding_for_training() #Curr. only doing new no old book :(

# Model parameters
device = torch.device('cuda')
hidden_dim = 6
output_dim = 6
# USE A VOCAB OF INPUT? PRolly not dynamic
# model = SongRNN(6,hidden_dim, output_dim).to(device)
# model = LSTM(hidden_dim)#.to(device)
# model = PointerNet(6, hidden_dim).to(device)
def train_it():
    #can be compressed into one line, but for troubleshooting must be placeed here, pls move later!
    
    X_train = pd.DataFrame(pd.read_pickle("X_train.pkl"))
    print(X_train.to_numpy())
    y_train = pd.DataFrame(pd.read_pickle("y_train.pkl"))
    X_tensor = torch.tensor(X_train.to_numpy(dtype='float32'), dtype=torch.float32).to(device)
    y_tensor = torch.tensor(y_train.to_numpy(dtype='float32'), dtype=torch.float32).to(device)

    encoder = EncoderRNN(6,256).to(device)
    decoder = DecoderRNN(256, 6).to(device)
    # decoder_Model = SongRNN(6,hidden_dim, output_dim).to(device)
    criterion = nn.MSELoss()
    # optimizer = optim.Adam(decoder.parameters(), lr=0.0001)
    learning_rate = 0.001
    encoder_optimizer = optim.Adam(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.Adam(decoder.parameters(), lr=learning_rate)
    num_epochs = 200
    train_loss = []
    # inputs = X_tensor
    # targets = y_tensor
    for epoch in range(num_epochs):
        for i in range(len(X_tensor)):
            # Get input and target batches and move to GPU if available
            input_tensor = X_tensor[i]#.unsqueeze(0)  # Make it 3D (1, seq_len, input_size)
            target_tensor = y_tensor[i]#.unsqueeze(0)  # Make it 3D (1, seq_len, input_size)
            # Forward pass
            encoder_optimizer.zero_grad()
            decoder_optimizer.zero_grad()

            encoder_outputs, encoder_hidden = encoder(input_tensor)
            decoder_outputs, _, _ = decoder(encoder_outputs, encoder_hidden, target_tensor)

            # Compute loss
            loss = criterion(
                decoder_outputs.view(-1, decoder_outputs.size(-1)),
                target_tensor.view(-1)
            )

            # Backward pass and optimization
            loss.backward()
            encoder_optimizer.step()
            decoder_optimizer.step()
            
            train_loss.append(loss.data[0])

    print(f'Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}')
            
            
    print("Epoch:", epoch, "Loss:", loss.item())
    torch.save(decoder.state_dict(), 'song_rnn_model_decoder.pth')
    torch.save(encoder.state_dict(), 'song_rnn_model_encoder.pth')
    
    
    # return decoder_Model

# train_it()


#time to run!
def run():
    with torch.no_grad():
        device = torch.device('cuda')
        hidden_dim = 256
        output_dim = 6
        model = SongRNN(6, hidden_dim, output_dim)#.to(device)
        # model = train_it(model)
        # model = Model().to(device)
        model.load_state_dict(torch.load('model_weights.pth'))
        # model = model.load('model_weights.pth')
        model.eval()#.to(device)
        input = [36,257,115,193,279,1]
        salt = 0.00001
        input = map(lambda food: food * salt, input)
        salted_input = list(input)
        songs = torch.tensor(salted_input, dtype=torch.float32).to(device)
        # songs = songs.view(1,6,6)
        print(songs.to('cpu').numpy())
        
        songs = songs.view(1,6)
        pred_order = model(songs)
        print(pred_order*10000)#.argmax().item())
    
    