import argparse
import time
import os
import numpy as np

class opt_pretrain():
    def __init__(self):
        time_stamp = time.time()
        local_time = time.localtime(time_stamp)
        self.time = time.strftime('%m%d%H%M', local_time)
        self.work_dir = r'~'
        self.work_dir = os.path.abspath(os.path.expanduser(self.work_dir))
        self.work_dir_local = os.path.abspath(os.path.expanduser(self.work_dir))

        # Acoustic setting
        self.acoustic_setting = {
            'sound_speed': 343.0, 
            'fs': 16000, 
            'T': 4.112,
            'nmic': 2,
            'mic_dist_range':[0.03, 0.20]}

    def parse(self):
        """ Function: Define optional arguments
        """
        parser = argparse.ArgumentParser(description='Self-supervised learing for multi-channel audio processing')

        # for training and test stages
        parser.add_argument('--gpu-id', type=str, default='7', metavar='GPU', help='GPU ID (default: 7)')
        parser.add_argument('--workers', type=int, default=8, metavar='Worker', help='number of workers (default: 8)')
        parser.add_argument('--bs', type=int, nargs='+', default=[128, 128, 128], metavar='TrainValTestBatch', help='batch size for training, validation and test (default: [128, 128, 128])')
        parser.add_argument('--no-cuda', action='store_true', default=False, help='disables CUDA training (default: False)')
        parser.add_argument('--use-amp', action='store_true', default=False, help='Use automatic mixed precision training (default: False)')
        parser.add_argument('--seed', type=int, default=1, metavar='Seed', help='random seed (default: 1)')
        
        parser.add_argument('--checkpoint-start', action='store_true', default=False, help='train model from saved latest checkpoints (default: False)')
        parser.add_argument('--checkpoint-from-best-epoch', action='store_true', default=False, help='train model from saved best checkpoints (default: False)')
        parser.add_argument('--time', type=str, default=self.time, metavar='Time', help='time flag')
        parser.add_argument('--work-dir', type=str, default=self.work_dir, metavar='WorkDir', help='work directory')

        parser.add_argument('--sources', type=int, nargs='+', default=[1], metavar='Sources', help='number of sources (default: 1)')
        parser.add_argument('--source-state', type=str, default='static', metavar='SourceState', help='state of sources (default: Static)') # ['static', 'mobile']
        parser.add_argument('--simu-exp', action='store_true', default=False, help='Experiments on simulated data (default: False)')

        parser.add_argument('--pretrain', action='store_true', default=False, help='change to pretrain stage (default: False)')
        parser.add_argument('--pretrain-frozen-encoder', action='store_true', default=False, help='change to pretrain stage (default: False)')
        parser.add_argument('--nepoch', type=int, default=30, metavar='Epoch', help='number of epochs to train (default: 30)')
        parser.add_argument('--lr', type=float, default=0.001, metavar='LR', help='learning rate (default:0.001)')
        
        parser.add_argument('--test', action='store_true', default=False, help='change to test stage of downstream tasks (default: False)')
        parser.add_argument('--test-mode', type=str, default='all', metavar='TestMode', help='test mode (default: all)')

        args = parser.parse_args()
        assert (args.pretrain + args.pretrain_frozen_encoder + args.test)==1, 'Pretraining stage (pretrain or test) is undefined'
        assert args.test_mode in ['all', 'ins'], 'Test mode is undefined'

        self.time = args.time
        self.work_dir = args.work_dir

        args.acoustic_setting = self.acoustic_setting
        
        data = 'sim' if args.simu_exp else 'real'
        print('\ntime='+self.time, 'data='+data)
        
        return args

    def dir(self):
        """ Function: Get directories of code, data and experimental results
        """ 
        work_dir = self.work_dir
        dirs = {}

        dirs['code'] = work_dir + '/SAR-SSL/code'
        dirs['data'] = self.work_dir_local + '/data'
        dirs['gerdata'] = self.work_dir_local + '/SAR-SSL/data'
        dirs['exp'] = work_dir + '/SAR-SSL/exp'

        dirs['micsig_simu_pretrain'] = dirs['gerdata'] + '/MicSig/simu/pretrain'
        dirs['micsig_simu_preval'] = dirs['gerdata'] + '/MicSig/simu/preval'
        dirs['micsig_simu_pretest'] = dirs['gerdata'] + '/MicSig/simu/pretest'
        dirs['micsig_simu_pretest_ins'] = [dirs['gerdata'] + '/MicSig/simu/pretest_ins_T1000']
        dirs['micsig_real_pretrain'] = {
            'DCASE': dirs['gerdata'] + '/MicSig/real/pretrain/DCASE',
            'MIR': dirs['gerdata'] + '/MicSig/real/pretrain/MIR',
            'Mesh': dirs['gerdata'] + '/MicSig/real/pretrain/Mesh',
            'BUTReverb': dirs['gerdata'] + '/MicSig/real/pretrain/BUTReverb',
            'dEchorate': dirs['gerdata'] + '/MicSig/real/pretrain/dEchorate',
            'ACE': dirs['gerdata'] + '/MicSig/real/pretrain/ACE',
            'LOCATA': dirs['data'] + '/MicSig/LOCATA',
            'MCWSJ': dirs['data'] + '/MicSig/MC_WSJ_AV',
            'LibriCSS': dirs['data'] + '/MicSig/LibriCSS',
            'AMI': dirs['data'] + '/MicSig/AMI',
            'AISHELL4': dirs['data'] + '/MicSig/AISHELL-4',
            'M2MeT': dirs['data'] + '/MicSig/M2MeT',
            'RealMAN': dirs['data'] + '/MicSig/RealMAN', 
            'RealMANOri': dirs['data'] + '/MicSig/aligned_static_high_精细对齐_correctDPRIR_filtered3'
            }
        dirs['micsig_real_preval'] = {
            'DCASE': dirs['gerdata'] + '/MicSig/real/preval/DCASE',
            'BUTReverb': dirs['gerdata'] + '/MicSig/real/preval/BUTReverb',
            'AISHELL4': dirs['data'] + '/MicSig/AISHELL-4',
            'M2MeT': dirs['data'] + '/MicSig/M2MeT',
            'RealMAN': dirs['data'] + '/MicSig/RealMAN',
            'RealMANOri': dirs['data'] + '/MicSig/aligned_static_high_精细对齐_correctDPRIR_filtered3'
            }
        dirs['micsig_real_pretest'] = {
            'ACE': dirs['gerdata'] + '/MicSig/real/pretrain/ACE',
            'LOCATA': dirs['data'] + '/MicSig/LOCATA',
            }

        # Experimental data
        dirs['log_pretrain'] = dirs['exp'] + '/pretrain/' + self.time
        dirs['log_pretrain_frozen_encoder'] = dirs['exp'] + '/pretrain_frozen_encoder/' + self.time

        return dirs


class opt_downstream():
    def __init__(self):
        time_stamp = time.time()
        local_time = time.localtime(time_stamp)
        self.time = time.strftime('%m%d%H%M', local_time)
        self.work_dir = r'~'
        self.work_dir = os.path.abspath(os.path.expanduser(self.work_dir))
        self.work_dir_local = os.path.abspath(os.path.expanduser(self.work_dir))

        # Acoustic setting
        self.acoustic_setting = {
            'sound_speed': 343.0, 
            'fs': 16000, 
            'snr_range': [15, 30],
            'nmic': 2,
            'mic_dist_range': [0.03, 0.20]}

        self.extra_info = '' 
        self.ds_token = ''
        self.ds_head = ''
        self.ds_embed = ''
        self.ds_nsimroom = 0

    def parse(self):
        """ Function: Define optional arguments
        """
        parser = argparse.ArgumentParser(description='Self-supervised learing for multi-channel audio processing')

        # for training and test stages
        parser.add_argument('--gpu-id', type=str, default='6,', metavar='GPU', help='GPU ID (default: 1)')
        parser.add_argument('--workers', type=int, default=4, metavar='Worker', help='number of workers (default: 8)')
        # parser.add_argument('--bs', type=int, nargs='+', default=[128, 128, 128], metavar='TrainValTestBatch', help='batch size for training, validation and test (default: [128, 128, 128])')
        parser.add_argument('--no-cuda', action='store_true', default=False, help='disables CUDA training (default: False)')
        parser.add_argument('--use-amp', action='store_true', default=False, help='Use automatic mixed precision training (default: False)')
        parser.add_argument('--seed', type=int, default=1, metavar='Seed', help='random seed (default: 1)')
        
        parser.add_argument('--checkpoint-start', action='store_true', default=False, help='train model from saved checkpoints (default: False)')
        parser.add_argument('--time', type=str, default=self.time, metavar='Time', help='time flag')
        parser.add_argument('--work-dir', type=str, default=self.work_dir, metavar='WorkDir', help='work directory')

        parser.add_argument('--sources', type=int, nargs='+', default=[1], metavar='Sources', help='number of sources (default: 1)')
        parser.add_argument('--source-state', type=str, default='static', metavar='SourceState', help='state of sources (default: Static)') # ['static', 'mobile']
        parser.add_argument('--simu-exp', action='store_true', default=False, help='experiments on simulated data (default: False)')

        parser.add_argument('--ds-train', action='store_true', default=False, help='change to train stage of downstream tasks (default: False)')
        parser.add_argument('--ds-trainmode', type=str, default='finetune', metavar='DSTrainMode', help='how to train downstream models (default: finetune)') # ['scratchLOW', 'finetune', 'lineareval']
        parser.add_argument('--ds-task', type=str, nargs='+', default=['TDOA'], metavar='DSTask', help='downstream task (default: TDOA estimation)')
        parser.add_argument('--ds-token', type=str, default='all', metavar='DSToken', help='downstream token (default: all)') # ['all', 'cls']
        parser.add_argument('--ds-head', type=str, default='mlp', metavar='DSHead', help='downstream head (default: mlp)')  
        parser.add_argument('--ds-embed', type=str, default='spat', metavar='DSEmbed', help='downstream embed (default: spat)') # ['spec_spat', 'spec', 'spat']
        parser.add_argument('--ds-nsimroom', type=int, default=0, metavar='DSSimRoom', help='number of simulated room used for downstream training (default: 0)') 
        parser.add_argument('--ds-real-sim-ratio', type=int, nargs='+', default=[1, 1], metavar='DSRealSimRatio', help='downstream number ratio between real data and simulated data (default: [1, 1])')

        parser.add_argument('--ds-test', action='store_true', default=False, help='change to test stage of downstream tasks (default: False)')
        parser.add_argument('--test-mode', type=str, default='cal_metric_wo_info', metavar='TestMode', help='test mode (default: cal_metric_wo_info)')

        args = parser.parse_args()
        assert (args.ds_train + args.ds_test)==1, 'Downstream stage (train or test) is not defined'
        assert args.ds_trainmode in ['scratchLOW', 'finetune', 'lineareval'], 'Downstream train mode in not defined' # 'sratchUP'   
        assert args.test_mode in ['cal_metric', 'cal_metric_wo_info', 'vis_embed'], 'Test mode is undefined'
        self.simu_exp = args.simu_exp
        self.time = args.time
        self.work_dir = args.work_dir
        self.ds_token = args.ds_token
        self.ds_head = args.ds_head
        self.ds_embed = args.ds_embed
        self.ds_nsimroom = args.ds_nsimroom

        self.ds_specifics = {'task': args.ds_task}
        if self.simu_exp:
            print('\nSimulated experiments:', 'time='+self.time, 'task='+str(args.ds_task), 'ds-embed='+self.ds_embed)
        else:
            if ('TDOA' in args.ds_task) & (len(args.ds_task)==1):
                ds_data = 'real_locata'
            else:
                ds_data = 'real_ace'
            self.ds_specifics['data'] = ds_data
            self.ds_specifics['real_sim_ratio'] = args.ds_real_sim_ratio
            print('\nReal-world experiments:', 'time='+self.time, 'task='+str(args.ds_task), 'ds-embed='+self.ds_embed, 'data='+self.ds_specifics['data'], 'real_sim_ratio='+str(self.ds_specifics['real_sim_ratio']))

        args.ds_specifics = self.ds_specifics
        args.acoustic_setting = self.acoustic_setting
        
        if self.simu_exp: ## Simulate data
            bs_set = [8] # simulated
            lr_set = [0.001, 0.0005, 0.0001, 0.00005] # simulated
            nepoch = 200
            num = args.ds_nsimroom * 100
            ntrial = np.maximum(1, round(32/(args.ds_nsimroom+10e-4)))
            self.ntrail = ntrial
            args.ds_setting = {}
            args.ds_setting['TDOA'] = {'nepoch': nepoch, 'num': num, 'lr_set': lr_set, 'bs_set': bs_set, 'ntrial': ntrial}
            args.ds_setting['DRR'] = {'nepoch': nepoch, 'num': num, 'lr_set': lr_set, 'bs_set': bs_set, 'ntrial': ntrial}
            args.ds_setting['C50'] = {'nepoch': nepoch, 'num': num, 'lr_set': lr_set, 'bs_set': bs_set, 'ntrial': ntrial}
            args.ds_setting['T60'] = {'nepoch': nepoch, 'num': num, 'lr_set': lr_set, 'bs_set': bs_set, 'ntrial': ntrial}
            args.ds_setting['ABS'] = {'nepoch': nepoch, 'num': num, 'lr_set': lr_set, 'bs_set': bs_set, 'ntrial': ntrial}
            self.extra_info = 'R'+str(args.ds_nsimroom)

        else: ## Real-world data
            bs_set = [16] # real-world
            lr_set = [0.001, 0.0001] # real-world 
            nepoch = 200
            num_TDOA = 80000
            if (args.ds_trainmode == 'finetune'):
                if self.ds_specifics['real_sim_ratio'] == [1,0]:
                    num = 1600
                elif self.ds_specifics['real_sim_ratio'] == [1,1]:
                    num = 3200
                elif self.ds_specifics['real_sim_ratio'] == [0,1]:
                    num = 32000
            elif (args.ds_trainmode == 'scratchLOW'):
                if self.ds_specifics['real_sim_ratio'] == [1,0]:
                    num = 1600
                elif self.ds_specifics['real_sim_ratio'] == [1,1]:
                    num = 16000
                elif self.ds_specifics['real_sim_ratio'] == [0,1]:
                    num = 32000
            else:
                raise Exception('Undefined trainmode for the number of real-world training data')
            ntrial = 1
                
            ## Inff plot: set to infinite training epochs for plotting training curves 
            # lr_set = [0.0001] # for TDOA estimation on real-world data 
            # nepoch = 60 # TDOA 
            # num_TDOA = 80000
            # # lr_set = [0.001, 0.0001]
            # # num = 3200
            # # # nepoch = 50 # T60
            # # # nepoch = 300 # DRR
            # # # # nepoch = 150 # C50
            # # # nepoch = 50 # ABS
            # # # nepoch = 200 # TDOA
            
            args.ds_setting = {}
            args.ds_setting['TDOA'] = {'nepoch': nepoch, 'num': num_TDOA, 'lr_set': lr_set, 'bs_set': bs_set, 'ntrial': ntrial}
            args.ds_setting['DRR'] = {'nepoch': nepoch, 'num': num, 'lr_set': lr_set, 'bs_set': bs_set, 'ntrial': ntrial}
            args.ds_setting['C50'] = {'nepoch': nepoch, 'num': num, 'lr_set': lr_set, 'bs_set': bs_set, 'ntrial': ntrial}
            args.ds_setting['T60'] = {'nepoch': nepoch, 'num': num, 'lr_set': lr_set, 'bs_set': bs_set, 'ntrial': ntrial}
            args.ds_setting['ABS'] = {'nepoch': nepoch, 'num': num, 'lr_set': lr_set, 'bs_set': bs_set, 'ntrial': ntrial}

        return args

    def dir(self):
        """ Function: Get directories of code, data and experimental results
        """ 
        work_dir = self.work_dir
        dirs = {}

        dirs['code'] = work_dir + '/SAR-SSL/code'
        # dirs['data'] = work_dir + '/data'
        # dirs['gerdata'] = work_dir + '/SAR-SSL/data'
        dirs['data'] = self.work_dir_local + '/data'
        dirs['gerdata'] = self.work_dir_local + '/SAR-SSL/data'
        dirs['exp'] = work_dir + '/SAR-SSL/exp'

        dirs['srcsig_train'] = dirs['data'] + '/SrcSig/wsj0/tr'
        dirs['srcsig_val'] = dirs['data'] + '/SrcSig/wsj0/dt'
        dirs['srcsig_test'] = dirs['data'] + '/SrcSig/wsj0/et'
        
        dirs['noisig_train'] = dirs['data'] + '/NoiSig/NOISEX-92'
        dirs['noisig_val'] = dirs['data'] + '/NoiSig/NOISEX-92'
        dirs['noisig_test'] = dirs['data'] + '/NoiSig/NOISEX-92'

        # simualted experiments
        if self.simu_exp:
            dirs['micsig_train_simu'] = []
            micsig_train_simu_dir = dirs['gerdata'] + '/MicSig/simu_ds/train'
            for trail_idx in range(self.ntrail):
                room_dirs = []
                for room_idx in range(self.ds_nsimroom):
                    idx = trail_idx * self.ds_nsimroom + room_idx + 1
                    room_dirs += [os.path.join(micsig_train_simu_dir , 'R'+str(idx))]
                dirs['micsig_train_simu'] += [room_dirs]

            dirs['micsig_val_simu'] = dirs['gerdata'] + '/MicSig/simu_ds/val'
            dirs['micsig_test_simu'] = dirs['gerdata'] + '/MicSig/simu_ds/test'

            data_model_flag = 'sim_'

        # real-world experiments
        else:
            # ACE-DRR, T60, C50, ABS estimation
            dirs['rir_real'] = dirs['gerdata'] + '/RIR/real/ACE'
            dirs['rir_train_simu'] = dirs['gerdata'] + '/RIR/simu/train'

            # LOCATA-TDOA estimation
            dirs['micsig_real'] = dirs['data'] + '/MicSig/LOCATA'
            dirs['micsig_real'] = dirs['gerdata'] + '/MicSig/real_ds_locata'
            dirs['micsig_train_simu'] = dirs['gerdata'] + '/MicSig/simu_ds/train'

            data_model_flag = 'real_' + 'train' + str(self.ds_specifics['real_sim_ratio'][0]) + 'real'+ str(self.ds_specifics['real_sim_ratio'][1]) + 'sim_valreal'

        # Experimental data
        dirs['log_pretrain'] = dirs['exp'] + '/pretrain/' + self.time
        
        dirs['log_task'] = dirs['exp'] + '/' + 'TASK' + '/' + self.time

        dirs['log_task_scratchLOW'] = dirs['log_task'] + '/scratchlow-' + self.ds_token + '-' + self.ds_head + '-' + 'NUM' + '-' + 'LR-BAS-TRI' + '-' + self.ds_embed + '-' + data_model_flag + self.extra_info

        dirs['log_task_finetune'] = dirs['log_task'] + '/finetune-' + self.ds_token + '-' + self.ds_head + '-' + 'NUM' + '-' + 'LR-BAS-TRI' + '-' + self.ds_embed + '-' + data_model_flag  + self.extra_info
        dirs['log_task_lineareval'] = dirs['log_task'] + '/lineareval-' + self.ds_token + '-' + self.ds_head + '-' + 'NUM' + '-' + 'LR-BAS-TRI' + '-' + self.ds_embed + '-' + data_model_flag + self.extra_info
        
        return dirs

if __name__ == '__main__':

    args = opt_pretrain().parse()
    dirs = opt_pretrain().dir()
    print('gpu-id: ' + str(args.gpu_id))
    print('code path:' + dirs['code']) 
