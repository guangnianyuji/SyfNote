# Assignment 3-Kaldi

[TOC]



# 1. Installation

I use the linux OS.

1. Run the command

   ```sh
   git clone https://github.com/kaldi-asr/kaldi
   ```

   

2. Check the Dependencies in`kaidi`

   ```sh
   cd tools
   extras/check_dependencies.sh
   ```

   And I need

   ```sh
   sudo apt-get install sox gfortran libtool subversion
   extras/install_mkl.sh
   ```

3. Compile:

   compile tools.

   ```sh
   cd tools
   make -j 8 #I have 8 cpus on my linux machine.
   ```

   It is a long time to wait.

   compile src.

   We want to use cuda. In file `src/configure`, change default configuration: use_cuda=true 

   ```sh
   cd ../src/ 
   ./configure --shared --cudatk-dir=/usr/local/cuda  
   
   make depend -j 8
   
   make -j 8
   ```

4. Test:

   run yes/no example.

   ```sh
   cd ../egs/yesno/s5
   sh run.sh
   ```

   

5. Preparation: thchs30

   ```sh
   wget https://openslr.magicdatatech.com/resources/18/data_thchs30.tgz
   
   tar zxvf data_thchs30.tgz
    
   wget https://openslr.magicdatatech.com/resources/18/resource.tgz
   
   tar zxvf resource.tgz
   ```

   

# 2.  Running yesno and THCHS-30 examples

## yesno

run yes/no example.

```sh
cd ../egs/yesno/s5
sh run.sh
```

If we run successfully, the WER (Word Error Rate) result will appear as shown in the following

![image-20231201162113130](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231201162113130.png)



![image-20231201162251537](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231201162251537.png)



## thchs30

In kaldi, 

```sh
cd egs/thchs30/s5
```

Modify cmd.sh under egs/thchs30 dir

```sh
#export train_cmd=queue.pl
#export decode_cmd="queue.pl --mem 4G"
#export mkgraph_cmd="queue.pl --mem 8G"
#export cuda_cmd="queue.pl --gpu 1“

export train_cmd=run.pl
export decode_cmd="run.pl --mem 4G"
export mkgraph_cmd="run.pl --mem 8G"
export cuda_cmd="run.pl --gpu 1"

```

Modify run.sh under egs/thchs30 dir

```sh
#n=8      #parallel jobs
n=4      #parallel jobs

#thchs=/nfs/public/materials/data/thchs30-openslr
thchs=/mnt/workspace/syf/thchs30/data_thchs30  #your path to data_thchs30

```

According to 

> You can test these four models and comment the rest tests in run.sh.

And we just run the cmd:

```sh
#monophone here
steps/train_mono.sh --boost-silence 1.25 --nj $n --cmd "$train_cmd" data/mfcc/train data/lang exp/mono || exit 1;
#test monophone model
local/thchs-30_decode.sh --mono true --nj $n "steps/decode.sh" exp/mono data/mfcc &

#monophone_ali here 
steps/align_si.sh --boost-silence 1.25 --nj $n --cmd "$train_cmd" data/mfcc/train data/lang exp/mono exp/mono_ali || exit 1;

#triphone
steps/train_deltas.sh --boost-silence 1.25 --cmd "$train_cmd" 2000 10000 data/mfcc/train data/lang exp/mono_ali exp/tri1 || exit 1;
#test tri1 model
local/thchs-30_decode.sh --nj $n "steps/decode.sh" exp/tri1 data/mfcc &

#triphone_ali
steps/align_si.sh --nj $n --cmd "$train_cmd" data/mfcc/train data/lang exp/tri1 exp/tri1_ali || exit 1;

#lda_mllt
steps/train_lda_mllt.sh --cmd "$train_cmd" --splice-opts "--left-context=3 --right-context=3" 2500 15000 data/mfcc/train data/lang exp/tri1_ali exp/tri2b || exit 1;
#test tri2b model
local/thchs-30_decode.sh --nj $n "steps/decode.sh" exp/tri2b data/mfcc &


#lda_mllt_ali
steps/align_si.sh  --nj $n --cmd "$train_cmd" --use-graphs true data/mfcc/train data/lang exp/tri2b exp/tri2b_ali || exit 1;

#sat
steps/train_sat.sh --cmd "$train_cmd" 2500 15000 data/mfcc/train data/lang exp/tri2b_ali exp/tri3b || exit 1;
#test tri3b model
local/thchs-30_decode.sh --nj $n "steps/decode_fmllr.sh" exp/tri3b data/mfcc &

#sat_ali
steps/align_fmllr.sh --nj $n --cmd "$train_cmd" data/mfcc/train data/lang exp/tri3b exp/tri3b_ali || exit 1;
```

### monophone

The result is 

```shell
exp/mono: nj=4 align prob=-100.08 over 25.49h [retry=0.2%, fail=0.0%] states=656 gauss=989
steps/train_mono.sh: Done training monophone system in exp/mono
```

![image-20231203215411874](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231203215411874.png)

The log indicates that a monophone system training, part of a speech recognition experiment using Kaldi software, has been completed. The training utilized four parallel jobs and took 25.49 hours, with a very low retry rate (0.2%) and no failures. It achieved a log likelihood alignment probability of -100.08, and the model was configured with 656 states and 989 Gaussians. The results are stored in the directory 'exp/mono'.

### triphone

The result is

```sh
exp/tri1: nj=4 align prob=-96.76 over 25.48h [retry=0.3%, fail=0.0%] states=1672 gauss=10026 tree-impr=4.80
steps/train_deltas.sh: Done training system with delta+delta-delta features in exp/tri1
```

![image-20231203193834038](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231203193834038.png)

The log entry suggests the completion of a more complex triphone-based speech recognition system using delta and delta-delta features, conducted with the Kaldi toolkit. The process ran with four jobs in parallel, taking 25.48 hours, showing a slight improvement in alignment probability to -96.76, with a retry rate of 0.3% and no failures. This system is larger, with 1672 states and 10026 Gaussians, and it shows a tree improvement score of 4.80. The trained model's data is stored under the 'exp/tri1' directory.



### lda_mllt

The result is

```sh
exp/tri2b: nj=4 align prob=-48.20 over 25.48h [retry=0.5%, fail=0.0%] states=2072 gauss=15030 tree-impr=4.32 lda-sum=24.01 mllt:impr,logdet=1.16,1.67
steps/train_lda_mllt.sh: Done training system with LDA+MLLT features in exp/tri2b
```

![image-20231203194007171](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231203194007171.png)

The log reflects that the 'exp/tri2b' directory holds the results of training a triphone speech recognition system with Linear Discriminant Analysis (LDA) and Maximum Likelihood Linear Transform (MLLT) optimizations. This training ran with four parallel jobs for 25.48 hours, substantially improving the alignment probability to -48.20. The system shows a modest retry rate of 0.5% with no failures, consisting of 2072 states and 15030 Gaussians, and it records a tree improvement of 4.32. Additional LDA and MLLT improvements are noted with scores of 24.01 and 1.16 for improvement and 1.67 for log determinant, respectively.

### sat

The result is

```sh
exp/tri3b: nj=4 align prob=-47.93 over 25.48h [retry=0.7%, fail=0.0%] states=2072 gauss=15018 fmllr-impr=2.41 over 18.97h tree-impr=6.36
steps/train_sat.sh: done training SAT system in exp/tri3b
```

![image-20231203194133106](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231203194133106.png)

The training session logged under 'exp/tri3b' indicates successful training of an advanced triphone-based speech recognition system, incorporating feature-space Maximum Likelihood Linear Regression (fMLLR). This session also utilized four parallel jobs, ran for 25.48 hours, and achieved a very good alignment probability of -47.93. Despite a slightly higher retry rate of 0.7%, there were no failures. The system maintained 2072 states and had a nearly consistent number of Gaussians at 15018. Notably, the fMLLR improvement was recorded at 2.41 over 18.97 hours, and the tree-based clustering improvement was at 6.36, indicating enhancements in the model's accuracy and robustness.

# 3. Record a segment of your own speech and recognize its contents using the trained (THCHS-30) models.

## Installation

1.  Install PortAudio

```
cd tools
./install_portaudio.sh
```

![image-20231203194612367](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231203194612367.png)

2. Compile Related Tools:

   ```
   cd ../src
   make ext
   ```

3. Copy the  dir `kaldi/egs/voxforge/online_demo` to `kaldi/egs/thchs30`

   ![image-20231203200524498](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231203200524498.png)

4. Record your audio. Create `online-data` directory. Put your audio, as the following image.

   ![image-20231203201842011](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231203201842011.png)

5. Change `kaldi/egs/thchs30/online_demo/run.sh`.

   Comment out the file downloading section .

   ![image-20231203195906313](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231203195906313.png)

​	Change the acoustic model type ac_model_type to the trained model  before. For example, I choose `tri3b`

![image-20231203200121399](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231203200121399.png)

6. In dir `online-data`, create dir  `models`.

   - ​	Inside the `models` directory, create a `tri3b` directory.

   - ​	Copy the following files from `s5/exp/tri3b` to your `tri3b` directory: `final.mdl `and 

     `35.mdl`(because symbolic link).

   - ​    Copy the following files from `s5/exp/tri3b/graph_word` to your`tri3b` directory: 

     `words.txt `and `HCLG.fst`.

   ![image-20231203202820088](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231203202820088.png)

7. Modify the recognition code to use your recorded audio  and use your model.

   ![image-20231203204313446](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231203204313446.png)

​	and run the cmd `online_demo\run.sh`.(Exactly,this type of `relative address` often elicits errors, so I use the `absolute address`  in fact.)

## Result

​	And my input is `语音识别作业 这里是上海市同济大学`。

​	And my output is

![image-20231203214856829](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231203214856829.png)



# Reference

1. https://kaldi-asr.org/doc/
2. [Kaldi系列--Ubuntu中TIMIT在线识别（三）_error opening input stream online-data/models/tri1-CSDN博客](https://blog.csdn.net/liahuafu/article/details/79910475)