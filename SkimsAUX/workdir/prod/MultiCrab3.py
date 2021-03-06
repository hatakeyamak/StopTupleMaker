#!/usr/bin/env python
# encoding: utf-8

# File        : MultiCrab3.py
# Author      : Ben Wu
# Contact     : benwu@fnal.gov
# Date        : 2015 Apr 01
#
# Description :


import copy, os, time, sys

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientUtilities import colors
from WMCore.Configuration import saveConfigurationFile
from crab3Config import config as config
from multiprocessing import Process

workArea = 'TopTagging_2017_V2'
outDir = '/store/group/lpcsusyhad/Stop_production/TopTagging_2017_V2/'
Pubname = 'TopTagging_2017_V2'
json_25ns = 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
#json_2017 ='Cert_294927-302343_13TeV_PromptReco_Collisions17_JSON.txt'
json_2017 = 'Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
json_2018 = 'Cert_314472-317080_13TeV_PromptReco_Collisions18_JSON.txt'
jsonHCALreval = 'Cert_314472-318876_13TeV_PromptReco_Collisions18_JSON.txt'
# Use the common keyword to select the samples you'd like to submit
# ALL: all of them; NONE: none of them; TEST: test printing out the crab3 config or disable actual submission; STATUS: check job status
# TTJets, WJetsToLNu, ZJetsToNuNu, DYJetsToLL, QCD, TTW, TTZ, ST_tW, SMS, HTMHT, SingleMuon, SingleElectron, DoubleMuon, DoubleEG
# Can be any of the combinations
#selSubmitKey = 'TEST STATUS TTJets' # 'TEST STATUS': no submission of jobs but rather checking crab job status related to the TTJets. If jobs failed, automatically resubmit them.
#selSubmitKey = 'TTJets_SingleLeptFrom HTMHT'
#selSubmitKey = 'TTJets_SingleLeptFrom TTJets_DiLept'
#selSubmitKey = 'TEST HTMHT TTJets_SingleLeptFrom TTJets_DiLept'
#selSubmitKey = 'MET-Run2017B-23Jun2017-v1 MET-Run2017C-PromptReco-v1 MET-Run2017C-PromptReco-v2 MET-Run2017C-PromptReco-v3 MET-Run2017D-PromptReco-v1'
#selSubmitKeun2018A-v1eMuon-Run2017A-PromptReco-v2 SingleMuon-Run2017A-PromptReco-v3 SingleMuon-Run2017B-04Jul2017-v2 SingleMuon-Run2017B-06Jul2017-v2 SingleMuon-Run2017B-12Sep2017-v1 SingleMuon-Run2017B-22Jun2017-v1 SingleMuon-Run2017B-23Jun2017-v1 SingleMuon-Run2017B-PromptReco-v1 SingleMuon-Run2017B-PromptReco-v2 SingleMuon-Run2017C-12Sep2017-v1 SingleMuon-Run2017C-PromptReco-v1 SingleMuon-Run2017C-PromptReco-v2 SingleMuon-Run2017C-PromptReco-v3 SingleMuon-Run2017D-PromptReco-v1 SingleMuon-Run2017E-PromptReco-v1 SingleMuon-Run2017F-PromptReco-v1 SingleMuon-Run2017G-PromptReco-v1'
#selSubmitKey  = 'SingleMuon-Run2017B SingleMuon-Run2017C SingleMuon-Run2017D SingleMuon-Run2017E SingleMuon-Run2017F SingleElectron-Run2017B SingleElectron-Run2017C SingleElectron-Run2017D SingleElectron-Run2017E SingleElectron-Run2017F MET-Run2017B-v1 MET-Run2017C-v1 MET-Run2017D-v1 MET-Run2017E-v1 MET-Run2017F-v1 SinglePhoton-Run2017B SinglePhoton-Run2017C SinglePhoton-Run2017D SinglePhoton-Run2017E SinglePhoton-Run2017F'
selSubmitKey= ' TTJets_amcatnlo'
#'TTToSemiLeptonic_HEM TTToSemiLeptonic_NoHEM'
#'METReval METReval_HEmiss SingleMuonReval_HEmiss SingleMuonReval JetHTReval JetHTReval_HEmiss EGammaReval EGammaReval_HEmiss'
#'RelValSMS-T1tttt_mGl-1500_mLSP-100 RelValNuGun RelValTTbarLepton RelValTTbar' 
#'SingleMuon-Run2018A-v1 SingleMuon-Run2018A-v2 SingleMuon-Run2018A-v3 SingleMuon-Run2018B-v1 SingleMuon-Run2018B-v2'
#'MET-Run2018A-v1 MET-Run2018A-v2 MET-Run2018A-v3 MET-Run2018B-v1'#'TTJets_SingleLet00257'#TTJets_SingleLeptFromT'
#selSubmitKey = 'WWTo2L2Nu'
#selSubmitKey = 'TEST ALL'
#selSubmitKey = 'TEST TTJets_SingleLeptFrom TTJets_Inc TTJets_DiLept ZJetsToNuNu_HT'
doAutoMonitor = False#True

## Format: keyword : IsData, fulldatasetname, unitperjob
jobslist = {
    # TTbar
    'TTJets_Inc'                             : [False, '/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#running
    'TTJets_amcatnlo'                        :[False, '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],
    'TTJets_SingleLeptFromT'            : [False, '/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM', 1],#NotStarted
    'TTJets_SingleLeptFromTbar'              : [False, '/TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#Just started
    'TTJets_SingleLeptFromTbar_ext1'         : [False, '/TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#Just Started
    'TTJets_HT-600to800'                     : [False, '/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#Just Started
    'TTJets_HT-800to1200'                    : [False, '/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#JustStarted
    'TTJets_HT-1200to2500'                   : [False, '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#JustStarted
    'TTJets_HT-2500toInf'                    : [False, '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM', 1],#JustStarted
    'TTJets_DiLept'                          : [False, '/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#JustStarted
    'TTJets_DiLept_ext1'                     : [False, '/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#JustStarted
    'TTToSemiLeptonic_HEM'                   : [False, '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISpring18MiniAOD-HEMPremix_100X_upgrade2018_realistic_v10-v3/MINIAODSIM', 1],    
    'TTToSemiLeptonic_NoHEM'                  : [False, '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISpring18MiniAOD-100X_upgrade2018_realistic_v10_ext1-v1/MINIAODSIM', 1],
  #HEM Full
  'TTTo2L2Nu_Full'                           : [False, '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISpring18MiniAOD-100X_upgrade2018_realistic_v10_ext1-v3/MINIAODSIM', 1],
  'TTTo2L2Nu_HEM'                            : [False, '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISpring18MiniAOD-HEMPremix_100X_upgrade2018_realistic_v10_ext2-v1/MINIAODSIM', 1],
  'WToENu_Full'                              : [False, '/WToENu_M-200_TuneCP5_13TeV-pythia8/RunIISpring18MiniAOD-100X_upgrade2018_realistic_v10-v3/MINIAODSIM', 1],
  'WToENu_HEM'                               : [False, '/WToENu_M-200_TuneCP5_13TeV-pythia8/RunIISpring18MiniAOD-HEMPremix_100X_upgrade2018_realistic_v10_ext1-v1/MINIAODSIM', 1],


    # WJets,
    'WJetsToLNu'                             : [False, '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],#Chain not started
    'WJetsToLNu_HT-70To100'                  : [False, '/WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],#Does not exist
    'WJetsToLNu_HT-100To200'                 : [False, '/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 1],#DONE
    'WJetsToLNu_HT-100To200_ext1'            : [False, '/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 1],#Done
    'WJetsToLNu_HT-100To200_ext2'            : [False, '/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 1],#Done
    'WJetsToLNu_HT-200To400'                 : [False, '/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#Done
    'WJetsToLNu_HT-400To600'                 : [False, '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#Done
    'WJetsToLNu_HT-600To800'                 : [False, '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#Done
    'WJetsToLNu_HT-800To1200'                : [False, '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#done
    'WJetsToLNu_HT-1200To2500'               : [False, '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#Done
    'WJetsToLNu_HT-2500ToInf'                : [False, '/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM', 1],#done


    # Zinv,
    'ZJetsToNuNu_HT-100To200'                : [False, '/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'ZJetsToNuNu_HT-200To400'                : [False, '/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'ZJetsToNuNu_HT-400To600'                : [False, '/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'ZJetsToNuNu_HT-600To800'                : [False, '/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#Started
    'ZJetsToNuNu_HT-800To1200'               : [False, '/ZJetsToNuNu_HT-800To1200_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'ZJetsToNuNu_HT-1200To2500'              : [False, '/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#started
    'ZJetsToNuNu_HT-2500ToInf'               : [False, '/ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#started

    # DYJets,
    'DYJetsToLL_M-50_ext1'                   : [False, '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM', 1],#NOTHING
    'DYJetsToLL_M-50_HT-70to100'             : [False, '/DYJetsToLL_M-50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#Started
    'DYJetsToLL_M-50_HT-100to200'            : [False, '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],#nameissue
    'DYJetsToLL_M-50_HT-100to200_ext1'       : [False, '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 1],#nameissue
    'DYJetsToLL_M-50_HT-200to400'            : [False, '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],#name issue
    'DYJetsToLL_M-50_HT-200to400_ext1'       : [False, '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 1],#name issue
    'DYJetsToLL_M-50_HT-400to600'            : [False, '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],#name issue
    'DYJetsToLL_M-50_HT-400to600_ext1'       : [False, '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 1],
##    'DYJetsToLL_M-50_HT-600toInf'            : [False, '/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 1],
##    'DYJetsToLL_M-50_HT-600toInf_ext1'       : [False, '/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM', 1],
    'DYJetsToLL_M-50_HT-600to800'            : [False, '/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM', 1],
    'DYJetsToLL_M-50_HT-800to1200'           : [False, '/DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'DYJetsToLL_M-50_HT-1200to2500'          : [False, '/DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'DYJetsToLL_M-50_HT-2500toInf'           : [False, '/DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],

    #GammaJets
    'GJets_HT-40To100'                      : [False,'/GJets_DR-0p4_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM', 1],#All F*** up
    'GJets_HT-100To200'                      : [False,'/GJets_DR-0p4_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM', 1],
    'GJets_HT-200To400'                      : [False, '/GJets_DR-0p4_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM', 1],
    'GJets_HT-400To600'                      : [False, '/GJets_DR-0p4_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v2/MINIAODSIM', 1],
    'GJets_HT-600ToInf'                      : [False, '/GJets_DR-0p4_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM', 1],

    # QCD,
    'QCD_HT100to200'                         : [False, '/QCD_HT100to200_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',1],#submitted
    'QCD_HT200to300'                         : [False, '/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM ',1],
    'QCD_HT300to500'                         : [False, '/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM ', 1], 
    'QCD_HT500to700'                         : [False, '/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_old_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],
    'QCD_HT700to1000'                        : [False, '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],
    'QCD_HT1000to1500'                       : [False, '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM ', 1],
    'QCD_HT1500to2000'                       : [False, '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_old_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM ', 1],
    'QCD_HT2000toInf'                        : [False, '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_old_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],

    #ttH and other higgs
    'ttHToNonbb'                             :[False, '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM', 1],#running now
    'ttHTobb'                                :[False, '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#DONE
    'VHToNonbb'                              : [False, '/VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 1],#DONE
    'VHToGG'                                 : [False, '/VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],#nothing yet
    'GluGluHToZZTo4L'                        : [False, '/GluGluHToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],#this does not exist in 2017


    #DiBoson
    'ZZTo2Q2Nu'                              : [False, '/ZZTo2Q2Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],#not exsisting
    'ZZTo2L2Nu'                              : [False, '/ZZTo2L2Nu_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],#no one wants it?
    'ZZTo2L2Q'                               : [False, '/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1],#DONE
    'ZZTo4Q'                                 : [False, '/ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'ZZTo4L'                                 : [False, '/ZZTo4L_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],

    'WZ'                                     : [False, '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'WZ_ext1'                                : [False, '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 1],
    'WZTo1L1Nu2Q'                            : [False, '/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM', 1],
    'WZTo1L3Nu'                              : [False, '/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'WZTo3LNu'                               : [False, '/WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],

    'WWTo4Q'                                 : [False, '/WWTo4Q_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'WWTo2L2Nu'                              : [False, '/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM', 1],
    #'WWTo1L1Nu2Q' : [False, '/WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'WWToLNuQQ'                              : [False, '/WWToLNuQQ_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'WWToLNuQQ_ext1'                         : [False, '/WWToLNuQQ_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 1],

    #TriBoson
    'WWW'                                    : [False, '/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'WWZ'                                    : [False, '/WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'WZZ'                                    : [False, '/WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'ZZZ'                                    : [False, '/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'WZG'                                    : [False, '/WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'WWG'                                    : [False, '/WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 1],

    #tt-Gamma
    'TTGJets'                                : [False, '/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],

    # ttW
    'TTWJetsToQQ'                            : [False, '/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'TTWJetsToLNu_ext1'                      : [False, '/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3/MINIAODSIM', 1],
    'TTWJetsToLNu_ext2'                      : [False, '/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM', 1],

    # ttZ
    'TTZToQQ'                                : [False, '/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
##    'TTZToLLNuNu'                            : [False, '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 1],
    'TTZToLLNuNu_ext1'                       : [False, '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 1],
    'TTZToLLNuNu_ext2'                       : [False, '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM', 1],

    # four top
    'TTTT'                                   : [False, '/TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],

    # single top

    'ST_s-channel_4f_leptonDecays'           : [False, '/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],

    'ST_t-channel_top_4f_inclusiveDecays'    : [False, '/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'ST_t-channel_antitop_4f_inclusiveDecays': [False, '/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],

    'ST_tW_top_5f_inclusiveDecays'           : [False, '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 1],
    'ST_tW_antitop_5f_inclusiveDecays'       : [False, '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 1],

    'ST_tW_top_5f_NoFullyHadronicDecays'     : [False, '/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'ST_tW_top_5f_NoFullyHadronicDecays_ext1': [False, '/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 1],
    'ST_tW_top_5f_NoFullyHadronicDecays_ext2': [False, '/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v2/MINIAODSIM', 1],

    'ST_tW_antitop_5f_NoFullyHadronicDecays' : [False, '/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'ST_tW_antitop_5f_NoFullyHadronicDecays_ext1'  : [False, '/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 1],
    'ST_tW_antitop_5f_NoFullyHadronicDecays_ext2'  : [False, '/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM', 1],

    'ST_tWll_5f'                             : [False, '/ST_tWll_5f_LO_13TeV-MadGraph-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'ST_tWnunu_5f'                           : [False, '/ST_tWnunu_5f_LO_13TeV-MadGraph-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],

    'tZq_ll_4f'                              : [False, '/tZq_ll_4f_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 1],

    # Signals FullSim
    'SMS-T1tttt_mGluino-1200_mLSP-800'       : [False, '/SMS-T1tttt_mGluino-1200_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'SMS-T1tttt_mGluino-1500_mLSP-100'       : [False, '/SMS-T1tttt_mGluino-1500_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'SMS-T1tttt_mGluino-2000_mLSP-100'       : [False, '/SMS-T1tttt_mGluino-2000_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'SMS-T2tt_mStop-225_mLSP-50'             : [False, '/SMS-T2tt_mStop-225_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'SMS-T2tt_mStop-250_mLSP-50'             : [False, '/SMS-T2tt_mStop-250_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'SMS-T2tt_mStop-250_mLSP-150'            : [False, '/SMS-T2tt_mStop-250_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'SMS-T2tt_mStop-300_mLSP-150'            : [False, '/SMS-T2tt_mStop-300_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'SMS-T2tt_mStop-325_mLSP-150'            : [False, '/SMS-T2tt_mStop-325_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'SMS-T2tt_mStop-425_mLSP-325'            : [False, '/SMS-T2tt_mStop-425_mLSP-325_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'SMS-T2tt_mStop-500_mLSP-325'            : [False, '/SMS-T2tt_mStop-500_mLSP-325_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'SMS-T2tt_mStop-650_mLSP-350'            : [False, '/SMS-T2tt_mStop-650_mLSP-350_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],
    'SMS-T2tt_mStop-850_mLSP-100'            : [False, '/SMS-T2tt_mStop-850_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1],

    # FastSim signals
    'SMS-T1tttt_FastSim_scan'                : [False, '/SMS-T1tttt_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 1],
    'SMS-T2tt_FastSim_scan_150to250'         : [False, '/SMS-T2tt_mStop-150to250_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 1],
    'SMS-T2tt_FastSim_scan_250to350'         : [False, '/SMS-T2tt_mStop-250to350_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 1],
    'SMS-T2tt_FastSim_scan_350to400'         : [False, '/SMS-T2tt_mStop-350to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 1],
    'SMS-T2tt_FastSim_scan_400to1200'        : [False, '/SMS-T2tt_mStop-400to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 1],
    'SMS-T5ttcc_FastSim_scan'                : [False, '/SMS-T5ttcc_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v3/MINIAODSIM', 1],
    'SMS-T5tttt_dM175_FastSim_scan'          : [False, '/SMS-T5tttt_dM175_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 1],
    'SMS-T1ttbb_FastSim_scan'                : [False, '/SMS-T1ttbb_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 1],

   #REVALS HCAL issue
  'RelValSMS-T1tttt_mGl-1500_mLSP-100'          : [False, '/RelValSMS-T1tttt_mGl-1500_mLSP-100_13/CMSSW_10_1_7-PU25ns_101X_upgrade2018_realistic_HEmiss_v1-v1/MINIAODSIM', 1],
   'RelValNuGun'            : [False, '/RelValNuGun/CMSSW_10_1_7-PU25ns_101X_upgrade2018_realistic_HEmiss_v1-v1/MINIAODSIM', 1],
   'RelValTTbarLepton'      : [False, '/RelValTTbarLepton_13/CMSSW_10_1_7-PU25ns_101X_upgrade2018_realistic_HEmiss_v1-v1/MINIAODSIM', 1],
'RelValTTbar'               : [False, '/RelValTTbar_13/CMSSW_10_1_7-PU25ns_101X_upgrade2018_realistic_HEmiss_v1-v1/MINIAODSIM', 1],
'RelValQCD_FlatPt_15_3000HS': [False, '/RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_1_7-PU25ns_101X_upgrade2018_realistic_HEmiss_v1-v1/MINIAODSIM', 1],

   'METReval'          : [True, '/MET/CMSSW_10_1_7-101X_dataRun2_Prompt_v11_RelVal_met2018B-v1/MINIAOD', 10],
   'METReval_HEmiss'          : [True, '/MET/CMSSW_10_1_7-101X_dataRun2_Prompt_HEmiss_v1_RelVal_met2018B-v1/MINIAOD', 10],
   'SingleMuonReval'          : [True, '/SingleMuon/CMSSW_10_1_7-101X_dataRun2_Prompt_v11_RelVal_sigMu2018B-v1/MINIAOD', 10],
   'SingleMuonReval_HEmiss'          : [True, '/SingleMuon/CMSSW_10_1_7-101X_dataRun2_Prompt_HEmiss_v1_RelVal_sigMu2018B-v1/MINIAOD', 10],
   'JetHTReval'          : [True, '/JetHT/CMSSW_10_1_7-101X_dataRun2_Prompt_v11_RelVal_jetHT2018B-v1/MINIAOD', 10],
   'JetHTReval_HEmiss'          : [True, '/JetHT/CMSSW_10_1_7-101X_dataRun2_Prompt_HEmiss_v1_RelVal_jetHT2018B-v1/MINIAOD', 10],
   'EGammaReval'          : [True, '/EGamma/CMSSW_10_1_7-101X_dataRun2_Prompt_v11_RelVal_EGamma2018B-v1/MINIAOD', 10],
   'EGammaReval_HEmiss'          : [True, '/EGamma/CMSSW_10_1_7-101X_dataRun2_Prompt_HEmiss_v1_RelVal_EGamma2018B-v1/MINIAOD', 10],

    # Data
    'HTMHT-Run2016H-03Feb2017_ver3-v1'            : [True, '/HTMHT/Run2016H-03Feb2017_ver3-v1/MINIAOD', 10],
    'HTMHT-Run2016H-03Feb2017_ver2-v1'            : [True, '/HTMHT/Run2016H-03Feb2017_ver2-v1/MINIAOD', 10],
    'HTMHT-Run2016G-03Feb2017-v1'                 : [True, '/HTMHT/Run2016G-03Feb2017-v1/MINIAOD', 10],
    'HTMHT-Run2016F-03Feb2017-v1'                 : [True, '/HTMHT/Run2016F-03Feb2017-v1/MINIAOD', 10],
    'HTMHT-Run2016E-03Feb2017-v1'                 : [True, '/HTMHT/Run2016E-03Feb2017-v1/MINIAOD', 10],
    'HTMHT-Run2016D-03Feb2017-v1'                 : [True, '/HTMHT/Run2016D-03Feb2017-v1/MINIAOD', 10],
    'HTMHT-Run2016C-03Feb2017-v1'                 : [True, '/HTMHT/Run2016C-03Feb2017-v1/MINIAOD', 10],
    'HTMHT-Run2016B-03Feb2017_ver2-v2'            : [True, '/HTMHT/Run2016B-03Feb2017_ver2-v2/MINIAOD', 10],
    'HTMHT-Run2016B-03Feb2017_ver1-v1'            : [True, '/HTMHT/Run2016B-03Feb2017_ver1-v1/MINIAOD', 10],

    #For the explaination of the extremely confusing name of MINIAOD, look at https://twiki.cern.ch/twiki/bin/view/CMSPublic/ReMiniAOD03Feb2017Notes 10 is how many lumi sections that are processed when running
    'MET-Run2016H-03Feb2017_ver3-v1'            : [True, '/MET/Run2016H-03Feb2017_ver3-v1/MINIAOD', 10],
    'MET-Run2016H-03Feb2017_ver2-v1'            : [True, '/MET/Run2016H-03Feb2017_ver2-v1/MINIAOD', 10],
    'MET-Run2016G-03Feb2017-v1'                 : [True, '/MET/Run2016G-03Feb2017-v1/MINIAOD', 10],
    'MET-Run2016F-03Feb2017-v1'                 : [True, '/MET/Run2016F-03Feb2017-v1/MINIAOD', 10],
    'MET-Run2016E-03Feb2017-v1'                 : [True, '/MET/Run2016E-03Feb2017-v1/MINIAOD', 10],
    'MET-Run2016D-03Feb2017-v1'                 : [True, '/MET/Run2016D-03Feb2017-v1/MINIAOD', 10],
    'MET-Run2016C-03Feb2017-v1'                 : [True, '/MET/Run2016C-03Feb2017-v1/MINIAOD', 10],
    'MET-Run2016B-03Feb2017_ver2-v2'            : [True, '/MET/Run2016B-03Feb2017_ver2-v2/MINIAOD', 10],
    'MET-Run2016B-03Feb2017_ver1-v1'            : [True, '/MET/Run2016B-03Feb2017_ver1-v1/MINIAOD', 10],

    'MET-Run2017B-v1'	                        : [True, '/MET/Run2017B-17Nov2017-v1/MINIAOD', 8],
    'MET-Run2017C-v1'	                        : [True, '/MET/Run2017C-17Nov2017-v1/MINIAOD', 8],
    'MET-Run2017D-v1'   	                : [True, '/MET/Run2017D-17Nov2017-v1/MINIAOD', 8],
    'MET-Run2017E-v1'             	        : [True, '/MET/Run2017E-17Nov2017-v1/MINIAOD', 8],
    'MET-Run2017F-v1'                           : [True, '/MET/Run2017F-17Nov2017-v1/MINIAOD', 8],


    'SingleMuon-Run2016H-03Feb2017_ver3-v1'            : [True, '/SingleMuon/Run2016H-03Feb2017_ver3-v1/MINIAOD', 10],
    'SingleMuon-Run2016H-03Feb2017_ver2-v1'            : [True, '/SingleMuon/Run2016H-03Feb2017_ver2-v1/MINIAOD', 10],
    'SingleMuon-Run2016G-03Feb2017-v1'                 : [True, '/SingleMuon/Run2016G-03Feb2017-v1/MINIAOD', 10],
    'SingleMuon-Run2016F-03Feb2017-v1'                 : [True, '/SingleMuon/Run2016F-03Feb2017-v1/MINIAOD', 10],
    'SingleMuon-Run2016E-03Feb2017-v1'                 : [True, '/SingleMuon/Run2016E-03Feb2017-v1/MINIAOD', 10],
    'SingleMuon-Run2016D-03Feb2017-v1'                 : [True, '/SingleMuon/Run2016D-03Feb2017-v1/MINIAOD', 10],
    'SingleMuon-Run2016C-03Feb2017-v1'                 : [True, '/SingleMuon/Run2016C-03Feb2017-v1/MINIAOD', 10],
    'SingleMuon-Run2016B-03Feb2017_ver2-v2'            : [True, '/SingleMuon/Run2016B-03Feb2017_ver2-v2/MINIAOD', 10],
    'SingleMuon-Run2016B-03Feb2017_ver1-v1'            : [True, '/SingleMuon/Run2016B-03Feb2017_ver1-v1/MINIAOD', 10],

    'SingleMuon-Run2017B'                 :[True, '/SingleMuon/Run2017B-17Nov2017-v1/MINIAOD', 8],
    'SingleMuon-Run2017C'                 :[True, '/SingleMuon/Run2017C-17Nov2017-v1/MINIAOD', 8],
    'SingleMuon-Run2017D'                :[True, '/SingleMuon/Run2017D-17Nov2017-v1/MINIAOD', 8],
    'SingleMuon-Run2017E'                :[True, '/SingleMuon/Run2017E-17Nov2017-v1/MINIAOD', 8],
    'SingleMuon-Run2017F'                :[True, '/SingleMuon/Run2017F-17Nov2017-v1/MINIAOD', 8],

    'SingleElectron-Run2016H-03Feb2017_ver3-v1'            : [True, '/SingleElectron/Run2016H-03Feb2017_ver3-v1/MINIAOD', 10],
    'SingleElectron-Run2016H-03Feb2017_ver2-v1'            : [True, '/SingleElectron/Run2016H-03Feb2017_ver2-v1/MINIAOD', 10],
    'SingleElectron-Run2016G-03Feb2017-v1'                 : [True, '/SingleElectron/Run2016G-03Feb2017-v1/MINIAOD', 10],
    'SingleElectron-Run2016F-03Feb2017-v1'                 : [True, '/SingleElectron/Run2016F-03Feb2017-v1/MINIAOD', 10],
    'SingleElectron-Run2016E-03Feb2017-v1'                 : [True, '/SingleElectron/Run2016E-03Feb2017-v1/MINIAOD', 10],
    'SingleElectron-Run2016D-03Feb2017-v1'                 : [True, '/SingleElectron/Run2016D-03Feb2017-v1/MINIAOD', 10],
    'SingleElectron-Run2016C-03Feb2017-v1'                 : [True, '/SingleElectron/Run2016C-03Feb2017-v1/MINIAOD', 10],
    'SingleElectron-Run2016B-03Feb2017_ver2-v2'            : [True, '/SingleElectron/Run2016B-03Feb2017_ver2-v2/MINIAOD', 10],
    'SingleElectron-Run2016B-03Feb2017_ver1-v1'            : [True, '/SingleElectron/Run2016B-03Feb2017_ver1-v1/MINIAOD', 10],

    'SingleElectron-Run2017B'             : [True, '/SingleElectron/Run2017B-17Nov2017-v1/MINIAOD', 8],
    'SingleElectron-Run2017C'             : [True, '/SingleElectron/Run2017C-17Nov2017-v1/MINIAOD', 8],
    'SingleElectron-Run2017D'            : [True, '/SingleElectron/Run2017D-17Nov2017-v1/MINIAOD', 8],
    'SingleElectron-Run2017E'            : [True, '/SingleElectron/Run2017E-17Nov2017-v1/MINIAOD', 8],
    'SingleElectron-Run2017F'            : [True, '/SingleElectron/Run2017F-17Nov2017-v1/MINIAOD', 8],

    'SinglePhoton-Run2017B'             : [True, '/SinglePhoton/Run2017B-17Nov2017-v1/MINIAOD', 8],
    'SinglePhoton-Run2017C'             : [True, '/SinglePhoton/Run2017C-17Nov2017-v1/MINIAOD', 8],
    'SinglePhoton-Run2017D'             : [True, '/SinglePhoton/Run2017D-17Nov2017-v1/MINIAOD', 8],
    'SinglePhoton-Run2017E'             : [True, '/SinglePhoton/Run2017E-17Nov2017-v1/MINIAOD', 8],
    'SinglePhoton-Run2017F'             : [True, '/SinglePhoton/Run2017F-17Nov2017-v1/MINIAOD', 8],

    'MET-Run2018A-v1'                       : [True, '/MET/Run2018A-PromptReco-v1/MINIAOD', 100],
    'MET-Run2018A-v2'                       : [True, '/MET/Run2018A-PromptReco-v2/MINIAOD', 100],
    'MET-Run2018A-v3'                       : [True, '/MET/Run2018A-PromptReco-v3/MINIAOD', 100],
    'MET-Run2018B-v1'                       : [True, '/MET/Run2018B-PromptReco-v1/MINIAOD', 100],
    
    'SingleMuon-Run2018A-v1'                : [True, '/SingleMuon/Run2018A-PromptReco-v1/MINIAOD', 100],
    'SingleMuon-Run2018A-v2'                : [True, '/SingleMuon/Run2018A-PromptReco-v2/MINIAOD', 100], 
    'SingleMuon-Run2018A-v3'                : [True, '/SingleMuon/Run2018A-PromptReco-v3/MINIAOD', 100], 
    'SingleMuon-Run2018B-v1'                : [True, '/SingleMuon/Run2018B-PromptReco-v1/MINIAOD', 100], 
    'SingleMuon-Run2018B-v2'                : [True, '/SingleMuon/Run2018B-PromptReco-v2/MINIAOD', 100],


}

tasklist = {}

def MonitoringJobs(tasklist):
    while True:
        sumFailed = 0
        sumComp = 0
        for request, name in tasklist.items():
           dirname = './%s/crab_%s' % (workArea, name)
           fulldir = os.path.abspath(dirname)
           try:
              results = crabCommand('status', dir=fulldir)
              if 'FAILED' in results['status']:
                 sumFailed += 1
              if 'COMPLETED' in results['status']:
                 sumComp += 1
              print "For task", request, "the job states are", results['jobsPerStatus']
              status = results['jobsPerStatus']
              if 'failed' in status:
                 print "failed : ", status['failed']
                 crabCommand('resubmit', dir=fulldir)
           except:
              pass
           time.sleep(2)

        print "\n\n", colors.RED, "sumFailed : ", sumFailed, "  sumComp : ", sumComp, " RE-CHECKING EVERY TASK...\n\n", colors.NORMAL
        if sumFailed == 0 and sumComp == len(tasklist):
           break;

def CreateMonitorList(tasklist):
    monList = open("monList_"+workArea+".txt", 'w')
    for key in sorted(tasklist):
       dirname = './%s/crab_%s' % (workArea, tasklist[key])
       print dirname
       fulldir = os.path.abspath(dirname)
       monList.write("crab status "+fulldir+"\n")
    monList.close()


def SubmitJob(key, value):
    doAll = False
    doTest = False

    allSelKeys = selSubmitKey.split()

    if selSubmitKey.find('NONE') != -1:
       print "Nothing to be done!"
       sys.exit()
    if selSubmitKey.find('ALL') != -1:
       doAll = True
    if selSubmitKey.find('TEST') != -1:
       doTest = True

    doThis = doAll

    if not doAll:
        for selKey in allSelKeys:
            if key.find(selKey) != -1:
                doThis = True
                break;

    if not doThis:
        return

    tempconfig = copy.deepcopy(config)
    tempconfig.General.requestName = key
    tempconfig.General.workArea = workArea
    tempconfig.Data.outputDatasetTag = Pubname + "_" + key
    tempconfig.Data.outLFNDirBase = outDir

    if len(value) <3:
        print "Not enough argument for %s" % key
        raise  AssertionError()
    if value[0]: # Data : note the version number after 23Sep2016 is complicated, so removing them
        if key.find('Run2016B-03Feb2017') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=80X_dataRun2_2016SeptRepro_v7', 'specialFix=JEC BADMUON', 'jecDBname=Summer16_23Sep2016AllV3_DATA']
            tempconfig.JobType.inputFiles = [json_25ns, 'Summer16_23Sep2016AllV3_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_25ns
        elif key.find('Run2016C-03Feb2017') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=80X_dataRun2_2016SeptRepro_v7', 'specialFix=JEC BADMUON', 'jecDBname=Summer16_23Sep2016AllV3_DATA']
            tempconfig.JobType.inputFiles = [json_25ns, 'Summer16_23Sep2016AllV3_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_25ns
        elif key.find('Run2016D-03Feb2017') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=80X_dataRun2_2016SeptRepro_v7', 'specialFix=JEC BADMUON', 'jecDBname=Summer16_23Sep2016AllV3_DATA']
            tempconfig.JobType.inputFiles = [json_25ns, 'Summer16_23Sep2016AllV3_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_25ns
        elif key.find('Run2016E-03Feb2017') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=80X_dataRun2_2016SeptRepro_v7', 'specialFix=JEC BADMUON', 'jecDBname=Summer16_23Sep2016AllV3_DATA']
            tempconfig.JobType.inputFiles = [json_25ns, 'Summer16_23Sep2016AllV3_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_25ns
        elif key.find('Run2016F-03Feb2017') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=80X_dataRun2_2016SeptRepro_v7', 'specialFix=JEC BADMUON', 'jecDBname=Summer16_23Sep2016AllV3_DATA']
            tempconfig.JobType.inputFiles = [json_25ns, 'Summer16_23Sep2016AllV3_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_25ns
        elif key.find('Run2016G-03Feb2017') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=80X_dataRun2_2016SeptRepro_v7', 'specialFix=JEC BADMUON', 'jecDBname=Summer16_23Sep2016AllV3_DATA']
            tempconfig.JobType.inputFiles = [json_25ns, 'Summer16_23Sep2016AllV3_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_25ns
        elif key.find('Run2016H-03Feb2017') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=80X_dataRun2_Prompt_v16', 'specialFix=JEC BADMUON', 'jecDBname=Summer16_23Sep2016AllV3_DATA']
            tempconfig.JobType.inputFiles = [json_25ns, 'Summer16_23Sep2016AllV3_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_25ns
        elif key.find('Run2017B') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=94X_mc2017_realistic_v12', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [json_2017, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_2017
        elif key.find('Run2017C') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=94X_mc2017_realistic_v12', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [json_2017, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_2017
        elif key.find('Run2017D') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=94X_mc2017_realistic_v12', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [json_2017, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_2017
        elif key.find('Run2017E') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=94X_mc2017_realistic_v12', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [json_2017, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_2017
        elif key.find('Run2017F') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=94X_mc2017_realistic_v12', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [json_2017, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_2017
        elif key.find('Run2018A') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=94X_mc2017_realistic_v12', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [json_2018, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_2018
        elif key.find('Run2018B') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=101X_dataRun2_Prompt_v9', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [json_2018, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = json_2018
        elif key.find('METReval') != -1:  
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=101X_dataRun2_Prompt_v11', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [jsonHCALreval, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = jsonHCALreval
        elif key.find('JetHTReval') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=101X_dataRun2_Prompt_v11', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [jsonHCALreval, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = jsonHCALreval
        elif key.find('SingleMuonReval') !=1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=101X_dataRun2_Prompt_v11', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [jsonHCALreval, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = jsonHCALreval
        elif key.find('EGammaReval') !=1: 
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=101X_dataRun2_Prompt_v11', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = ['Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = jsonHCALreval
        elif key.find('METReval_HEmiss') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=101X_dataRun2_Prompt_HEmiss_v1', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [jsonHCALreval, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = jsonHCALreval
        elif key.find('JetHTReval_HEmiss') != -1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=101X_dataRun2_Prompt_HEmiss_v1', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [jsonHCALreval, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = jsonHCALreval
        elif key.find('SingleMuonReval_HEmiss') !=1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=101X_dataRun2_Prompt_HEmiss_v1', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [jsonHCALreval, 'Fall17_17Nov2017BCDEF_V6_DATA.db']
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = jsonHCALreval
        elif key.find('EGammaReval_HEmiss') !=1:
            tempconfig.JobType.pyCfgParams = ['mcInfo=0', 'GlobalTag=101X_dataRun2_Prompt_HEmiss_v1', 'jecDBname=Fall17_17Nov2017BCDEF_V6_DATA']
            tempconfig.JobType.inputFiles = [jsonHCALreval, 'Fall17_17Nov2017BCDEF_V6_DATA.db']       
            tempconfig.Data.splitting = 'LumiBased'
            tempconfig.Data.lumiMask = jsonHCALreval
        else:
            pass
    else:
       if key.find('FastSim') != -1:
          tempconfig.JobType.pyCfgParams = ['mcInfo=1', 'GlobalTag=80X_mcRun2_asymptotic_2016_miniAODv2_v0', 'specialFix=JEC BADMUON', 'jecDBname=Spring16_25nsFastSimMC_V1', 'fastsim=1']
          tempconfig.JobType.inputFiles = ['Spring16_25nsFastSimMC_V1.db']
          tempconfig.Data.splitting = 'FileBased'
       else:
          tempconfig.JobType.pyCfgParams = ['mcInfo=1', 'GlobalTag=94X_mc2017_realistic_v12', 'specialFix=JEC BADMUON', 'jecDBname=Fall17_17Nov2017_V8_MC']
          tempconfig.JobType.inputFiles = ['Fall17_17Nov2017_V8_MC.db']
          tempconfig.Data.splitting = 'FileBased'


    tempconfig.Data.inputDataset = value[1].strip()
    tempconfig.Data.unitsPerJob = value[2]

    if value[0] and len(value) > 3:
        tempconfig.Data.lumiMask = value[3]

    # Submitting jobs
    if doTest:
        saveConfigurationFile(tempconfig, workArea+"/test/"+key+"_test_cfg.py")
        tasklist["crab_"+key] = key
    else:
        results = crabCommand('submit', config = tempconfig)
        tasklist[results['uniquerequestname']] = key
    del tempconfig

if __name__ == "__main__":

    if not os.path.exists(workArea):
       os.makedirs(workArea)
       os.makedirs(workArea+"/test")

    allSelKeys = selSubmitKey.split()

    for key, value in jobslist.items():
        p = Process(target=SubmitJob , args=(key, value))
        p.start()
        p.join()

        for selKey in allSelKeys:
           if key.find(selKey) != -1:
              tasklist["crab_"+key] = key
              break;

    CreateMonitorList(tasklist)

    doTest = False
    doCheckStatus = False

    if selSubmitKey.find('TEST') != -1:
       doTest = True
    if selSubmitKey.find('STATUS') != -1:
       doCheckStatus = True

    if doTest:
       print tasklist

    if (not doTest and doAutoMonitor) or doCheckStatus:
       MonitoringJobs(tasklist)
