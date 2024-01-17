import librosa
import numpy as np
import matplotlib.pyplot as plt
'''
Pre-emphasis
Windowing
STFT
Mel-filter bank
Log()
DCT
Dynamic feature extraction
Feature transform
'''

'''
You are allowed to use existing FFT, DCT, 
and log functions as well as plot functions provided by the package in your project.
'''
def pre_emphasis(signal, alpha=0.97):
    emphasized_signal = np.append(signal[0], signal[1:] - alpha * signal[:-1])
    return emphasized_signal

def frame_divide(data, frame_len,frame_mov):

    sig_len = len(data)  # the length of signal
    frame_num = int(np.ceil((sig_len - frame_len) / frame_mov))  # frame number

    # pad zeros (that is because the ceil function makes the actual length of frame longer,
    # so we have to pad zeros)
    zero_num = (frame_num * frame_mov + frame_len) - sig_len
    zeros = np.zeros(zero_num)

    # concat data with zeros
    filled_signal = np.concatenate((data, zeros))
    # print(filled_signal)
    # extract the frame time 
    #[frame_num,frame_len]  [frame_num,frame_len]
    #每个取样点...
    indices = np.tile(np.arange(0, frame_len), (frame_num, 1)) + \
              np.tile(np.arange(0, frame_num * frame_mov, frame_mov), (frame_len, 1)).T#每个frame开始的地方
    # print(indices[:2])
    '''
    frame_mov=1 frame_len=4
    0    0   0   
    1   1    1
    2   2   2
    '''

    # get the data
    indices = np.array(indices, dtype=np.int32)
    divided = filled_signal[indices]
    #print("divided audio",divided.shape)

    return divided

def hamming_window(audio,frame_len,alpha=0.46164):
    save_image(audio[710],"before window",'samples','Amplitude')
    
    n = np.arange(frame_len)
    window = 1-alpha - alpha * np.cos(2 * np.pi * n / (frame_len - 1))
    save_image(window,"Window",'samples','Amplitude')
    windowed_audio = audio * window
    save_image(windowed_audio[710],"after window",'samples','Amplitude')
    return windowed_audio
 
'''
short time fourier transform 

'''
def stft(audio_frame,n_fft):
    magnitude_frame = np.absolute(np.fft.rfft(audio_frame, n_fft))  # the magnitude
   # print("shape",magnitude.shape)
    power_frame=(1.0/n_fft*(magnitude_frame**2))
    save_image(power_frame[710],"power",'freq(Hz)','Amplitude')
    return power_frame
    
    
def mel_filter(sample_rate,n_fft):
    low_freq_mel = 0
    high_freq_mel = 2595 * np.log10(1 + (sample_rate / 2) / 700)
    #print(low_freq_mel, high_freq_mel)
    
    nfilt = 40
    mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # 所有的mel中心点，为了方便后面计算mel滤波器组，左右两边各补一个中心点
    hz_points = 700 * (10 ** (mel_points / 2595) - 1)#对应的f
    
    fbank = np.zeros((nfilt, int(n_fft / 2 + 1)))  # 各个mel滤波器在能量谱对应点的取值
    bin = (hz_points / (sample_rate / 2)) * (n_fft / 2)  # 各个mel滤波器中心点对应FFT的区域编码，找到有值的位置
    
    '''
    这个循环填充了fbank矩阵。对于每个滤波器，它设置了其在FFT二进制索引范围内的值。
    每个滤波器在其中心频率附近为1，然后在其两侧线性递减到0。
    这样，每个滤波器都能捕获其中心频率附近的能量。
    '''
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1])   # left
        f_m = int(bin[m])             # center
        f_m_plus = int(bin[m + 1])    # right
        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
            
    return fbank
 
'''
discrete cosine transform
'''
def dct(log_mel, n_mfcc=26, n_ceps=12):
    transpose = log_mel.T
    len_data = len(transpose)
    # print(len_data)
    dct_audio = []
    for j in range(n_mfcc):
        temp = 0
        for m in range(len_data):
            temp += (transpose[m]) * np.cos(j * (m - 0.5) * np.pi / len_data)
        dct_audio.append(temp)
    ret = np.array(dct_audio[1:n_ceps + 1])
    return ret

def delta(data, k=1):

    delta_feat = []
    transpose = data.T
    q = len(transpose)  # the dimension of the mfcc
    for t in range(q):
        if t < k:
            delta_feat.append(transpose[t + 1] - transpose[t])
        elif t >= q - k:
            delta_feat.append(transpose[t] - transpose[t - 1])
        else:
            denominator = 2 * sum([i ** 2 for i in range(1, k + 1)])
            numerator = sum([i * (transpose[t + i] - transpose[t - i]) for i in range(1, k + 1)])
            delta_feat.append(numerator / denominator)
    return np.array(delta_feat)

def normalization(data):
    
    data_mean=np.mean(data,axis=0,keepdims=True)
    data_vari=np.var(data,axis=0,keepdims=True) 
    return (data-data_mean)/data_vari


def plot_audio(x,y,title,x_label,y_label):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"image/{title}.png") 
    plt.close()
    
def save_image(data,title,x_label,y_label):
    plt.plot(data)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"image/{title}.png") 
    plt.close()
    
# 绘制频谱图
def plot_spectrogram(spec,title,x_label, y_label):
    fig = plt.figure(figsize=(20, 5))
    heatmap = plt.pcolor(spec)
    fig.colorbar(mappable=heatmap)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    #plt.grid()
    plt.tight_layout()
    plt.savefig(f"image/{title}.png") 
    plt.close()
    

if __name__ == "__main__":
    audio_path = "light.wav"
    start_time = 1.0  # Start time of the segment in seconds
    end_time = 3.0    # End time of the segment in seconds
    #Sample Rate）的缩写。采样率是数字音频处理中的重要概念，
    # 它表示在一秒内对连续信号进行采样的次数。采样率通常以赫兹（Hz）为单位表示，表示每秒采集的样本数。
    sr=16000
    audio, _ = librosa.load(audio_path, sr=sr)[:15*sr]
    print("reading finish")
    plot_audio( np.arange(len(audio))/sr,audio,'Audio Waveform','Time (s)','Amplitude')
    
    audio=pre_emphasis(audio)
    print("pre_emphasis finish")
    plot_audio(np.arange(len(audio))/sr,audio,'Pre_emphasis Audio Waveform','Time (s)','Amplitude')
    
    frame_len = int(sr * 0.025)  # the length of frame(25 ms)
    frame_mov = int(sr * 0.010)  # the frame movement(10 ms)
    audio_frame=frame_divide(audio,frame_len,frame_mov)
    
    audio_frame=hamming_window(audio_frame,frame_len)
    print("window finish")
   
    power_frame=stft(audio_frame,n_fft=512)
    #print("power_frame shape",power_frame.shape)
    print("stft finish")
   # save_image(power_frame[200],'Freq Amplitude','Freq (Hz)','Amplitude')
   
    fbank=mel_filter(sample_rate=sr,n_fft=512)
    print("fbank generate finish")

    filter_banks_energy = np.dot(power_frame, fbank.T)
    filter_banks_energy = np.where(filter_banks_energy <= 0, np.finfo(float).eps, filter_banks_energy)
    mel_power_frame = 20 * np.log10(filter_banks_energy)  # dB
    print("apply fbank finish")
    
    #print(mel_data.shape)#(frame_num,nfilter)
    plot_spectrogram(mel_power_frame.T,'filter_banks Spectrum', 'frame_num','Filter Banks')
    
    mfcc=dct(mel_power_frame)
    print("discrete Fourier transform finish")
    
    energy_frame_square_sum=np.sum((power_frame**2).T, axis=0,keepdims=True)
    energy_frame_square_sum[energy_frame_square_sum<=0]=1e-30
    
    energy_frame=10*np.log10(energy_frame_square_sum)  # get the energy
    mfcc=np.append(mfcc,energy_frame,axis=0)   
    plot_spectrogram(mfcc,'mfcc Spectrum', 'frame_num','MFCC coefficients')
    print("mfcc feature generate finish")
    
    delta_data = delta(mfcc)  # first delta
    delta_square_data = delta(delta_data.T)  # second delta
    mfcc_with_delta1 = np.append(mfcc ,delta_data.T, axis=0)  # append first delta
    mfcc_with_delta_1_2 =  np.append(mfcc_with_delta1, delta_square_data.T, axis=0)# append second delta
    plot_spectrogram(mfcc_with_delta_1_2,'mfcc_with_delta1&2 Spectrum', 'frame_num','MFCC coefficients')
    print("dynamic feature generate finish")
    
    
    nor_data=normalization(mfcc_with_delta_1_2)
    plot_spectrogram(nor_data,'normalized mfcc_with_delta1&2 Spectrum', 'frame_num','MFCC coefficients')
    
    
    
    
    

   
    
   
   