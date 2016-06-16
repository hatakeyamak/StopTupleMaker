import FWCore.ParameterSet.Config as cms

triggerProducer = cms.EDProducer('prodTriggerResults',
   trigTagSrc = cms.InputTag("TriggerResults"),
   trigPrescalesTagSrc = cms.InputTag("patTrigger"),
   triggerNameList = cms.vstring(
            'HLT_PFHT350_PFMET100_NoiseCleaned_v',
            'HLT_PFHT350_PFMET100_JetIdCleaned_v',
            'HLT_PFHT350_PFMET100_v',
            'HLT_PFMET170_NoiseCleaned_v',
            'HLT_PFMET170_JetIdCleaned_v',
            'HLT_PFHT350_v',
            'HLT_PFHT800_v',
            'HLT_PFHT900_v',
            'HLT_Ele27_eta2p1_WPLoose_Gsf_v',
            'HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf_v',
            'HLT_IsoMu17_eta2p1_v',
            'HLT_PFHT350_PFMET120_NoiseCleaned_v',
            'HLT_Mu15_IsoVVVL_PFHT350_PFMET50_v',
            'HLT_Ele15_IsoVVVL_PFHT350_PFMET50_v',
            'HLT_Mu15_IsoVVVL_PFHT350_PFMET70_v',
            'HLT_Ele15_IsoVVVL_PFHT350_PFMET70_v',
            'HLT_Mu15_IsoVVVL_PFHT400_PFMET70_v',
            'HLT_Ele15_IsoVVVL_PFHT400_PFMET70_v',
            'HLT_Mu15_IsoVVVL_BTagCSV0p72_PFHT400_v',
            'HLT_Mu15_IsoVVVL_BTagCSV07_PFHT400_v',
            'HLT_Mu15_IsoVVVL_PFHT600_v',
            'HLT_Ele15_IsoVVVL_PFHT600_v',
            'HLT_Mu45_eta2p1_v',
            'HLT_Mu50_eta2p1_v',
            'HLT_Mu50_v',
            'HLT_Mu55_v',
            'HLT_Photon75_v',
            'HLT_Photon90_v',
            'HLT_Photon90_CaloIdL_PFHT500_v',
            'HLT_DoubleEle8_CaloIdM_Mass8_PFHT300_v',
            'HLT_Ele27_eta2p1_WP85_Gsf_v',
            'HLT_IsoMu20_eta2p1_IterTrk02_v',
            'HLT_DoubleMu8_Mass8_PFHT300_v',
            'HLT_Ele27_WP85_Gsf_v',
            'HLT_IsoMu20_eta2p1_v',
            'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v',
            'HLT_DoubleMu18NoFiltersNoVtx_v',
            'HLT_Mu20_v',
            'HLT_QuadJet45_TripleCSV0p5_v',
            'HLT_DoubleJet90_Double30_TripleCSV0p5_v',
            'HLT_Ele15_IsoVVVL_PFHT350_v',
            'HLT_Mu15_IsoVVVL_PFHT350_v',
            'HLT_Ele23_WPLoose_Gsf_v',

            'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT250_v',
            'HLT_DoubleMu8_Mass8_PFHT250_v',
            'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v2',
            'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v2',
            'HLT_PFHT750_4JetPt50_v',
            'HLT_PFHT450_SixJet40_PFBTagCSV0p72_v',
            'HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v',
# Additional to RA2/b triggers
            'HLT_PFMET100_PFMHT100_IDTight_v',
            'HLT_PFMET110_PFMHT110_IDTight_v',
            'HLT_PFMET120_PFMHT120_IDTight_v',
            'HLT_PFMET130_PFMHT130_IDTight_v',
            'HLT_PFMET140_PFMHT140_IDTight_v',
            'HLT_PFMET150_PFMHT150_IDTight_v',
            'HLT_IsoMu16_eta2p1_CaloMET30_v',
            'HLT_Mu30_TkMu11_v',
            'HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_MW_v',
            'HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v',
            # New for 2016
            'HLT_PFHT300_PFMET100_v',
            'HLT_PFHT300_v',
   ),
   debug = cms.bool(False),
)


