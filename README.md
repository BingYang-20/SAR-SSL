# SAR-SSL
A python implementation of “**<a href="https://arxiv.org/abs/2312.00476" target="_blank">Self-Supervised Learning of Spatial Acoustic Representation with Cross-Channel Signal Reconstruction and Multi-Channel Conformer</a>**”

+ **Contributions**
  - **Self-supervised learning of spatial acoustic representation (SSL-SAR)** 
    - first self-supervised learning method in spatial acoustic representation learning and multi-channel audio signal processing
    - designs cross-channel signal reconstruction pretext task to learn the spatial acoustic and the spectral pattern information
    - learns useful knowledge that can be transferred to the spatial acoustics-related tasks

  - **Multi-channel audio Conformer (MC-Conformer)** 
    - unified architecture for both the pretext and downstream tasks
    - learns the local and global properties of spatial acoustics present in the time-frequency domain
    - boosts the performance of both pretext and downstream tasks
    <div align=center>
    <img src=https://github.com/BingYang-20/SAR-SSL/assets/74909427/852ddafa-3fbc-4959-8a7e-e0ce0f2417c6 width=90% />
    </div>

## Datasets
+ **Source signals**: from <a href="https://catalog.ldc.upenn.edu/LDC93S6A" target="_blank">WSJ0 database</a> 
+ **Simulated RIRs**: generated by <a href="https://github.com/DavidDiazGuerra/gpuRIR" target="_blank">gpuRIR toolbox</a> 
+ **Simulated noise**: generated by <a href="https://github.com/ehabets/ANF-Generator" target="_blank">arbitrary noise field generator</a>
+ **Real-world RIRs or microphone signals**: from <a href="https://www.eng.biu.ac.il/gannot/downloads" target="_blank">MIR</a>, <a href="https://zenodo.org/record/5500451" target="_blank">MeshRIR</a>, <a href="https://zenodo.org/record/6408611" target="_blank">DCASE</a>, <a href="https://zenodo.org/record/6576203" target="_blank">dEchorate</a>, <a href="https://speech.fit.vutbr.cz/software/but-speech-fit-reverb-database" target="_blank">BUTReverb</a>, <a href="https://zenodo.org/record/6257551" target="_blank">ACE</a>, <a href="https://zenodo.org/records/3630471" target="_blank">LOCATA</a> databases
    | Datasets | #Room | Microphone Array | #Mic. Pair|  #Room x #Source position x #Array position | Noise Type |
    | :--------: | :--: | :--: | :--: | :--: |  :--: | 
    | MIR | 3  | Three 8-channel linear arrays | 60 | 3 x 26 x 1 | W/o |
    | MeshRIR | 1 | 441 microphones | 8874 | 1 x 32 x 1 | W/o |
    | DCASE | 9 | A 4-channel tetrahedral array (EM32) | 3 | 38530 | Ambience |
    | dEchorate | 11 | Six 5-channel linear arrays | 48 | 11 x 3 x 1 | Ambience, babble, white |
    | BUTReverb | 9 | An 8-channel spherical array | 28 | 51 | Ambience |
    | ACE | 7 | A 2-channel array (Chromebook), | 433 | 7 x 1 x 2 | Ambience, babble, fan |
    | |  | a 3-channel right-angled triangle array (Mobile), | |
    | | | an 8-channel linear array (Lin8Ch), | |
    | | | a 32-channel spherical array (EM32) | |
    | LOCATA | 1 | A 15-channel linear array (DICIT), | 492 |  Moving/static | Ambience |
    | |  | a 12-channel robot array (Robot head), | |
    | |  | a 32-channel spherical array (Eigenmike) | |

## Quick start
### Pretext Task

+ **Preparation**
  - Download datasets to folders according to the following dictionary
    ```
    .-SAR-SSL
    | .-code
    | .-data
    | .-exp
    .-data
      .-SouSig
      | .-wsj0
      |   .-dt
      |   .-et
      |   .-tr
      .-RIR
      | .-DCASE
      | | .-TAU-SRIR_DB
      | | .-TAU-SNoise_DB
      | .-Mesh
      | | .-S32-M441_npy
      | .-MIRDB
      | | .-Impulse_response_Acoustic_Lab_Bar-Ilan_University
      | .-dEchorate
      | | .-dEchorate_database.csv
      | | .-dEchorate_rir.h5
      | | .-dEchorate_annotations.h5
      | | .-dEchorate_noise_gzip7.hdf5
      | | .-dEchorate_babble_gzip7.hdf5
      | | .-dEchorate_silence_gzip7.hdf5
      | .-BUTReverb
      | | .-RIRs
      | .-ACE
      |   .-RIRN
      |   .-Data
      .-SenSig
        .-LOCATA
          .-dev
          .-eval
    ```

  - Install: numpy, scipy, soundfile, tqdm, matplotlib, <a href="https://github.com/DavidDiazGuerra/gpuRIR" target="_blank">gpuRIR</a>, <a href="https://github.com/wiseman/py-webrtcvad" target="_blank">webrtcvad</a>, etc.

+ **Data generation**
  - Simulated data
    ```
    python data_generation_SimulatedSIG_notspecifyroom.py --stage pretrain --wnoise --gpu-id [*]
    python data_generation_SimulatedSIG_notspecifyroom.py --stage preval --wnoise --gpu-id [*] 
    python data_generation_SimulatedSIG_notspecifyroom.py --stage test --wnoise --gpu-id [*]
    ```
  - Real-world data (DCASE, MeshRIR, MIR, ACE, dEchorate, BUTReverb)
    1. select recorded RIRs and noise signals
    ```
    python data_generation_MeasuredRIR.py --data-id 0 --data-type rir noise # DCASE
    python data_generation_MeasuredRIR.py --data-id 3 --data-type rir noise # ACE
    python data_generation_MeasuredRIR.py --data-id 4 --data-type rir noise # dEchorate
    python data_generation_MeasuredRIR.py --data-id 5 --data-type rir noise # BUTReverb
    python data_generation_MeasuredRIR.py --data-id 1 --data-type rir # MeshRIR 
    python data_generation_MeasuredRIR.py --data-id 2 --data-type rir # MIR
    ```
    2. generate microphone signals with recorded RIRs and noise signals 
    ```
    python data_generation_SIGfromMeasuredRIR.py --data-id 0 3 4 5 --wnoise --stage pretrain 
    python data_generation_SIGfromMeasuredRIR.py --data-id 0 3 4 5 --wnoise --stage preval
    python data_generation_SIGfromMeasuredRIR.py --data-id 0 3 4 5 --wnoise --stage test
    python data_generation_SIGfromMeasuredRIR.py --data-id 1 2 --stage pretrain 
    python data_generation_SIGfromMeasuredRIR.py --data-id 1 2 --stage preval
    python data_generation_SIGfromMeasuredRIR.py --data-id 1 2 --stage test
    ```
  - Real-world data (LOCATA)
    ```
    python data_generation_LOCATA.py --stage pretrain
    python data_generation_LOCATA.py --stage preval
    python data_generation_LOCATA.py --stage test_pretrain
    ```
  - Simulated data (some instances)
    1. uncomment `acoustic_scene.dp_mic_signal = []` in class `RandomMicSigDatasetOri` of `data_generation_dataset.py`
    2. specify `room_size`, `T60`, `SNR` in `data_generation_opt.py` (default)
    3. generate corresponding intances
    ```
    python data_generation_SimulatedSIG_notspecifyroom.py --stage test --wnoise --ins --gpu-id 7 
    ```

+ **Training**
  
  Sepcify the data time version (`self.time_ver`) and whether training with simulated data (`self.pretrain_sim`) in class `opt_pretrain` of `opt.py`
  
  ```
  python run_pretrain.py --pretrain --gpu-id [*]
  ```
+ **Evaluation**

  Specify test_mode in run_pretrain.py
  ```
  python run_pretrain.py --test --time [*] --gpu-id [*]
  ```
+ **Trained models**
  - best_model.tar

### Downstream Task

+ **Preparation**
  - the same to pretext task
 
+ **Data generation**
  - Simulated data
    1. generate RIRs 
    ```
    python data_generation_SimulatedRIR.py --gpu-id [*]
    ```
    2. generate microphone signals from RIRs
    ```
    # room = 2, 4, 8, 16, 32, 64, 128 or 256, and room-trial-id = 16, 8, 4, 2, 1, 1 or 1
    python data_generation_SIGfromMeasuredRIR.py --data-id 6 --wnoise --stage train --room 8 --room-trial-id 0 
    python data_generation_SIGfromMeasuredRIR.py --data-id 6 --wnoise --stage val --room 20 
    python data_generation_SIGfromMeasuredRIR.py --data-id 6 --wnoise --stage test --room 20 
    ```

  - Real-world data
    - TDOA estimation
    ```
    python data_generation_LOCATA.py --stage train
    python data_generation_LOCATA.py --stage val 
    python data_generation_LOCATA.py --stage test 
    ```
    - DRR, T60, C50, absorption coefficient estimation: on-the-fly from selected RIRs and noise signals

+ **Training**

  Sepcify the data time version (`self.time_ver`) and whether training with simulated data (`downstream_sim`) in class `opt_downstream` of `opt.py`
  - Simulated data
  ```
  # ds-nsimroom = 2, 4, 8, 16, 32, 64, 128 or 256
  # ds-trainmode = finetune, lineareval or scratchLOW
  python run_downstream.py --ds-train --ds-trainmode finetune --ds-nsimroom 8 --ds-task TDOA --time [*] --gpu-id [*] 
  python run_downstream.py --ds-train --ds-trainmode finetune --ds-nsimroom 8 --ds-task DRR T60 C50 ABS --time [*] --gpu-id [*] 

  python run_downstream.py --ds-train --ds-trainmode scratchUP --ds-task TDOA --time [*] --gpu-id [*] 
  python run_downstream.py --ds-train --ds-trainmode scratchUP --ds-task DRR T60 C50 ABS --time [*] --gpu-id [*] 
  ```
  - Real-world data
  ```
  # ds-trainmode = finetune or scratchLOW
  # ds-real-sim-ratio = 1 1, 1 0 or 0 1
  python run.py --ds-train --ds-trainmode finetune --ds-real-sim-ratio 1 1 --ds-task TDOA ---time [*] --gpu-id [*]
  python run.py --ds-train --ds-trainmode finetune --ds-real-sim-ratio 1 1 --ds-task DRR T60 C50 ABS--time [*] --gpu-id [*]

  ```
+ **Evaluation**

  Specify test mode (`test_mode`) in `run_downstream.py`
  - Simulated data
  ```
  # ds-nsimroom = 2, 4, 8, 16, 32, 64, 128 or 256
  # ds-trainmode = finetune, lineareval or scratchLOW
  python run_downstream.py --ds-test --ds-trainmode finetune --ds-nsimroom 8 --ds-task TDOA --time [*] --gpu-id [*] 
  python run_downstream.py --ds-test --ds-trainmode finetune --ds-nsimroom 8 --ds-task DRR T60 C50 ABS --time [*] --gpu-id [*] 

  python run_downstream.py --ds-test --ds-trainmode scratchUP --ds-task TDOA --time [*] --gpu-id [*] 
  python run_downstream.py --ds-test --ds-trainmode scratchUP --ds-task DRR T60 C50 ABS --time [*] --gpu-id [*] 
  ```
  - Real-world data
  ```
  # ds-trainmode = finetune or scratchLOW
  # ds-real-sim-ratio = 1 1, 1 0 or 0 1
  python run_downstream.py --ds-test --ds-trainmode finetune -ds-real-sim-ratio 1 1 --ds-task TDOA --time [*] --gpu-id [*] 
  python run_downstream.py --ds-test --ds-trainmode finetune -ds-real-sim-ratio 1 1 --ds-task DRR T60 C50 ABS --time [*] --gpu-id [*] 
  ```
  - Read downstream results (MAEs of TDOA, DRR, T60, C50, SNR, ABS estimation) from saved mat files
  ```
  python read_dsmat_bslr.py --time [*]
  python read_lossmetric_simdata.py
  python read_lossmetric_realdata.py
  ```

+ **Trained models**
  - ensemble_model.tar

## Citation
If you find our work useful in your research, please consider citing:
```
@InProceedings{yang2023sarssl,
    author = "Bing Yang and Xiaofei Li",
    title = "Self-Supervised Learning of Spatial Acoustic Representation with Cross-Channel Signal Reconstruction and Multi-Channel Conformer",
    booktitle = "arXiv preprint arXiv:2312.00476",
    year = "2023",
    pages = ""}
```

## Licence
MIT